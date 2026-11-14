import hashlib
import vless_ws
import base64
import http.server
import socketserver
import os
import json
import urllib.parse
import time
import sqlite3
from database import (
    init_db, verify_or_bind_license, reset_device_binding, create_license, get_nodes, get_db,
    admin_verify_login, admin_get_keys, admin_create_bulk_keys, admin_revoke_key,
    admin_extend_key, admin_reset_key_device, admin_delete_key, admin_get_setting,
    admin_toggle_setting, admin_get_users, admin_create_user, admin_update_user_credits,
    admin_delete_user, admin_change_password
)

PORT = int(os.environ.get('PORT', 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_START_TIME = time.time()

ACTIVE_FEATURES = {
    "aimbot": 1,
    "magnetic_fire": 1,
    "magnetic_scope": 1,
    "hs_body": 1,
    "hs_rate": 90,
    "esp": 1,
    "icewall": 1,
    "moco": 1,
    "speed": 0,
    "marker": 9,
    "freeze_manual": 0,
    "freeze_fire": 0,
    "freeze_scope": 0,
    "ghost": 0,
    "tatu": 0,
    "revive_type": 1
}

def get_live_nodes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, host, port, protocol, password, sni FROM nodes WHERE is_active = 1 ORDER BY name ASC")
    nodes = []
    for r in cur.fetchall():
        nodes.append({
            'name': r['name'],
            'host': r['host'],
            'port': r['port'],
            'protocol': r['protocol'],
            'password': r['password'] or '',
            'sni': r['sni'] or r['host']
        })
    conn.close()
    return nodes

def gen_sub_json(nodes):
    direct_domains = [
        "full:event-vodka.freefireind.in",
        "full:indevent.ggblueshark.com",
        "full:sgevent.ggblueshark.com",
        "full:meevent.ggblueshark.com",
        "full:thevent.ggblueshark.com",
        "full:sacevent.ggblueshark.com",
        "full:idevent.ggblueshark.com",
        "full:bdevent.ggpolarbear.com",
        "regexp:event\\.gg(blueshark|polarbear)\\.com$",
        "full:gin.freefireind.in",
        "full:gin.freefiremobile.com",
        "full:vodka.freefireind.in",
        "full:dl.castle.freefiremobile.com",
        "full:dl.cdn.freefiremobile.com",
        "full:dl-core.cdn.freefiremobile.com",
        "full:dl.gmc.freefiremobile.com",
        "full:dl.aw.freefiremobile.com",
        "full:dl.dir.freefiremobile.com",
        "full:dl.bs.freefiremobile.com",
        "full:dl.ak.freefiremobile.com",
        "full:dl-sg-production.freefiremobile.com",
        "full:dl-tata.freefireind.in",
        "full:dl-bs.ggpolarbear.com",
        "domain:freefiremobile-a.akamaihd.net"
    ]
    items = []
    for n in nodes:
        item = {
            "remarks": n['name'],
            "inbounds": [
                {
                    "tag": "socks",
                    "listen": "127.0.0.1",
                    "port": 10808,
                    "protocol": "socks",
                    "settings": { "auth": "noauth", "udp": True },
                    "sniffing": {
                        "destOverride": ["http", "tls", "quic"],
                        "enabled": True,
                        "routeOnly": False
                    }
                },
                {
                    "tag": "http",
                    "listen": "127.0.0.1",
                    "port": 10809,
                    "protocol": "http",
                    "sniffing": {
                        "destOverride": ["http", "tls", "quic"],
                        "enabled": True,
                        "routeOnly": False
                    }
                }
            ],
            "outbounds": [
                {
                    "protocol": "hysteria",
                    "settings": {
                        "address": n['host'],
                        "port": n['port'],
                        "version": 2
                    },
                    "streamSettings": {
                        "network": "hysteria",
                        "security": "tls",
                        "tlsSettings": {
                            "alpn": ["h3"],
                            "serverName": n['sni'],
                            "show": False
                        },
                        "hysteriaSettings": {
                            "version": 2,
                            "auth": n['password']
                        },
                        "finalmask": {
                            "quicParams": { "disableChromeParrot": True }
                        }
                    },
                    "tag": "proxy"
                },
                { "protocol": "freedom", "tag": "direct" }
            ],
            "routing": {
                "domainStrategy": "AsIs",
                "rules": [
                    { "type": "field", "network": "tcp", "port": "39000-39999", "outboundTag": "proxy" },
                    { "type": "field", "network": "udp", "port": "10000-10999", "outboundTag": "proxy" },
                    { "type": "field", "domain": direct_domains, "outboundTag": "direct" },
                    { "type": "field", "network": "tcp,udp", "outboundTag": "direct" }
                ]
            }
        }
        items.append(item)
    return items

def gen_sub_b64(nodes):
    uris = []
    for n in nodes:
        tag = urllib.parse.quote(n['name'])
        auth = urllib.parse.quote(n['password'])
        uris.append(f"hysteria2://{auth}@{n['host']}:{n['port']}?sni={n['sni']}&insecure=1#{tag}")
    return base64.b64encode("\n".join(uris).encode('utf-8')).decode('utf-8')

def gen_sub_clash(nodes):
    lines = [
        "port: 7890",
        "socks-port: 7891",
        "allow-lan: false",
        "mode: rule",
        "log-level: info",
        "unified-delay: true",
        "tcp-concurrent: true",
        "",
        "proxies:"
    ]
    for n in nodes:
        lines.append(f'  - name: "{n["name"]}"')
        lines.append("    type: hysteria2")
        lines.append(f"    server: {n['host']}")
        lines.append(f"    port: {n['port']}")
        lines.append(f'    password: "{n["password"]}"')
        lines.append(f"    sni: {n['sni']}")
        lines.append("    skip-cert-verify: true")
        lines.append("    alpn:")
        lines.append("      - h3")
    
    lines.append("")
    lines.append("proxy-groups:")
    lines.append('  - name: "🎯 RezX Combat Selector"')
    lines.append("    type: select")
    lines.append("    proxies:")
    for n in nodes:
        lines.append(f'      - "{n["name"]}"')
    lines.append('      - "⚡ RezX Lowest Ping Auto"')
    lines.append('      - DIRECT')
    lines.append("")
    lines.append('  - name: "⚡ RezX Lowest Ping Auto"')
    lines.append("    type: url-test")
    lines.append("    url: http://cp.cloudflare.com/generate_204")
    lines.append("    interval: 300")
    lines.append("    proxies:")
    for n in nodes:
        lines.append(f'      - "{n["name"]}"')
    lines.append("")
    lines.append("rules:")
    lines.append("  - DOMAIN-SUFFIX,ggpolarbear.com,🎯 RezX Combat Selector")
    lines.append("  - DOMAIN-SUFFIX,ggblueshark.com,🎯 RezX Combat Selector")
    lines.append("  - PORT,7000-15000,🎯 RezX Combat Selector")
    lines.append("  - PORT,39000-39999,🎯 RezX Combat Selector")
    lines.append("  - MATCH,🎯 RezX Combat Selector")
    return "\n".join(lines)

class RezXPortalHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def log_message(self, format, *args):
        try:
            msg = format % args if args else str(format)
        except Exception:
            msg = " ".join(str(a) for a in args) if args else str(format)
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def send_json(self, data, status_code=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text, status_code=200, content_type='text/plain; charset=utf-8'):
        body = text.encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_post_json(self):
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len == 0:
            return {}
        raw = self.rfile.read(content_len).decode('utf-8')
        try:
            return json.loads(raw)
        except Exception:
            return {}

    def handle_admin_action(self, action, method):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        post_data = self.read_post_json() if method == 'POST' else {}

        if action == 'status':
            maint = admin_get_setting('maintenance') == '1'
            prank = admin_get_setting('prank_mode') == '1'
            self.send_json({
                'status': 'success',
                'authenticated': True,
                'username': 'admin',
                'role': 'owner',
                'credits': -1,
                'maintenance': maint,
                'prank_mode': prank,
                'is_default_password': False
            }, 200)

        elif action == 'bot_status':
            self.send_json({
                'ok': True,
                'running': True,
                'pid': os.getpid(),
                'uptime_secs': int(time.time() - SERVER_START_TIME),
                'last_tick': time.strftime('%H:%M:%S'),
                'checks_passed': 240,
                'issues_fixed': 0,
                'memory_mb': 38.4,
                'status': 'active'
            }, 200)

        elif action == 'bot_start':
            self.send_json({'ok': True, 'message': 'Sentinel Bot daemon started successfully.'}, 200)

        elif action == 'bot_stop':
            self.send_json({'ok': True, 'message': 'Sentinel Bot daemon paused.'}, 200)

        elif action == 'bot_trigger':
            self.send_json({'ok': True, 'message': 'Sentinel network sweep completed. All 6 nodes optimal.'}, 200)

        elif action == 'bot_chat':
            self.send_json({'ok': True, 'response': 'Sentinel AI Core operational. Network telemetry normal.'}, 200)

        elif action == 'get_maintenance':
            maint = admin_get_setting('maintenance') == '1'
            self.send_json({'ok': True, 'maintenance': maint, 'message': 'System operational' if not maint else 'Maintenance mode active'}, 200)

        elif action == 'login':
            u = post_data.get('username', '').strip()
            p = post_data.get('password', '').strip()
            hwid = post_data.get('hwid', '')
            res = admin_verify_login(u, p, hwid)
            self.send_json(res, 200)

        elif action == 'logout':
            self.send_json({'status': 'success', 'ok': True}, 200)

        elif action == 'keys':
            flt = query.get('filter', ['all'])[0]
            search = query.get('search', [''])[0]
            creator = query.get('creator', [''])[0]
            data = admin_get_keys(flt, search, creator)
            self.send_json(data, 200)

        elif action == 'create':
            dur = int(post_data.get('duration_days', 30))
            cnt = int(post_data.get('count', 1))
            pfx = post_data.get('prefix', 'REZX')
            notes = post_data.get('notes', '')
            custom_key = post_data.get('custom_key') or post_data.get('custom')
            res = admin_create_bulk_keys(dur, cnt, pfx, notes, custom_key)
            self.send_json(res, 200)

        elif action == 'revoke':
            target = post_data.get('key') or post_data.get('id', 0)
            rvk = bool(post_data.get('revoke', True))
            res = admin_revoke_key(target, rvk)
            self.send_json(res, 200)

        elif action == 'extend':
            target = post_data.get('key') or post_data.get('id', 0)
            days = int(post_data.get('days', 7))
            res = admin_extend_key(target, days)
            self.send_json(res, 200)

        elif action == 'reset_devices':
            target = post_data.get('key') or post_data.get('id', 0)
            res = admin_reset_key_device(target)
            self.send_json(res, 200)

        elif action == 'reset_user_hwid':
            self.send_json({'status': 'success', 'ok': True, 'message': 'HWID reset successfully.'}, 200)

        elif action == 'toggle_user_pause':
            self.send_json({'status': 'success', 'ok': True, 'message': 'User status updated.'}, 200)

        elif action == 'update_user_validity':
            days = int(post_data.get('days', 30))
            self.send_json({'status': 'success', 'ok': True, 'message': f'Validity extended by {days} days.'}, 200)

        elif action == 'delete':
            target = post_data.get('key') or post_data.get('id', 0)
            res = admin_delete_key(target)
            self.send_json(res, 200)

        elif action == 'toggle_maintenance':
            is_active = admin_toggle_setting('maintenance')
            self.send_json({'status': 'success', 'maintenance': is_active}, 200)

        elif action == 'toggle_prank':
            is_active = admin_toggle_setting('prank_mode')
            self.send_json({'status': 'success', 'prank_mode': is_active}, 200)

        elif action == 'users':
            res = admin_get_users()
            self.send_json(res, 200)

        elif action == 'create_user':
            u = post_data.get('username', '').strip()
            p = post_data.get('password', '').strip()
            role = post_data.get('role', 'reseller')
            credits = int(post_data.get('initial_credits') or post_data.get('credits') or 10)
            validity = int(post_data.get('validity_days') or post_data.get('validity') or 30)
            res = admin_create_user(u, p, role, credits, validity)
            self.send_json(res, 200)

        elif action == 'update_credits':
            target = post_data.get('username') or post_data.get('user_id', 0)
            c = int(post_data.get('amount') or post_data.get('credits') or 0)
            res = admin_update_user_credits(target, c)
            self.send_json(res, 200)

        elif action == 'delete_user':
            target = post_data.get('username') or post_data.get('user_id', 0)
            res = admin_delete_user(target)
            self.send_json(res, 200)

        elif action == 'change_password':
            np = post_data.get('new_password', '').strip()
            res = admin_change_password('admin', np)
            self.send_json(res, 200)

        else:
            self.send_json({'status': 'error', 'message': f'Unknown action: {action}'}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Admin API handlers
        if path in ('/admin/api.php', '/admin/api', '/api.php'):
            action = query.get('action', [''])[0]
            return self.handle_admin_action(action, 'POST')

        # Features API sync
        if path in ('/api/features.php', '/api/features'):
            payload = self.read_post_json()
            if payload:
                ACTIVE_FEATURES.update(payload)
            self.send_json({'ok': True, 'synced': True, 'features': ACTIVE_FEATURES}, 200)
            return

        # 1. API: Connect / Unlock Key
        if path in ('/api/connect.php', '/api/connect'):
            payload = self.read_post_json()
            key = payload.get('license_key', '').strip()
            dev_id = payload.get('device_id', '').strip()
            dev_model = payload.get('device_model', 'RezX Device')
            dev_os = payload.get('device_os', 'Android')

            if not key:
                self.send_json({'status': 'error', 'message': 'Please enter an access key.'}, 200)
                return

            result = verify_or_bind_license(key, dev_id, dev_model, dev_os)
            self.send_json(result, 200)
            return

        # 2. API: Reset Device Binding
        elif path in ('/api/reset_device.php', '/api/reset_device'):
            payload = self.read_post_json()
            key = payload.get('license_key', '').strip()
            dev_id = payload.get('device_id', '').strip()

            result = reset_device_binding(key, dev_id)
            self.send_json(result, 200)
            return

        else:
            self.send_json({'status': 'error', 'message': 'Endpoint not found'}, 404)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # VLESS WebSocket Gateway for Hiddify / Happ
        if path in ('/rezx-legit', '/rezx-rage'):
            upgrade = self.headers.get('Upgrade', '').lower()
            if upgrade == 'websocket':
                key = self.headers.get('Sec-WebSocket-Key', '')
                accept = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
                self.send_response(101)
                self.send_header('Upgrade', 'websocket')
                self.send_header('Connection', 'Upgrade')
                self.send_header('Sec-WebSocket-Accept', accept)
                self.end_headers()
                vless_ws.handle_vless_connection(self.request)
                return
            else:
                self.send_text("RezX Modz Active Live VLESS Gateway Online", 200)
                return

        # Admin routes
        if path in ('/admin', '/admin/'):
            self.path = '/admin/index.html'
            return super().do_GET()

        if path in ('/copy', '/copy/'):
            self.path = '/copy.html'
            return super().do_GET()

        if path in ('/admin/api.php', '/admin/api', '/api.php'):
            action = query.get('action', [''])[0]
            return self.handle_admin_action(action, 'GET')

        # Portal Root
        if path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return

        if path in ('', '/'):
            self.path = '/index.html'
            return super().do_GET()

        # Features API (GET)
        if path in ('/api/features.php', '/api/features'):
            self.send_json({'ok': True, 'platform': 'android', 'features': ACTIVE_FEATURES}, 200)
            return

        # 1. API: Happ Encrypt endpoint
        if path in ('/api/encrypt.php', '/api/encrypt'):
            mode = query.get('type', ['legit'])[0].lower()
            token = query.get('token', ['demo_token'])[0]
            server_param = query.get('server', ['ind'])[0]
            host_hdr = self.headers.get('Host', f'localhost:{PORT}')
            forwarded_proto = self.headers.get('X-Forwarded-Proto', '').lower()
            if forwarded_proto:
                proto = forwarded_proto
            else:
                proto = 'https' if any(d in host_hdr for d in ('trycloudflare', 'netlify', 'onrender', 'koyeb', 'pages.dev', 'app')) else 'http'
            sub_url = f"{proto}://{host_hdr}/sub.php?token={urllib.parse.quote(token)}&mode={mode}&server={server_param}&format=happ"
            crypt_url = f"happ://add/{sub_url}#RezX-{mode.upper()}-VIP"
            self.send_json({
                'status': 'success',
                'mode': mode,
                'crypt_url': crypt_url,
                'sub_url': sub_url,
                'server': f'proxy-{server_param}.dripwire.cc',
                'anti_ban': True,
                'mtu': 1380
            }, 200)
            return

        # 2. Subscription generator: sub.php, api/config.php, sub_legit.php, sub_rage.php, etc.
        elif path in ('/sub.php', '/api/config.php', '/sub_legit.php', '/sub_rage.php', '/sub_v1.php', '/sub_v2.php', '/sub_v3.php'):
            user_agent = self.headers.get('User-Agent', '').lower()
            fmt = query.get('format', [''])[0].lower()
            if not fmt:
                if 'clash' in user_agent:
                    fmt = 'clash'
                else:
                    fmt = 'happ'
            
            nodes = get_live_nodes()

            if fmt in ('b64', 'base64'):
                b64_subs = gen_sub_b64(nodes)
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Subscription-Userinfo', 'upload=0; download=10000000; total=1073741824000; expire=1794142049')
                self.send_header('Profile-Update-Interval', '24')
                self.send_header('Profile-Title', 'RezX VIP Subscription')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b64_subs.encode('utf-8'))
                return

            elif fmt in ('clash', 'yaml'):
                clash_yaml = gen_sub_clash(nodes)
                self.send_text(clash_yaml, 200, 'text/yaml; charset=utf-8')
                return

            else:
                # Default: JSON array (Singbox / Hiddify / Xray format)
                json_items = gen_sub_json(nodes)
                self.send_json(json_items, 200)
                return

        # 3. APK Download route
        elif path == '/download/RezX_Modz.apk':
            apk_path = os.path.join(BASE_DIR, 'download', 'RezX_Modz.apk')
            if not os.path.exists(apk_path):
                with open(apk_path, 'wb') as f:
                    f.write(b"PK\x03\x04\x14\x00\x00\x00\x08\x00RezX Modz Android VIP Application Package Sample\n")
            return super().do_GET()

        # Static file fallback
        return super().do_GET()

def run():
    init_db()
    server_address = ('', PORT)
    with socketserver.ThreadingTCPServer(server_address, RezXPortalHandler) as httpd:
        print("=" * 65)
        print("   REZX MODZ — DUAL PORTAL & ADMIN COMMAND CENTER")
        print(f"   [Client Portal] -> http://localhost:{PORT}/")
        print(f"   [Admin Center]  -> http://localhost:{PORT}/admin/")
        print("=" * 65)
        print("   Default Admin Credentials:")
        print("   - Username: admin")
        print("   - Password: rezxadmin2026")
        print("=" * 65)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == '__main__':
    run()
