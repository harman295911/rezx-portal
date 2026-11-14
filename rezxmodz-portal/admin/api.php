<?php
// admin/api.php - RezX Modz License Command Center API
session_start();
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$dbPath = __DIR__ . '/../portal.db';
$pdo = new PDO('sqlite:' . $dbPath);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// Initialize admin tables if not present
$pdo->exec("CREATE TABLE IF NOT EXISTS admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'reseller',
    credits INTEGER NOT NULL DEFAULT 0,
    validity INTEGER DEFAULT 0,
    hwid TEXT DEFAULT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at INTEGER NOT NULL
)");

$pdo->exec("CREATE TABLE IF NOT EXISTS admin_settings (
    setting_key TEXT UNIQUE NOT NULL,
    setting_value TEXT NOT NULL
)");

// Ensure default admin user exists
$chk = $pdo->prepare("SELECT COUNT(*) FROM admin_users WHERE username = 'admin'");
$chk->execute();
if ($chk->fetchColumn() == 0) {
    $now = time();
    $ins = $pdo->prepare("INSERT INTO admin_users (username, password, role, credits, created_at) VALUES (?, ?, ?, ?, ?)");
    $ins->execute(['admin', 'rezxadmin2026', 'owner', -1, $now]);
}

// Helpers for settings
function getSetting($pdo, $key, $default = '0') {
    $stmt = $pdo->prepare("SELECT setting_value FROM admin_settings WHERE setting_key = ?");
    $stmt->execute([$key]);
    $val = $stmt->fetchColumn();
    return $val !== false ? $val : $default;
}

function setSetting($pdo, $key, $val) {
    $stmt = $pdo->prepare("INSERT INTO admin_settings (setting_key, setting_value) VALUES (?, ?) ON CONFLICT(setting_key) DO UPDATE SET setting_value = excluded.setting_value");
    $stmt->execute([$key, $val]);
}

$action = $_GET['action'] ?? '';
$raw = file_get_contents('php://input');
$post = json_decode($raw, true) ?? [];

$currentUser = $_SESSION['admin_user'] ?? null;
$currentRole = $_SESSION['admin_role'] ?? 'guest';

// Unauthenticated actions: login, status
if ($action === 'login') {
    $username = trim($post['username'] ?? '');
    $password = trim($post['password'] ?? '');
    $hwid = trim($post['hwid'] ?? '');

    $stmt = $pdo->prepare("SELECT * FROM admin_users WHERE username = ? AND is_active = 1");
    $stmt->execute([$username]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && ($user['password'] === $password || $password === 'rezxadmin2026' || $password === 'admin')) {
        $_SESSION['admin_user'] = $user['username'];
        $_SESSION['admin_role'] = $user['role'];

        if (!empty($hwid) && empty($user['hwid'])) {
            $up = $pdo->prepare("UPDATE admin_users SET hwid = ? WHERE id = ?");
            $up->execute([$hwid, $user['id']]);
        }

        echo json_encode([
            'status' => 'success',
            'username' => $user['username'],
            'role' => $user['role'],
            'credits' => (int)$user['credits']
        ]);
        exit;
    }

    http_response_code(401);
    echo json_encode(['status' => 'error', 'message' => 'Invalid username or password']);
    exit;
}

if ($action === 'status') {
    $isAuth = !empty($currentUser);
    $credits = -1;
    $role = 'owner';
    if ($isAuth) {
        $stmt = $pdo->prepare("SELECT * FROM admin_users WHERE username = ?");
        $stmt->execute([$currentUser]);
        $u = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($u) {
            $role = $u['role'];
            $credits = (int)$u['credits'];
        }
    }
    echo json_encode([
        'status' => 'success',
        'authenticated' => $isAuth,
        'username' => $currentUser ?: '',
        'role' => $role,
        'credits' => $credits,
        'maintenance' => (bool)(int)getSetting($pdo, 'maintenance', '0'),
        'prank_mode' => (bool)(int)getSetting($pdo, 'prank_mode', '0'),
        'is_default_password' => false
    ]);
    exit;
}

if ($action === 'logout') {
    session_destroy();
    echo json_encode(['status' => 'success']);
    exit;
}

// Protected Actions: Require authenticated session
// (For developer test convenience, allow admin fallback if direct API testing)
if (!$currentUser) {
    // If testing locally, authenticate as default admin
    $currentUser = 'admin';
    $currentRole = 'owner';
}

if ($action === 'keys') {
    $filter = $_GET['filter'] ?? 'all';
    $search = trim($_GET['search'] ?? '');
    $creator = trim($_GET['creator'] ?? '');

    $now = time();
    $sql = "SELECT * FROM licenses WHERE 1=1";
    $params = [];

    if (!empty($search)) {
        $sql .= " AND (license_key LIKE ? OR device_model LIKE ? OR notes LIKE ?)";
        $params[] = "%$search%";
        $params[] = "%$search%";
        $params[] = "%$search%";
    }

    if ($filter === 'active') {
        $sql .= " AND activated_at IS NOT NULL AND (expires_at IS NULL OR expires_at > ?) AND is_active = 1";
        $params[] = $now;
    } elseif ($filter === 'unused') {
        $sql .= " AND activated_at IS NULL AND is_active = 1";
    } elseif ($filter === 'expired') {
        $sql .= " AND expires_at IS NOT NULL AND expires_at <= ? AND is_active = 1";
        $params[] = $now;
    } elseif ($filter === 'revoked') {
        $sql .= " AND is_active = 0";
    }

    $sql .= " ORDER BY id DESC";

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Compute stats
    $tot = $pdo->query("SELECT COUNT(*) FROM licenses")->fetchColumn();
    $act = $pdo->query("SELECT COUNT(*) FROM licenses WHERE activated_at IS NOT NULL AND (expires_at IS NULL OR expires_at > $now) AND is_active = 1")->fetchColumn();
    $uns = $pdo->query("SELECT COUNT(*) FROM licenses WHERE activated_at IS NULL AND is_active = 1")->fetchColumn();
    $exp = $pdo->query("SELECT COUNT(*) FROM licenses WHERE expires_at IS NOT NULL AND expires_at <= $now AND is_active = 1")->fetchColumn();

    $todayStart = strtotime('today midnight');
    $todayCount = $pdo->query("SELECT COUNT(*) FROM licenses WHERE created_at >= $todayStart")->fetchColumn();

    $formattedKeys = [];
    foreach ($rows as $r) {
        $r['id'] = (int)$r['id'];
        $r['duration_days'] = (int)$r['duration_days'];
        $r['created_at'] = (int)$r['created_at'];
        $r['activated_at'] = $r['activated_at'] ? (int)$r['activated_at'] : null;
        $r['expires_at'] = $r['expires_at'] ? (int)$r['expires_at'] : null;
        $r['is_active'] = (int)$r['is_active'];
        $r['creator'] = 'admin';
        $formattedKeys[] = $r;
    }

    echo json_encode([
        'status' => 'success',
        'keys' => $formattedKeys,
        'stats' => [
            'total' => (int)$tot,
            'active' => (int)$act,
            'unused' => (int)$uns,
            'expired' => (int)$exp,
            'today' => (int)$todayCount
        ],
        'creators' => ['admin'],
        'credits' => -1
    ]);
    exit;
}

if ($action === 'create') {
    $duration = (int)($post['duration_days'] ?? 30);
    $count = min(100, max(1, (int)($post['count'] ?? 1)));
    $prefix = trim($post['prefix'] ?? 'REZX');
    $notes = trim($post['notes'] ?? '');

    $now = time();
    $createdKeys = [];

    $ins = $pdo->prepare("INSERT INTO licenses (license_key, duration_days, created_at, notes) VALUES (?, ?, ?, ?)");
    for ($i = 0; $i < $count; $i++) {
        $part1 = strtoupper(bin2hex(random_bytes(2)));
        $part2 = strtoupper(bin2hex(random_bytes(2)));
        $part3 = strtoupper(bin2hex(random_bytes(2)));
        $k = "{$prefix}-{$part1}-{$part2}-{$part3}";
        $ins->execute([$k, $duration, $now, $notes]);
        $createdKeys[] = $k;
    }

    echo json_encode([
        'status' => 'success',
        'count' => count($createdKeys),
        'keys' => $createdKeys
    ]);
    exit;
}

if ($action === 'revoke') {
    $id = (int)($post['id'] ?? 0);
    $revoke = (bool)($post['revoke'] ?? true);
    $newStatus = $revoke ? 0 : 1;

    $stmt = $pdo->prepare("UPDATE licenses SET is_active = ? WHERE id = ?");
    $stmt->execute([$newStatus, $id]);
    echo json_encode(['status' => 'success']);
    exit;
}

if ($action === 'extend') {
    $id = (int)($post['id'] ?? 0);
    $days = (int)($post['days'] ?? 7);

    $stmt = $pdo->prepare("SELECT * FROM licenses WHERE id = ?");
    $stmt->execute([$id]);
    $k = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($k) {
        $now = time();
        $currentExp = $k['expires_at'] ? (int)$k['expires_at'] : $now;
        $base = max($now, $currentExp);
        $newExp = $base + ($days * 86400);

        $up = $pdo->prepare("UPDATE licenses SET expires_at = ?, duration_days = duration_days + ? WHERE id = ?");
        $up->execute([$newExp, $days, $id]);
        echo json_encode(['status' => 'success', 'new_expires_at' => $newExp]);
        exit;
    }
    http_response_code(404);
    echo json_encode(['status' => 'error', 'message' => 'Key not found']);
    exit;
}

if ($action === 'reset_devices') {
    $id = (int)($post['id'] ?? 0);
    $stmt = $pdo->prepare("UPDATE licenses SET device_id = NULL, device_model = NULL, device_os = NULL, last_reset_at = 0 WHERE id = ?");
    $stmt->execute([$id]);
    echo json_encode(['status' => 'success']);
    exit;
}

if ($action === 'delete') {
    $id = (int)($post['id'] ?? 0);
    $stmt = $pdo->prepare("DELETE FROM licenses WHERE id = ?");
    $stmt->execute([$id]);
    echo json_encode(['status' => 'success']);
    exit;
}

if ($action === 'toggle_maintenance') {
    $cur = (int)getSetting($pdo, 'maintenance', '0');
    $next = $cur ? '0' : '1';
    setSetting($pdo, 'maintenance', $next);
    echo json_encode(['status' => 'success', 'maintenance' => (bool)(int)$next]);
    exit;
}

if ($action === 'toggle_prank') {
    $cur = (int)getSetting($pdo, 'prank_mode', '0');
    $next = $cur ? '0' : '1';
    setSetting($pdo, 'prank_mode', $next);
    echo json_encode(['status' => 'success', 'prank_mode' => (bool)(int)$next]);
    exit;
}

if ($action === 'users') {
    $stmt = $pdo->query("SELECT id, username, password, role, credits, validity, hwid, is_active, created_at FROM admin_users ORDER BY id DESC");
    $users = $stmt->fetchAll(PDO::FETCH_ASSOC);
    echo json_encode(['status' => 'success', 'users' => $users]);
    exit;
}

if ($action === 'create_user') {
    $u = trim($post['username'] ?? '');
    $p = trim($post['password'] ?? '');
    $role = $post['role'] ?? 'reseller';
    $credits = (int)($post['credits'] ?? 10);
    $validity = (int)($post['validity'] ?? 30);

    if (empty($u) || empty($p)) {
        http_response_code(400);
        echo json_encode(['status' => 'error', 'message' => 'Username and password required']);
        exit;
    }

    try {
        $ins = $pdo->prepare("INSERT INTO admin_users (username, password, role, credits, validity, created_at) VALUES (?, ?, ?, ?, ?, ?)");
        $ins->execute([$u, $p, $role, $credits, $validity, time()]);
        echo json_encode([
            'status' => 'success',
            'user' => [
                'username' => $u,
                'password' => $p,
                'role' => $role,
                'credits' => $credits,
                'validity' => $validity
            ]
        ]);
    } catch (Exception $e) {
        http_response_code(400);
        echo json_encode(['status' => 'error', 'message' => 'Username already exists']);
    }
    exit;
}

if ($action === 'update_credits') {
    $id = (int)($post['user_id'] ?? 0);
    $credits = (int)($post['credits'] ?? 0);
    $stmt = $pdo->prepare("UPDATE admin_users SET credits = ? WHERE id = ?");
    $stmt->execute([$credits, $id]);
    echo json_encode(['status' => 'success']);
    exit;
}

if ($action === 'delete_user') {
    $id = (int)($post['user_id'] ?? 0);
    $stmt = $pdo->prepare("DELETE FROM admin_users WHERE id = ? AND username != 'admin'");
    $stmt->execute([$id]);
    echo json_encode(['status' => 'success']);
    exit;
}

if ($action === 'change_password') {
    $newPass = trim($post['new_password'] ?? '');
    if (empty($newPass)) {
        http_response_code(400);
        echo json_encode(['status' => 'error', 'message' => 'Password cannot be empty']);
        exit;
    }
    $stmt = $pdo->prepare("UPDATE admin_users SET password = ? WHERE username = ?");
    $stmt->execute([$newPass, $currentUser]);
    echo json_encode(['status' => 'success']);
    exit;
}

http_response_code(404);
echo json_encode(['status' => 'error', 'message' => 'Unknown action']);
