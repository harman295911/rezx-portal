# vless_ws.py - Lightweight High-Performance VLESS WebSocket Handler for RezX Modz
import socket
import select
import struct
import hashlib
import base64
import threading

def make_ws_frame(payload, opcode=0x02):
    length = len(payload)
    if length < 126:
        header = bytes([0x80 | opcode, length])
    elif length <= 0xFFFF:
        header = bytes([0x80 | opcode, 126]) + struct.pack('!H', length)
    else:
        header = bytes([0x80 | opcode, 127]) + struct.pack('!Q', length)
    return header + payload

def read_exact(sock, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf.extend(chunk)
    return bytes(buf)

def read_ws_frame(sock):
    header = read_exact(sock, 2)
    if not header:
        return None, None
    b0 = header[0]
    b1 = header[1]
    opcode = b0 & 0x0F
    masked = bool(b1 & 0x80)
    payload_len = b1 & 0x7F

    if payload_len == 126:
        ext = read_exact(sock, 2)
        if not ext: return None, None
        payload_len = struct.unpack('!H', ext)[0]
    elif payload_len == 127:
        ext = read_exact(sock, 8)
        if not ext: return None, None
        payload_len = struct.unpack('!Q', ext)[0]

    mask = None
    if masked:
        mask = read_exact(sock, 4)
        if not mask: return None, None

    payload = read_exact(sock, payload_len)
    if payload is None:
        return None, None

    if masked:
        unmasked = bytearray(payload)
        for i in range(len(unmasked)):
            unmasked[i] ^= mask[i % 4]
        return bytes(unmasked), opcode

    return payload, opcode

def handle_vless_connection(client_sock):
    target_sock = None
    try:
        client_sock.settimeout(15.0)
        first_payload, opcode = read_ws_frame(client_sock)
        if not first_payload or len(first_payload) < 20:
            return

        # Parse VLESS request header
        pos = 0
        ver = first_payload[pos]; pos += 1
        uid = first_payload[pos:pos+16]; pos += 16
        addons_len = first_payload[pos]; pos += 1
        pos += addons_len
        cmd = first_payload[pos]; pos += 1
        target_port = struct.unpack('!H', first_payload[pos:pos+2])[0]; pos += 2
        atyp = first_payload[pos]; pos += 1

        if atyp == 1: # IPv4
            dest = socket.inet_ntoa(first_payload[pos:pos+4]); pos += 4
        elif atyp == 2: # Domain
            dlen = first_payload[pos]; pos += 1
            dest = first_payload[pos:pos+dlen].decode('utf-8', errors='ignore'); pos += dlen
        elif atyp == 3: # IPv6
            dest = socket.inet_ntop(socket.AF_INET6, first_payload[pos:pos+16]); pos += 16
        else:
            return

        initial_data = first_payload[pos:]

        # Connect to destination server (TCP)
        print(f'[vless_ws] CMD: {cmd}, Target: {dest}:{target_port}')
        target_sock = socket.create_connection((dest, target_port), timeout=8.0)
        client_sock.settimeout(None)
        target_sock.settimeout(None)

        if initial_data:
            target_sock.sendall(initial_data)

        # Send VLESS response header: \x00 (ver 0) + \x00 (addons len 0)
        first_resp = b'\x00\x00'
        client_sock.sendall(make_ws_frame(first_resp))

        # Bidirectional streaming pump
        def client_to_target():
            try:
                while True:
                    data, op = read_ws_frame(client_sock)
                    if data is None:
                        break
                    if op == 0x08: # Close frame
                        break
                    if data:
                        target_sock.sendall(data)
            except Exception:
                pass
            finally:
                try: target_sock.shutdown(socket.SHUT_WR)
                except Exception: pass

        def target_to_client():
            try:
                while True:
                    data = target_sock.recv(16384)
                    if not data:
                        break
                    client_sock.sendall(make_ws_frame(data))
            except Exception:
                pass
            finally:
                try: client_sock.shutdown(socket.SHUT_WR)
                except Exception: pass

        t1 = threading.Thread(target=client_to_target, daemon=True)
        t2 = threading.Thread(target=target_to_client, daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    except Exception as e:
        import traceback
        print(f'[vless_ws ERR] {e}')
        traceback.print_exc()
    finally:
        if target_sock:
            try: target_sock.close()
            except Exception: pass
        if client_sock:
            try: client_sock.close()
            except Exception: pass
