<?php
// api/connect.php - RezX Modz Strict Connect & Verification Endpoint
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$raw = file_get_contents('php://input');
$data = json_decode($raw, true) ?? [];

$licenseKey = strtoupper(trim($data['license_key'] ?? ''));
$deviceId = trim($data['device_id'] ?? '');
$deviceModel = trim($data['device_model'] ?? 'RezX Phone');
$deviceOs = trim($data['device_os'] ?? 'Android');

if (empty($licenseKey)) {
    echo json_encode(['status' => 'error', 'message' => 'Please enter your access key.']);
    exit;
}

$dbFile = __DIR__ . '/../portal.db';
try {
    $pdo = new PDO('sqlite:' . $dbFile);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Look up license in database - MUST be created by Admin
    $stmt = $pdo->prepare("SELECT * FROM licenses WHERE license_key = ?");
    $stmt->execute([$licenseKey]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    $now = time();

    // STRICT CHECK: Reject if key does not exist
    if (!$row) {
        echo json_encode([
            'status' => 'error',
            'message' => 'Invalid access key. Key was not found in the system. Contact your seller.'
        ]);
        exit;
    }

    // STRICT CHECK: Reject if suspended/revoked
    if (isset($row['is_active']) && (int)$row['is_active'] === 0) {
        echo json_encode([
            'status' => 'error',
            'message' => 'This access key has been suspended or revoked by Admin.'
        ]);
        exit;
    }

    // Check expiration
    if (!empty($row['expires_at']) && $now > (int)$row['expires_at']) {
        echo json_encode([
            'status' => 'error',
            'message' => 'Access key has expired.'
        ]);
        exit;
    }

    // Check device lock
    if (!empty($row['device_id']) && $row['device_id'] !== $deviceId) {
        echo json_encode([
            'status' => 'error',
            'message' => 'Key is locked to another device (' . ($row['device_model'] ?: 'Another Phone') . '). Reset device binding in Manage tab first.'
        ]);
        exit;
    }

    // First time activation: bind device and calculate expiry
    if (empty($row['activated_at'])) {
        $duration = (int)($row['duration_days'] ?: 30);
        $expires = $now + ($duration * 86400);
        $up = $pdo->prepare("UPDATE licenses SET activated_at = ?, expires_at = ?, device_id = ?, device_model = ?, device_os = ? WHERE license_key = ?");
        $up->execute([$now, $expires, $deviceId, $deviceModel, $deviceOs, $licenseKey]);
        $row['expires_at'] = $expires;
    } else {
        if (empty($row['device_id'])) {
            $up = $pdo->prepare("UPDATE licenses SET device_id = ?, device_model = ?, device_os = ? WHERE license_key = ?");
            $up->execute([$deviceId, $deviceModel, $deviceOs, $licenseKey]);
        }
    }

    $token = bin2hex(random_bytes(8));
    $encryptedLink = "vless://{$licenseKey}@matrix.rezxmodz.lol:443?security=reality#INDIA%20RezX%2001%20VIP";

    $lastReset = (int)($row['last_reset_at'] ?? 0);
    $canReset = ($now - $lastReset) >= (7 * 86400);
    $resetCooldown = max(0, (7 * 86400) - ($now - $lastReset));

    echo json_encode([
        'status' => 'success',
        'key' => $licenseKey,
        'token' => $token,
        'expires_at' => date('Y-m-d H:i:s', $row['expires_at']),
        'expires_timestamp' => (int)$row['expires_at'],
        'nodes_count' => 4,
        'encrypted_link' => $encryptedLink,
        'subscription_url' => "/sub_legit.php?token={$token}",
        'bound_device' => [
            'device_id' => $deviceId,
            'device_name' => "{$deviceModel} · {$deviceOs}"
        ],
        'can_reset' => $canReset,
        'reset_cooldown_left' => $resetCooldown
    ]);

} catch (Exception $e) {
    echo json_encode([
        'status' => 'error',
        'message' => 'Server database error. Please try again later.'
    ]);
}
