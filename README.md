# Visioncount ✋

**Visioncount** is a real-time computer vision application that detects and counts raised fingers using a standard webcam. Built with Python, OpenCV, and Google's MediaPipe hand-tracking model, it identifies up to two hands simultaneously, distinguishes left from right, and classifies common gestures — including Fist, Open Palm, Peace, Thumbs Up, and Pointing — purely from hand landmark geometry, with no manual calibration required.

The app overlays a live dashboard on the video feed showing per-hand finger counts, total count, FPS, and session stats, and includes a lighthearted two-hand Rock-Paper-Scissors readout. It also supports screenshot capture, configurable camera/confidence settings via command-line flags, and structured logging with graceful error handling for camera and processing failures.

**Tech stack:** Python · OpenCV · MediaPipe · argparse · logging

---

## Features

- **Multi-hand tracking** — detects up to two hands at once, each with its own finger count and info panel.
- **Left/Right hand labeling** — thumb logic auto-adjusts per hand so counting is accurate for both.
- **Gesture recognition** — recognizes Fist, Open Palm, Peace, Thumbs Up, Pointing, Rock On, and more from finger patterns.
- **Two-hand Rock-Paper-Scissors readout** — show two hands and see your "moves" called out live.
- **Live FPS counter** and session stats (max fingers seen, screenshots taken) shown in a translucent header.
- **Screenshot capture** — press `s` to save the current frame with a timestamped filename.
- **Robust & configurable** — command-line flags for camera index, resolution, confidence thresholds, and max hands; handles camera failures and per-frame processing errors without crashing; structured logging instead of bare prints.

## Requirements

- Python **3.9 – 3.11** (MediaPipe's classic `solutions` API isn't reliably available on newer Python versions — see Troubleshooting below)
- A webcam

## Setup

```bash
python3 -m venv ai_env
source ai_env/bin/activate       # Windows: ai_env\Scripts\activate
pip install -r requirements.txt
```

## How to run

```bash
source ai_env/bin/activate
python finger_counter.py
```

### Optional flags

```bash
python finger_counter.py --camera 1 --max-hands 2 --confidence 0.75 \
    --width 1280 --height 720 --screenshot-dir screenshots --log-level INFO
```

| Flag                  | Default        | Description                        |
|-----------------------|----------------|-------------------------------------|
| `--camera`            | `0`            | Camera index to open                |
| `--max-hands`         | `2`            | Max hands to track simultaneously   |
| `--confidence`        | `0.7`          | Min detection/tracking confidence   |
| `--width` / `--height`| `1280` / `720` | Requested capture resolution        |
| `--screenshot-dir`    | `screenshots`  | Folder where screenshots are saved  |
| `--log-level`         | `INFO`         | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Controls

| Key | Action               |
|-----|----------------------|
| `q` | Quit                 |
| `s` | Save a screenshot    |
| `r` | Reset session stats  |

## How it works

1. Each frame is flipped (mirror view) and converted to RGB for MediaPipe.
2. MediaPipe Hands returns 21 landmarks per detected hand plus a Left/Right classification.
3. For each hand, finger "up/down" state is computed by comparing tip and joint landmark positions (thumb uses x-coordinates and flips based on handedness; the other four fingers use y-coordinates).
4. The finger-state pattern is matched against a gesture table to label common gestures, and counts/gestures are drawn as a per-hand info card.
5. A header overlay shows total fingers, FPS, and running session stats.

## Troubleshooting

**`AttributeError: module 'mediapipe' has no attribute 'solutions'`**
Recent MediaPipe releases have removed the legacy `solutions` API this project uses, and pip may install one of these newer versions automatically — especially on very new Python versions (3.12+) where older, compatible MediaPipe builds aren't available. Fix:

```bash
# Use Python 3.11 specifically for this project
python3.11 -m venv ai_env
source ai_env/bin/activate
pip install opencv-python "mediapipe==0.10.14"
```

**Camera won't open / `Could not open camera index 0`**
Try a different index with `--camera 1`, and make sure no other app is using the webcam. On macOS, check System Settings → Privacy & Security → Camera and allow Terminal/your IDE access.

## License

MIT — feel free to use, modify, and share.
