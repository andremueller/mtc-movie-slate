# MTC Movie Slate for TouchOSC

TouchOSC Mk2 Layout mit MIDI Timecode Display und Recording Light Integration.

## Features

- **MTC Display** — Empfängt MIDI Timecode (Quarter-Frame + Full Frame) und zeigt `HH:MM:SS:FF`
- **Recording Light** — Erkennt Recording State via MIDI Notes und zeigt visuelles Feedback
- **OSC Bridge** — Sendet Recording State via OSC an externe Bridge (für Shelly/Recording Light Steuerung)

## MIDI Notes (von Logic Pro Recording Light)

| Note | Vel | Bedeutung |
|------|-----|-----------|
| 24   | 127 | Spur für Aufnahme aktiviert (Record Ready → blinkt) |
| 24   | 0   | Record Ready deaktiviert |
| 25   | 127 | Aufnahme läuft (dauerhaft an) |
| 25   | 0   | Aufnahme gestoppt |

## OSC Integration

Das Lua Script im Layout sendet bei Recording State Changes OSC-Nachrichten:

| OSC Adresse | Wert | Bedeutung |
|-------------|------|-----------|
| `/recording/state` | 0 | Idle (Licht aus) |
| `/recording/state` | 1 | Armed (Licht blinkt) |
| `/recording/state` | 2 | Recording (Licht an) |
| `/recording/light` | 0/1 | Vereinfachter Licht-Zustand |

Eingehende OSC (von der Bridge, für manuelle Tests):

| OSC Adresse | Wert | Wirkung |
|-------------|------|---------|
| `/recording/light/set` | 0 | Licht aus |
| `/recording/light/set` | 1 | Licht an (Recording) |
| `/recording/light/set` | 2 | Licht blinken (Armed) |

### TouchOSC OSC Connection konfigurieren

1. **Connections** → **OSC 1** aktivieren
2. **Host:** IP-Adresse des Macs mit der Bridge (`bridge.py`)
3. **Send Port:** `9000`
4. **Type:** UDP

Die Bridge (`bridge.py`) leitet OSC → MQTT → Shelly weiter.
Siehe: [recording-light-shelly](https://github.com/muellera/recording-light-shelly) Projekt.

## MMC Format (Referenz)

```
F0 7F <Device-ID> <Sub-ID#1> [<Sub-ID#2> [<parameters>]] F7
```

- `7F` = deviceID (all devices)
- `06` = subId1 (MMC Machine Control Command)

## Detect Bonjour Services

```bash
dns-sd -B _osc._udp
```

Details zu einem Service:

```bash
dns-sd -L "My-iPhone" _osc._tcp local
```
