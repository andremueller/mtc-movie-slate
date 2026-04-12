# MTC Remote Control

Python/Tkinter GUI for entering production metadata (artist, production, take),
sent via OSC to the TouchOSC MTC Movie Slate app.

The GUI provides text input fields that are difficult to implement in TouchOSC
on iPad/iPhone.

## Getting Started

```bash
./start.sh
```

The script automatically creates a venv with Python 3.13 (requires tkinter)
and installs dependencies.

Or via the Makefile in the parent directory:

```bash
make remote
```

## Dependencies

- Python 3.13 (Homebrew: `python@3.13` — tkinter is not available in Python 3.14)
- `python-osc`
- `zeroconf`

## Usage

1. Start → automatic Bonjour discovery of TouchOSC devices
2. Or manually enter the TouchOSC device IP/port
3. Enter artist, production, take
4. Values are sent via OSC (`/production/name`, `/production/part`, `/production/take`)
   to TouchOSC

## Recording Light Test

The GUI includes buttons to test the recording light without Logic Pro:

- **OFF** — turn light off
- **ARMED** — light blinks
- **RECORDING** — light on (steady)

These send OSC directly to `bridge.py` on port 9000.
