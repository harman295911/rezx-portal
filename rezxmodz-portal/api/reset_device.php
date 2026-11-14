<?php
// api/reset_device.php - RezX Modz Device Reset for PHP environments
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

$licenseKey = trim($data['license_key'] ?? '');
$deviceId = trim($data['device_id'] ?? '');

if (empty($licenseKey)) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'License key required']);
    exit;
}

$dbFile = __DIR__ . '/../portal.db';
try {
    $pdo = new PDO('sqlite:' . $dbFile);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->prepare("SELECT * FROM licenses WHERE license_key = ?");
    $stmt->execute([$licenseKey]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$row) {
        http_response_code(404);
        echo json_encode(['status' => 'error', 'message' => 'Key not found']);
        exit;
    }

    $now = time();
    $lastReset = (int)($row['last_reset_at'] ?? 0);
    $cooldown = 7 * 86400;

    if (($now - $lastReset) < $cooldown) {
        $left = $cooldown - ($now - $lastReset);
        http_response_code(429);
        echo json_encode([
            'status' => 'error',
            'message' => 'Reset on cooldown (7 days)',
            'seconds_left' => $left
        ]);
        exit;
    }

    $up = $pdo->prepare("UPDATE licenses SET device_id = NULL, device_model = NULL, device_os = NULL, last_reset_at = ? WHERE license_key = ?");
    $up->execute([$now, $licenseKey]);

    echo json_encode(['status' => 'success', 'message' => 'Device unlinked successfully']);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['status' => 'error', 'message' => 'Database error']);
}
