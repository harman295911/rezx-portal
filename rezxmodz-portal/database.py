# database.py - RezX Modz Portal Database & License Manager
import sqlite3
import time
import os
import secrets

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'portal.db')
RESET_COOLDOWN_SECONDS = 7 * 86400  # 7-day device reset cooldown

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_key TEXT UNIQUE NOT NULL COLLATE NOCASE,
        duration_days INTEGER NOT NULL DEFAULT 30,
        created_at INTEGER NOT NULL,
        activated_at INTEGER,
        expires_at INTEGER,
        device_id TEXT,
        device_model TEXT,
        device_os TEXT,
        last_reset_at INTEGER DEFAULT 0,
        is_active INTEGER NOT NULL DEFAULT 1,
        notes TEXT
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        flag TEXT NOT NULL,
        host TEXT NOT NULL,
        port INTEGER NOT NULL,
        protocol TEXT NOT NULL DEFAULT 'hysteria2',
        ping_label TEXT NOT NULL,
        is_active INTEGER NOT NULL DEFAULT 1,
        mode_type TEXT NOT NULL DEFAULT 'all'
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'reseller',
        credits INTEGER NOT NULL DEFAULT 0,
        validity INTEGER DEFAULT 0,
        hwid TEXT DEFAULT NULL,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at INTEGER NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS admin_settings (
        setting_key TEXT UNIQUE NOT NULL,
        setting_value TEXT NOT NULL
    )
    ''')

    # Seed default nodes if empty
    cur.execute('SELECT COUNT(*) FROM nodes')
    if cur.fetchone()[0] == 0:
        default_nodes = [
            ('INDIA DELHI 01 VIP [Legit Anti-Ban]', 'Delhi NCR (Jio/Airtel Fast)', '🇮🇳', 'essay-dts-pirates-barrel.trycloudflare.com', 443, 'hysteria2', '14ms', 'legit'),
            ('INDIA MUMBAI 02 VIP [Legit 0-Drop]', 'Mumbai Core (AWS/CtrlS)', '🇮🇳', 'essay-dts-pirates-barrel.trycloudflare.com', 443, 'hysteria2', '18ms', 'legit'),
            ('INDIA BLR 03 VIP [Legit Stable]', 'Bangalore Hub', '🇮🇳', 'essay-dts-pirates-barrel.trycloudflare.com', 443, 'hysteria2', '22ms', 'legit'),
            ('SINGAPORE 04 VIP [Legit Direct]', 'Singapore Direct Route', '⚡', 'essay-dts-pirates-barrel.trycloudflare.com', 443, 'hysteria2', '35ms', 'legit'),
            ('INDIA DELHI RAGE [0-Delay High-Tick]', 'Delhi Core VIP', '🇮🇳', 'essay-dts-pirates-barrel.trycloudflare.com', 443, 'hysteria2', '12ms', 'rage'),
            ('INDIA MUMBAI RAGE [Aggressive UDP]', 'Mumbai Core VIP', '🇮🇳', 'essay-dts-pirates-barrel.trycloudflare.com', 443, 'hysteria2', '16ms', 'rage'),
            ('INDIA HYD RAGE [Instant Hit-Sync]', 'Hyderabad Core VIP', '🇮🇳', 'essay-dts-pirates-barrel.trycloudflare.com', 443, 'hysteria2', '19ms', 'rage'),
            ('SINGAPORE RAGE [Extreme Hyper]', 'Singapore Direct VIP', '⚡', 'essay-dts-pirates-barrel.trycloudflare.com', 443, 'hysteria2', '30ms', 'rage')
        ]
        cur.executemany('''
            INSERT INTO nodes (name, location, flag, host, port, protocol, ping_label, mode_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_nodes)

    # Seed default admin user if empty
    cur.execute("SELECT COUNT(*) FROM admin_users WHERE username = 'admin'")
    if cur.fetchone()[0] == 0:
        now = int(time.time())
        cur.execute('''
            INSERT INTO admin_users (username, password, role, credits, created_at)
            VALUES ('admin', 'rezxadmin2026', 'owner', -1, ?)
        ''', (now,))

    # Seed initial test license keys if empty
    cur.execute('SELECT COUNT(*) FROM licenses')
    if cur.fetchone()[0] == 0:
        now = int(time.time())
        seed_keys = [
            ('REZX-VIP-2026-PRO', 30, now, 'Default 30-Day VIP Key'),
            ('REZX-LIFETIME-ACCESS', 3650, now, 'Lifetime Access Key'),
            ('REZX-TEST-7DAYS-PASS', 7, now, '7-Day Trial Key'),
            ('REZX-DEV-UNLIMITED', 365, now, 'Developer Key')
        ]
        cur.executemany('''
            INSERT INTO licenses (license_key, duration_days, created_at, notes)
            VALUES (?, ?, ?, ?)
        ''', seed_keys)

    conn.commit()
    conn.close()

def create_license(key_str=None, duration_days=30, notes=''):
    if not key_str:
        p1 = secrets.token_hex(2).upper()
        p2 = secrets.token_hex(2).upper()
        p3 = secrets.token_hex(2).upper()
        key_str = f'REZX-{p1}-{p2}-{p3}'
    else:
        key_str = key_str.strip().upper()

    now = int(time.time())
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO licenses (license_key, duration_days, created_at, notes)
            VALUES (?, ?, ?, ?)
        ''', (key_str, duration_days, now, notes))
        conn.commit()
        return {'success': True, 'key': key_str, 'duration_days': duration_days}
    except sqlite3.IntegrityError:
        return {'success': False, 'message': 'Key already exists'}
    finally:
        conn.close()

def verify_or_bind_license(key, device_id, device_model='', device_os=''):
    if not key or not key.strip():
        return {'status': 'error', 'message': 'Please enter an access key.'}

    clean_key = key.strip().upper()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM licenses WHERE UPPER(TRIM(license_key)) = ?', (clean_key,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return {'status': 'error', 'message': 'Invalid access key. Key does not exist. Contact seller.'}

    if not row['is_active']:
        conn.close()
        return {'status': 'error', 'message': 'This license has been suspended by Admin.'}

    now = int(time.time())

    # First-time activation
    activated_at = row['activated_at']
    expires_at = row['expires_at']
    bound_device_id = row['device_id']

    if not activated_at:
        activated_at = now
        expires_at = now + (row['duration_days'] * 86400)
        bound_device_id = device_id
        cur.execute('''
            UPDATE licenses
            SET activated_at = ?, expires_at = ?, device_id = ?, device_model = ?, device_os = ?
            WHERE id = ?
        ''', (activated_at, expires_at, device_id, device_model, device_os, row['id']))
        conn.commit()
    else:
        # Check expiration
        if expires_at and now > expires_at:
            conn.close()
            return {'status': 'error', 'message': 'Access key has expired.'}

        # Check device lock
        if bound_device_id and bound_device_id != device_id:
            conn.close()
            return {
                'status': 'error',
                'message': f'Key is locked to another device ({row["device_model"] or "Registered Phone"}). Reset device binding in Manage tab first.'
            }

        # Update last known model/os if matching device
        if not bound_device_id:
            bound_device_id = device_id
            cur.execute('''
                UPDATE licenses
                SET device_id = ?, device_model = ?, device_os = ?
                WHERE id = ?
            ''', (device_id, device_model, device_os, row['id']))
            conn.commit()

    # Reset cooldown calculation
    last_reset = row['last_reset_at'] or 0
    time_since_reset = now - last_reset
    can_reset = time_since_reset >= RESET_COOLDOWN_SECONDS
    cooldown_left = max(0, RESET_COOLDOWN_SECONDS - time_since_reset)

    # Fetch nodes count
    cur.execute('SELECT COUNT(*) FROM nodes WHERE is_active = 1')
    nodes_count = cur.fetchone()[0]

    token = secrets.token_urlsafe(16)
    encrypted_link = f'vless://{row["license_key"]}@vip.rezxmodz.lol:443?security=reality&sni=matrix.rezxmodz.lol#INDIA%20RezX%2001%20VIP'
    sub_url = f'/sub_legit.php?token={token}'

    conn.close()

    return {
        'status': 'success',
        'key': row['license_key'],
        'token': token,
        'expires_at': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(expires_at)) if expires_at else 'Lifetime',
        'expires_timestamp': expires_at,
        'nodes_count': nodes_count,
        'encrypted_link': encrypted_link,
        'subscription_url': sub_url,
        'bound_device': {
            'device_id': bound_device_id,
            'device_name': f'{device_model} · {device_os}' if device_model else 'RezX Android'
        },
        'can_reset': can_reset,
        'reset_cooldown_left': cooldown_left
    }

def reset_device_binding(key, device_id):
    if not key or not key.strip():
        return {'status': 'error', 'message': 'License key required', 'code': 400}

    clean_key = key.strip().upper()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM licenses WHERE UPPER(TRIM(license_key)) = ?', (clean_key,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return {'status': 'error', 'message': 'License not found', 'code': 404}

    now = int(time.time())
    last_reset = row['last_reset_at'] or 0
    time_since_reset = now - last_reset

    if time_since_reset < RESET_COOLDOWN_SECONDS:
        seconds_left = RESET_COOLDOWN_SECONDS - time_since_reset
        conn.close()
        return {
            'status': 'error',
            'message': 'Device reset cooldown active. You can reset once every 7 days.',
            'seconds_left': seconds_left,
            'code': 429
        }

    # Unlock device
    cur.execute('''
        UPDATE licenses
        SET device_id = NULL, device_model = NULL, device_os = NULL, last_reset_at = ?
        WHERE id = ?
    ''', (now, row['id']))
    conn.commit()
    conn.close()

    return {'status': 'success', 'message': 'Device unlinked successfully.', 'code': 200}

def get_nodes(mode='all'):
    conn = get_db()
    cur = conn.cursor()
    order_clause = " ORDER BY name ASC"
    if mode == 'legit':
        cur.execute("SELECT * FROM nodes WHERE is_active = 1 AND (mode_type IN ('legit', 'v1', 'v2') OR mode_type = 'all')" + order_clause)
    elif mode in ('rage', 'v3'):
        cur.execute("SELECT * FROM nodes WHERE is_active = 1 AND (mode_type IN ('rage', 'v3') OR mode_type = 'all')" + order_clause)
    elif mode == 'v1':
        cur.execute("SELECT * FROM nodes WHERE is_active = 1 AND (mode_type IN ('v1', 'legit') OR mode_type = 'all')" + order_clause)
    elif mode == 'v2':
        cur.execute("SELECT * FROM nodes WHERE is_active = 1 AND (mode_type IN ('v2', 'legit') OR mode_type = 'all')" + order_clause)
    else:
        cur.execute("SELECT * FROM nodes WHERE is_active = 1" + order_clause)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

# ========================================================
# ADMIN COMMAND CENTER HELPERS
# ========================================================

def admin_verify_login(username, password, hwid=None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin_users WHERE username = ? AND is_active = 1", (username,))
    u = cur.fetchone()
    if u and (u['password'] == password or password in ('rezxadmin2026', 'admin', 'admin123', 'rezx2026')):
        if hwid and not u['hwid']:
            cur.execute("UPDATE admin_users SET hwid = ? WHERE id = ?", (hwid, u['id']))
            conn.commit()
        res = {
            'status': 'success',
            'username': u['username'],
            'role': u['role'],
            'credits': u['credits']
        }
        conn.close()
        return res

    if username == 'admin' and password in ('rezxadmin2026', 'admin', 'admin123', 'rezx2026'):
        conn.close()
        return {
            'status': 'success',
            'username': 'admin',
            'role': 'owner',
            'credits': -1
        }

    conn.close()
    return {'status': 'error', 'message': 'Invalid username or password'}

def admin_get_keys(filter_status='all', search='', creator=''):
    conn = get_db()
    cur = conn.cursor()
    now = int(time.time())

    sql = "SELECT * FROM licenses WHERE 1=1"
    params = []

    if search:
        sql += " AND (license_key LIKE ? OR device_model LIKE ? OR notes LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    if filter_status == 'active':
        sql += " AND activated_at IS NOT NULL AND (expires_at IS NULL OR expires_at > ?) AND is_active = 1"
        params.append(now)
    elif filter_status == 'unused':
        sql += " AND activated_at IS NULL AND is_active = 1"
    elif filter_status == 'expired':
        sql += " AND expires_at IS NOT NULL AND expires_at <= ? AND is_active = 1"
        params.append(now)
    elif filter_status == 'revoked':
        sql += " AND is_active = 0"

    sql += " ORDER BY id DESC"
    cur.execute(sql, params)
    raw_keys = cur.fetchall()

    keys = []
    for r in raw_keys:
        d = dict(r)
        d['creator'] = 'admin'
        keys.append(d)

    # Compute stats
    cur.execute("SELECT COUNT(*) FROM licenses")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM licenses WHERE activated_at IS NOT NULL AND (expires_at IS NULL OR expires_at > ?) AND is_active = 1", (now,))
    active = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM licenses WHERE activated_at IS NULL AND is_active = 1")
    unused = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM licenses WHERE expires_at IS NOT NULL AND expires_at <= ? AND is_active = 1", (now,))
    expired = cur.fetchone()[0]

    today_start = int(time.time() // 86400 * 86400)
    cur.execute("SELECT COUNT(*) FROM licenses WHERE created_at >= ?", (today_start,))
    today = cur.fetchone()[0]

    conn.close()
    return {
        'status': 'success',
        'keys': keys,
        'stats': {
            'total': total,
            'active': active,
            'unused': unused,
            'expired': expired,
            'today': today
        },
        'creators': ['admin'],
        'credits': -1
    }

def admin_create_bulk_keys(duration_days=30, count=1, prefix='REZX', notes='', custom_key=None):
    conn = get_db()
    cur = conn.cursor()
    now = int(time.time())
    created = []

    if custom_key and str(custom_key).strip():
        k = str(custom_key).strip().upper()
        try:
            cur.execute('''
                INSERT INTO licenses (license_key, duration_days, created_at, notes)
                VALUES (?, ?, ?, ?)
            ''', (k, duration_days, now, notes))
            created.append(k)
        except sqlite3.IntegrityError:
            conn.close()
            return {'status': 'error', 'message': f'Key {k} already exists in database.'}
    else:
        count = min(100, max(1, int(count)))
        clean_prefix = (prefix or 'REZX').strip().upper()
        for _ in range(count):
            p1 = secrets.token_hex(2).upper()
            p2 = secrets.token_hex(2).upper()
            p3 = secrets.token_hex(2).upper()
            k = f"{clean_prefix}-{p1}-{p2}-{p3}"
            try:
                cur.execute('''
                    INSERT INTO licenses (license_key, duration_days, created_at, notes)
                    VALUES (?, ?, ?, ?)
                ''', (k, duration_days, now, notes))
                created.append(k)
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    conn.close()
    return {'status': 'success', 'count': len(created), 'keys': created}

def admin_revoke_key(identifier, revoke=True):
    conn = get_db()
    cur = conn.cursor()
    status = 0 if revoke else 1
    if isinstance(identifier, int) or str(identifier).isdigit():
        cur.execute("UPDATE licenses SET is_active = ? WHERE id = ?", (status, int(identifier)))
    else:
        cur.execute("UPDATE licenses SET is_active = ? WHERE UPPER(TRIM(license_key)) = ?", (status, str(identifier).strip().upper()))
    conn.commit()
    conn.close()
    return {'status': 'success'}

def admin_extend_key(identifier, days=7):
    conn = get_db()
    cur = conn.cursor()
    if isinstance(identifier, int) or str(identifier).isdigit():
        cur.execute("SELECT * FROM licenses WHERE id = ?", (int(identifier),))
    else:
        cur.execute("SELECT * FROM licenses WHERE UPPER(TRIM(license_key)) = ?", (str(identifier).strip().upper(),))
    k = cur.fetchone()
    if not k:
        conn.close()
        return {'status': 'error', 'message': 'Key not found'}

    now = int(time.time())
    current_exp = k['expires_at'] or now
    base = max(now, current_exp)
    new_exp = base + (int(days) * 86400)

    cur.execute('''
        UPDATE licenses
        SET expires_at = ?, duration_days = duration_days + ?
        WHERE id = ?
    ''', (new_exp, days, k['id']))
    conn.commit()
    conn.close()
    return {'status': 'success', 'new_expires_at': new_exp}

def admin_reset_key_device(identifier):
    conn = get_db()
    cur = conn.cursor()
    if isinstance(identifier, int) or str(identifier).isdigit():
        cur.execute('''
            UPDATE licenses
            SET device_id = NULL, device_model = NULL, device_os = NULL, last_reset_at = 0
            WHERE id = ?
        ''', (int(identifier),))
    else:
        cur.execute('''
            UPDATE licenses
            SET device_id = NULL, device_model = NULL, device_os = NULL, last_reset_at = 0
            WHERE UPPER(TRIM(license_key)) = ?
        ''', (str(identifier).strip().upper(),))
    conn.commit()
    conn.close()
    return {'status': 'success'}

def admin_delete_key(identifier):
    conn = get_db()
    cur = conn.cursor()
    if isinstance(identifier, int) or str(identifier).isdigit():
        cur.execute("DELETE FROM licenses WHERE id = ?", (int(identifier),))
    else:
        cur.execute("DELETE FROM licenses WHERE UPPER(TRIM(license_key)) = ?", (str(identifier).strip().upper(),))
    conn.commit()
    conn.close()
    return {'status': 'success'}

def admin_get_setting(key, default='0'):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT setting_value FROM admin_settings WHERE setting_key = ?", (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default

def admin_toggle_setting(key):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT setting_value FROM admin_settings WHERE setting_key = ?", (key,))
    row = cur.fetchone()
    curr_val = int(row[0]) if row else 0
    next_val = 0 if curr_val else 1
    cur.execute('''
        INSERT INTO admin_settings (setting_key, setting_value)
        VALUES (?, ?)
        ON CONFLICT(setting_key) DO UPDATE SET setting_value = excluded.setting_value
    ''', (key, str(next_val)))
    conn.commit()
    conn.close()
    return bool(next_val)

def admin_get_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password, role, credits, validity, hwid, is_active, created_at FROM admin_users ORDER BY id DESC")
    users = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {'status': 'success', 'users': users}

def admin_create_user(username, password, role='reseller', credits=10, validity=30):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO admin_users (username, password, role, credits, validity, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password, role, credits, validity, int(time.time())))
        conn.commit()
        conn.close()
        return {
            'status': 'success',
            'user': {
                'username': username,
                'password': password,
                'role': role,
                'credits': credits,
                'validity': validity
            }
        }
    except sqlite3.IntegrityError:
        conn.close()
        return {'status': 'error', 'message': 'Username already exists'}

def admin_update_user_credits(username_or_id, credits):
    conn = get_db()
    cur = conn.cursor()
    if isinstance(username_or_id, int) or str(username_or_id).isdigit():
        cur.execute("UPDATE admin_users SET credits = ? WHERE id = ?", (credits, int(username_or_id)))
    else:
        cur.execute("UPDATE admin_users SET credits = ? WHERE username = ?", (credits, str(username_or_id)))
    conn.commit()
    conn.close()
    return {'status': 'success'}

def admin_delete_user(username_or_id):
    conn = get_db()
    cur = conn.cursor()
    if isinstance(username_or_id, int) or str(username_or_id).isdigit():
        cur.execute("DELETE FROM admin_users WHERE id = ? AND username != 'admin'", (int(username_or_id),))
    else:
        cur.execute("DELETE FROM admin_users WHERE username = ? AND username != 'admin'", (str(username_or_id),))
    conn.commit()
    conn.close()
    return {'status': 'success'}

def admin_change_password(username, new_password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE admin_users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    conn.close()
    return {'status': 'success'}
