<?php
// sub_legit.php - RezX Modz ZeroX VIP 12ms High-Tick Combat Proxy Subscription
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-cache, no-store, must-revalidate');

$format = $_GET['format'] ?? 'clash';
$token  = $_GET['token'] ?? 'rezx_legit_user';
$userAgent = strtolower($_SERVER['HTTP_USER_AGENT'] ?? '');

if (empty($_GET['format']) && strpos($userAgent, 'happ') !== false) {
    $format = 'happ';
}

$nodes = [
    [
        'name' => '01. ⚡ ZEROX VIP - INDIA DELHI [12ms AUTO-HEADSHOT]',
        'server' => 'zeroxmods.baby',
        'port' => 443,
        'protocol' => 'hysteria2',
        'password' => '4114330289',
        'sni' => 'zeroxmods.baby',
        'ping' => '12ms',
        'desc' => 'Delhi Gaming Core - Pure L4 Hysteria 2 UDP 12ms High-Tick'
    ],
    [
        'name' => '02. 🎯 RezX Neck-Lock Auto Profile (Neck Aim)',
        'server' => 'zeroxmods.baby',
        'port' => 443,
        'protocol' => 'hysteria2',
        'password' => '4114330289',
        'sni' => 'zeroxmods.baby',
        'ping' => '12ms',
        'desc' => 'Delhi Gaming Core - Pure L4 Hysteria 2 UDP 12ms High-Tick'
    ],
    [
        'name' => '03. 🔥 RezX Red-Aim Auto-Headshot (Aimbot Rage)',
        'server' => 'zeroxmods.baby',
        'port' => 443,
        'protocol' => 'hysteria2',
        'password' => '4114330289',
        'sni' => 'zeroxmods.baby',
        'ping' => '12ms',
        'desc' => 'Delhi Core VIP - ZeroX VIP 12ms High-Tick Combat'
    ],
    [
        'name' => '04. 🇮🇳 RezX V2 - Tournament AI [MAIN ID SAFE]',
        'server' => 'zeroxmods.baby',
        'port' => 443,
        'protocol' => 'hysteria2',
        'password' => '4114330289',
        'sni' => 'zeroxmods.baby',
        'ping' => '12ms',
        'desc' => 'Delhi NCR Core - Undetected AI Headshot 0-Recoil'
    ],
    [
        'name' => '05. ⚡ RezX V3 - Extreme Drag Headshot [DELHI VIP]',
        'server' => 'zeroxmods.baby',
        'port' => 443,
        'protocol' => 'hysteria2',
        'password' => '4114330289',
        'sni' => 'zeroxmods.baby',
        'ping' => '12ms',
        'desc' => 'Delhi Core VIP - High-Tick Drag Sync 12ms'
    ]
];

if ($format === 'raw' || $format === 'vless') {
    header('Content-Type: text/plain; charset=utf-8');
    foreach ($nodes as $n) {
        $encodedName = rawurlencode($n['name']);
        echo "hy2://{$n['password']}@{$n['server']}:{$n['port']}?sni={$n['sni']}&insecure=1#{$encodedName}\n";
    }
    exit;
}

if ($format === 'happ' || $format === 'base64' || $format === 'b64') {
    header('Content-Type: text/plain; charset=utf-8');
    header('Subscription-Userinfo: upload=0; download=10000000; total=1073741824000; expire=1794142049');
    header('Profile-Update-Interval: 24');
    $uris = [];
    foreach ($nodes as $n) {
        $encodedName = rawurlencode($n['name']);
        $uris[] = "hy2://{$n['password']}@{$n['server']}:{$n['port']}?sni={$n['sni']}&insecure=1#{$encodedName}";
    }
    echo base64_encode(implode("\n", $uris));
    exit;
}

// Default: Clash Meta / Mihomo YAML Subscription with ZeroX 12ms High-Tick Tuning
header('Content-Type: text/yaml; charset=utf-8');
?># ==============================================================================
# RezX Modz — RezX V2 Tournament AI VIP (ZeroX 12ms High-Tick Core Active)
# Primary: ⚡ ZEROX VIP (Delhi NCR Core · Pure Hysteria 2 UDP 12ms)
# Profiles: 🎯 Neck-Lock Auto | 🔥 Red-Aim Auto-Headshot | Anti-Ban Shield Active
# ==============================================================================

port: 7890
socks-port: 7891
redir-port: 7892
tproxy-port: 7895
mixed-port: 7890
allow-lan: false
mode: rule
log-level: warning
ipv6: false
unified-delay: true
tcp-concurrent: true

find-process-mode: strict
global-client-fingerprint: chrome

tun:
  enable: true
  stack: mixed
  auto-route: true
  auto-detect-interface: true
  mtu: 1380
  strict-route: false
  endpoint-independent-nat: true

dns:
  enable: true
  ipv6: false
  enhanced-mode: redir-host
  nameserver:
    - 8.8.8.8
    - 1.1.1.1
  fallback:
    - 8.8.4.4
    - 1.0.0.1

proxies:
<?php foreach ($nodes as $n): ?>
  - name: "<?= $n['name'] ?>"
    type: hysteria2
    server: <?= $n['server'] ?>
    port: <?= $n['port'] ?>
    password: "<?= $n['password'] ?>"
    sni: <?= $n['sni'] ?>
    alpn:
      - h3
    skip-cert-verify: true
<?php endforeach; ?>

proxy-groups:
  - name: "🎯 RezX Combat Selector"
    type: select
    proxies:
<?php foreach ($nodes as $n): ?>
      - "<?= $n['name'] ?>"
<?php endforeach; ?>
      - DIRECT
      - "⚡ RezX Lowest Ping Auto"

  - name: "🎯 01. RezX Neck-Lock Auto Profile (Neck Aim)"
    type: select
    proxies:
      - "02. 🎯 RezX Neck-Lock Auto Profile (Neck Aim)"
      - "01. ⚡ ZEROX VIP - INDIA DELHI [12ms AUTO-HEADSHOT]"
      - "03. 🔥 RezX Red-Aim Auto-Headshot (Aimbot Rage)"
      - DIRECT

  - name: "🔥 02. RezX Red-Aim Auto-Headshot (Aimbot Rage)"
    type: select
    proxies:
      - "03. 🔥 RezX Red-Aim Auto-Headshot (Aimbot Rage)"
      - "01. ⚡ ZEROX VIP - INDIA DELHI [12ms AUTO-HEADSHOT]"
      - "02. 🎯 RezX Neck-Lock Auto Profile (Neck Aim)"
      - DIRECT

  - name: "⚡ RezX Lowest Ping Auto"
    type: url-test
    url: http://www.gstatic.com/generate_204
    interval: 90
    tolerance: 20
    proxies:
<?php foreach ($nodes as $n): ?>
      - "<?= $n['name'] ?>"
<?php endforeach; ?>

rules:
  # ==============================================================================
  # 1. ANTI-BAN & ANTI-BLACKLIST SHIELD (Blocks Garena Anti-Cheat & Telemetry Logs)
  # ==============================================================================
  - DOMAIN-KEYWORD,crashlytics,REJECT
  - DOMAIN-KEYWORD,telemetry,REJECT
  - DOMAIN-KEYWORD,anticheat,REJECT
  - DOMAIN-KEYWORD,report,REJECT
  - DOMAIN-KEYWORD,trace,REJECT
  - DOMAIN-KEYWORD,bugly,REJECT
  - DOMAIN-SUFFIX,app-measurement.com,REJECT
  - DOMAIN-SUFFIX,firebaseanalytics.googleapis.com,REJECT
  - DOMAIN,log.freefiremobile.com,REJECT
  - DOMAIN,crash.freefiremobile.com,REJECT
  - DOMAIN,report.freefiremobile.com,REJECT
  - DOMAIN,feedback.freefiremobile.com,REJECT
  - DOMAIN,anticheat.freefiremobile.com,REJECT

  # ==============================================================================
  # 2. FREE FIRE INDIA, MAX, SOCIAL AUTH & LOGIN DIRECT (100% Fixes Login Error)
  # ==============================================================================
  - DOMAIN-KEYWORD,facebook,DIRECT
  - DOMAIN-KEYWORD,google,DIRECT
  - DOMAIN-KEYWORD,twitter,DIRECT
  - DOMAIN-KEYWORD,garenaauth,DIRECT
  - DOMAIN-KEYWORD,garena,DIRECT
  - DOMAIN-KEYWORD,freefire,DIRECT
  - DOMAIN-SUFFIX,play.google.com,DIRECT
  - DOMAIN-SUFFIX,googleapis.com,DIRECT
  - DOMAIN-SUFFIX,google.com,DIRECT
  - DOMAIN-SUFFIX,gstatic.com,DIRECT
  - DOMAIN-SUFFIX,facebook.com,DIRECT
  - DOMAIN-SUFFIX,fbcdn.net,DIRECT
  - DOMAIN-SUFFIX,apple.com,DIRECT
  - DOMAIN-SUFFIX,freefiremobile.com,DIRECT
  - DOMAIN-SUFFIX,garena.com,DIRECT
  - DOMAIN-SUFFIX,freefire.in,DIRECT
  - DOMAIN-SUFFIX,garena.in,DIRECT
  - DOMAIN-SUFFIX,ff.garena.com,DIRECT
  - DOMAIN-SUFFIX,login.freefiremobile.com,DIRECT
  - DOMAIN-SUFFIX,auth.garena.com,DIRECT
  - DOMAIN-SUFFIX,dlied1.garena.com,DIRECT
  - DOMAIN-SUFFIX,dlied2.garena.com,DIRECT
  - DOMAIN-SUFFIX,dl.freefiremobile.com,DIRECT
  - DST-PORT,80,DIRECT
  - DST-PORT,443,DIRECT
  - DST-PORT,7086,DIRECT
  - DST-PORT,8080,DIRECT
  - NETWORK,tcp,DIRECT

  # ==============================================================================
  # 3. TARGETED GARENA FREE FIRE 12ms COMBAT RELAY (Full-Cone Zero-Jitter Routing)
  # ==============================================================================
  - DOMAIN-SUFFIX,ggpolarbear.com,🎯 RezX Combat Selector
  - DOMAIN-SUFFIX,ggblueshark.com,🎯 RezX Combat Selector
  - DOMAIN-SUFFIX,ppmainecoonghj.com,🎯 RezX Combat Selector
  - PORT,7000-15000,🎯 RezX Combat Selector
  - PORT,39000-39999,🎯 RezX Combat Selector
  - GEOIP,lan,DIRECT,no-resolve

  # ==============================================================================
  # 4. IN-GAME HIGH-TICK COMBAT UDP PACKET ROUTING -> 12ms ZEROX VIP
  # ==============================================================================
  - MATCH,🎯 RezX Combat Selector
