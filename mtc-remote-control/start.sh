#!/bin/bash
set -e
cd "$(dirname "$0")"

PYTHON=python3.13
VENV=venv

# Venv erstellen falls nicht vorhanden
if [ ! -d "$VENV" ]; then
    echo "Creating venv with $PYTHON..."
    $PYTHON -m venv "$VENV"
fi

# Abhängigkeiten installieren
source "$VENV/bin/activate"
pip install -q python-osc zeroconf 2>&1 | tail -1

# Starten
echo "Starting MTC Remote Control..."
python src/mtc_remote_control/main.py
