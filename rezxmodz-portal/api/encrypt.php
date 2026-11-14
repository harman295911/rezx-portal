<?php
// api/encrypt.php - RezX Modz Happ Crypt URL generator (Indian Server Non-Root Anti-Ban)
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$type  = strtolower($_GET['type'] ?? 'legit');
$token = $_GET['token'] ?? bin2hex(random_bytes(6));

if ($type === 'rage') {
    $server = 'delhi-rage.vip.rezxmodz.lol';
    $label = 'RezX-RAGE-INDIAN-VIP';
    $path = '%2Frezx-rage';
} else {
    $server = 'delhi.vip.rezxmodz.lol';
    $label = 'RezX-LEGIT-INDIAN-ANTIBAN';
    $path = '%2Frezx-legit';
}

$cryptUrl = "happ://crypt5/vless://rezx-vip-{$token}@{$server}:443?encryption=none&security=tls&sni=matrix.rezxmodz.lol&type=ws&host=matrix.rezxmodz.lol&path={$path}#{$label}";

echo json_encode([
    'status' => 'success',
    'mode' => $type,
    'crypt_url' => $cryptUrl,
    'server' => $server,
    'anti_ban' => true,
    'mtu' => 1380
], JSON_UNESCAPED_SLASHES);
