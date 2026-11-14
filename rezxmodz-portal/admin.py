# admin.py - RezX Modz Operator CLI Management Tool
import sys
import argparse
import time
from database import init_db, create_license, get_db, reset_device_binding

def banner():
    print("""
===========================================================
   REZX MODZ — OPERATOR MANAGEMENT CLI (v1.7)
===========================================================
    """)

def list_keys():
    init_db()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM licenses ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("[!] No keys generated yet.")
        return

    print(f"{'ID':<4} {'KEY':<24} {'DAYS':<6} {'STATUS':<10} {'BOUND DEVICE':<25} {'EXPIRES AT'}")
    print("-" * 90)
    now = int(time.time())
    for r in rows:
        key = r['license_key']
        days = r['duration_days']
        exp = r['expires_at']
        dev = r['device_model'] or (r['device_id'][:12] + '...' if r['device_id'] else 'None')
        if not r['is_active']:
            status = "SUSPENDED"
        elif exp and now > exp:
            status = "EXPIRED"
        elif r['activated_at']:
            status = "ACTIVE"
        else:
            status = "UNUSED"

        exp_str = time.strftime('%Y-%m-%d', time.gmtime(exp)) if exp else "Unused"
        print(f"{r['id']:<4} {key:<24} {days:<6} {status:<10} {dev:<25} {exp_str}")
    print("-" * 90)

def generate_key(days, count=1, notes=""):
    init_db()
    print(f"[*] Generating {count} key(s) with {days} days duration...")
    for i in range(count):
        res = create_license(duration_days=days, notes=notes)
        if res.get('success'):
            print(f" [+] Generated Key: {res['key']} ({days} Days)")
        else:
            print(f" [-] Failed: {res.get('message')}")

def reset_device(key):
    init_db()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE licenses SET device_id = NULL, device_model = NULL, device_os = NULL WHERE license_key = ?", (key,))
    if cur.rowcount > 0:
        conn.commit()
        print(f"[+] Device binding for key {key} successfully cleared.")
    else:
        print(f"[-] Key {key} not found.")
    conn.close()

def main():
    banner()
    parser = argparse.ArgumentParser(description="RezX Modz Operator CLI")
    parser.add_argument("--list", action="store_true", help="List all generated licenses")
    parser.add_argument("--gen", type=int, metavar="DAYS", help="Generate a new key with specified days (e.g. 30)")
    parser.add_argument("--count", type=int, default=1, help="Number of keys to generate (default 1)")
    parser.add_argument("--notes", type=str, default="", help="Note for key")
    parser.add_argument("--reset", type=str, metavar="KEY", help="Force reset device lock on a key")

    if len(sys.argv) == 1:
        parser.print_help()
        print("\nQuick Shortcuts:")
        print("  python admin.py --list")
        print("  python admin.py --gen 30 --count 5")
        print("  python admin.py --reset REZX-XXXX-XXXX-XXXX")
        return

    args = parser.parse_args()

    if args.list:
        list_keys()
    elif args.gen is not None:
        generate_key(args.gen, args.count, args.notes)
    elif args.reset:
        reset_device(args.reset)

if __name__ == "__main__":
    main()
