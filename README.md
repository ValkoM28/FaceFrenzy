# FaceFrenzy

A face-detection game built for the PYNQ FPGA platform.

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `pynq` requires a Xilinx PYNQ-compatible board (e.g. PYNQ-Z1/Z2). On a standard PC you can omit it for development purposes.

### 3. Run

```bash
cd src/app
python main.py
```

## Deactivate the virtual environment

```bash
deactivate
```
