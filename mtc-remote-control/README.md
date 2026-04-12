# MTC Remote Control

Python/Tkinter GUI zum Eingeben von Produktions-Metadaten (Künstler, Produktion, Take),
die per OSC an die TouchOSC MTC Movie Slate App gesendet werden.

Die GUI bietet Texteingabefelder, die in TouchOSC auf dem iPad/iPhone
schwierig umzusetzen sind.

## Starten

```bash
./start.sh
```

Das Script erstellt automatisch ein venv mit Python 3.13 (benötigt tkinter)
und installiert die Abhängigkeiten.

Oder über das Makefile im übergeordneten Verzeichnis:

```bash
make remote
```

## Abhängigkeiten

- Python 3.13 (Homebrew: `python@3.13` — tkinter ist in Python 3.14 nicht enthalten)
- `python-osc`
- `zeroconf`

## Usage

1. Starten → automatische Bonjour-Discovery von TouchOSC Geräten
2. Oder manuell IP/Port des TouchOSC-Geräts eingeben
3. Künstler, Produktion, Take eingeben
4. Werte werden per OSC (`/production/name`, `/production/part`, `/production/take`)
   an TouchOSC gesendet
