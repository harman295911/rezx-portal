[
  {
    "remarks": "01. \ud83c\uddee\ud83c\uddf3 INDIA RezX [MUMBAI VIP \u2022 20ms \u2022 ALL GUNS AIMLOCK & HEADSHOT]",
    "inbounds": [
      {
        "tag": "socks",
        "listen": "127.0.0.1",
        "port": 10808,
        "protocol": "socks",
        "settings": {
          "auth": "noauth",
          "udp": true
        },
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      },
      {
        "tag": "http",
        "listen": "127.0.0.1",
        "port": 10809,
        "protocol": "http",
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      }
    ],
    "outbounds": [
      {
        "protocol": "hysteria",
        "settings": {
          "address": "proxy-ind.dripwire.cc",
          "port": 443,
          "version": 2
        },
        "streamSettings": {
          "network": "hysteria",
          "security": "tls",
          "tlsSettings": {
            "alpn": [
              "h3"
            ],
            "serverName": "proxy-ind.dripwire.cc",
            "show": false
          },
          "hysteriaSettings": {
            "version": 2,
            "auth": "7569711485:6ad446c3a634245e"
          },
          "finalmask": {
            "quicParams": {
              "disableChromeParrot": true
            }
          }
        },
        "tag": "proxy"
      },
      {
        "protocol": "freedom",
        "tag": "direct"
      }
    ],
    "routing": {
      "domainStrategy": "AsIs",
      "rules": [
        {
          "type": "field",
          "network": "tcp",
          "port": "39000-39999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "network": "udp",
          "port": "10000-10999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "domain": [
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
          ],
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "network": "tcp,udp",
          "outboundTag": "direct"
        }
      ]
    }
  },
  {
    "remarks": "02. \ud83c\uddf8\ud83c\uddec SINGAPORE RezX [SG VIP \u2022 35ms \u2022 ALL GUNS AIMLOCK & HEADSHOT]",
    "inbounds": [
      {
        "tag": "socks",
        "listen": "127.0.0.1",
        "port": 10808,
        "protocol": "socks",
        "settings": {
          "auth": "noauth",
          "udp": true
        },
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      },
      {
        "tag": "http",
        "listen": "127.0.0.1",
        "port": 10809,
        "protocol": "http",
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      }
    ],
    "outbounds": [
      {
        "protocol": "hysteria",
        "settings": {
          "address": "proxy-sg.dripwire.cc",
          "port": 443,
          "version": 2
        },
        "streamSettings": {
          "network": "hysteria",
          "security": "tls",
          "tlsSettings": {
            "alpn": [
              "h3"
            ],
            "serverName": "proxy-sg.dripwire.cc",
            "show": false
          },
          "hysteriaSettings": {
            "version": 2,
            "auth": "7569711485:6ad446c3a634245e"
          },
          "finalmask": {
            "quicParams": {
              "disableChromeParrot": true
            }
          }
        },
        "tag": "proxy"
      },
      {
        "protocol": "freedom",
        "tag": "direct"
      }
    ],
    "routing": {
      "domainStrategy": "AsIs",
      "rules": [
        {
          "type": "field",
          "network": "tcp",
          "port": "39000-39999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "network": "udp",
          "port": "10000-10999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "domain": [
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
          ],
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "network": "tcp,udp",
          "outboundTag": "direct"
        }
      ]
    }
  },
  {
    "remarks": "03. \ud83c\udde7\ud83c\udde9 BANGLADESH RezX [DHAKA VIP \u2022 30ms \u2022 ALL GUNS AIMLOCK & HEADSHOT]",
    "inbounds": [
      {
        "tag": "socks",
        "listen": "127.0.0.1",
        "port": 10808,
        "protocol": "socks",
        "settings": {
          "auth": "noauth",
          "udp": true
        },
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      },
      {
        "tag": "http",
        "listen": "127.0.0.1",
        "port": 10809,
        "protocol": "http",
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      }
    ],
    "outbounds": [
      {
        "protocol": "hysteria",
        "settings": {
          "address": "proxy-bd.dripwire.cc",
          "port": 443,
          "version": 2
        },
        "streamSettings": {
          "network": "hysteria",
          "security": "tls",
          "tlsSettings": {
            "alpn": [
              "h3"
            ],
            "serverName": "proxy-bd.dripwire.cc",
            "show": false
          },
          "hysteriaSettings": {
            "version": 2,
            "auth": "7569711485:6ad446c3a634245e"
          },
          "finalmask": {
            "quicParams": {
              "disableChromeParrot": true
            }
          }
        },
        "tag": "proxy"
      },
      {
        "protocol": "freedom",
        "tag": "direct"
      }
    ],
    "routing": {
      "domainStrategy": "AsIs",
      "rules": [
        {
          "type": "field",
          "network": "tcp",
          "port": "39000-39999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "network": "udp",
          "port": "10000-10999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "domain": [
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
          ],
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "network": "tcp,udp",
          "outboundTag": "direct"
        }
      ]
    }
  },
  {
    "remarks": "04. \ud83c\uddea\ud83c\uddfa EUROPE RezX [FRANKFURT VIP \u2022 90ms \u2022 ALL GUNS AIMLOCK & HEADSHOT]",
    "inbounds": [
      {
        "tag": "socks",
        "listen": "127.0.0.1",
        "port": 10808,
        "protocol": "socks",
        "settings": {
          "auth": "noauth",
          "udp": true
        },
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      },
      {
        "tag": "http",
        "listen": "127.0.0.1",
        "port": 10809,
        "protocol": "http",
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      }
    ],
    "outbounds": [
      {
        "protocol": "hysteria",
        "settings": {
          "address": "proxy-eu.dripwire.cc",
          "port": 443,
          "version": 2
        },
        "streamSettings": {
          "network": "hysteria",
          "security": "tls",
          "tlsSettings": {
            "alpn": [
              "h3"
            ],
            "serverName": "proxy-eu.dripwire.cc",
            "show": false
          },
          "hysteriaSettings": {
            "version": 2,
            "auth": "7569711485:6ad446c3a634245e"
          },
          "finalmask": {
            "quicParams": {
              "disableChromeParrot": true
            }
          }
        },
        "tag": "proxy"
      },
      {
        "protocol": "freedom",
        "tag": "direct"
      }
    ],
    "routing": {
      "domainStrategy": "AsIs",
      "rules": [
        {
          "type": "field",
          "network": "tcp",
          "port": "39000-39999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "network": "udp",
          "port": "10000-10999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "domain": [
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
          ],
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "network": "tcp,udp",
          "outboundTag": "direct"
        }
      ]
    }
  },
  {
    "remarks": "05. \ud83c\udde7\ud83c\uddf7 BRAZIL RezX [SAO PAULO VIP \u2022 120ms \u2022 ALL GUNS AIMLOCK & HEADSHOT]",
    "inbounds": [
      {
        "tag": "socks",
        "listen": "127.0.0.1",
        "port": 10808,
        "protocol": "socks",
        "settings": {
          "auth": "noauth",
          "udp": true
        },
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      },
      {
        "tag": "http",
        "listen": "127.0.0.1",
        "port": 10809,
        "protocol": "http",
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      }
    ],
    "outbounds": [
      {
        "protocol": "hysteria",
        "settings": {
          "address": "proxy-br.dripwire.cc",
          "port": 443,
          "version": 2
        },
        "streamSettings": {
          "network": "hysteria",
          "security": "tls",
          "tlsSettings": {
            "alpn": [
              "h3"
            ],
            "serverName": "proxy-br.dripwire.cc",
            "show": false
          },
          "hysteriaSettings": {
            "version": 2,
            "auth": "7569711485:6ad446c3a634245e"
          },
          "finalmask": {
            "quicParams": {
              "disableChromeParrot": true
            }
          }
        },
        "tag": "proxy"
      },
      {
        "protocol": "freedom",
        "tag": "direct"
      }
    ],
    "routing": {
      "domainStrategy": "AsIs",
      "rules": [
        {
          "type": "field",
          "network": "tcp",
          "port": "39000-39999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "network": "udp",
          "port": "10000-10999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "domain": [
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
          ],
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "network": "tcp,udp",
          "outboundTag": "direct"
        }
      ]
    }
  },
  {
    "remarks": "06. \ud83d\udee1\ufe0f RezX BACKUP [ANTI-999+ FAILOVER \u2022 20ms \u2022 HIGH TICKRATE]",
    "inbounds": [
      {
        "tag": "socks",
        "listen": "127.0.0.1",
        "port": 10808,
        "protocol": "socks",
        "settings": {
          "auth": "noauth",
          "udp": true
        },
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      },
      {
        "tag": "http",
        "listen": "127.0.0.1",
        "port": 10809,
        "protocol": "http",
        "sniffing": {
          "destOverride": [
            "http",
            "tls",
            "quic"
          ],
          "enabled": true,
          "routeOnly": false
        }
      }
    ],
    "outbounds": [
      {
        "protocol": "hysteria",
        "settings": {
          "address": "rezxmodz.lol",
          "port": 443,
          "version": 2
        },
        "streamSettings": {
          "network": "hysteria",
          "security": "tls",
          "tlsSettings": {
            "alpn": [
              "h3"
            ],
            "serverName": "rezxmodz.lol",
            "show": false
          },
          "hysteriaSettings": {
            "version": 2,
            "auth": "4114330289"
          },
          "finalmask": {
            "quicParams": {
              "disableChromeParrot": true
            }
          }
        },
        "tag": "proxy"
      },
      {
        "protocol": "freedom",
        "tag": "direct"
      }
    ],
    "routing": {
      "domainStrategy": "AsIs",
      "rules": [
        {
          "type": "field",
          "network": "tcp",
          "port": "39000-39999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "network": "udp",
          "port": "10000-10999",
          "outboundTag": "proxy"
        },
        {
          "type": "field",
          "domain": [
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
          ],
          "outboundTag": "direct"
        },
        {
          "type": "field",
          "network": "tcp,udp",
          "outboundTag": "direct"
        }
      ]
    }
  }
]