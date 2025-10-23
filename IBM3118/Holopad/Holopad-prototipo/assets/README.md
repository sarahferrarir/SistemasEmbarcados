# Holopad: A Gesture-Based Mouse Control System

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Holopad is a Python project that provides robust, real-time mouse control using hand gestures captured via your webcam. It uses **MediaPipe Hands** for high-fidelity hand tracking and **PyAutoGUI** to translate a rich set of gestures into desktop actions.

This project has been re-architected from a simple mouse mover into a full-featured HCI (Human-Computer Interaction) tool that is responsive, configurable, and intuitive.

---

## Features

- **Multi-Gesture Support:** A full suite of mouse actions, not just moving and clicking.
- **High-Precision Clicking:** A smart "freeze" feature locks the cursor just before a click, allowing you to hit small targets accurately.
- **Full Mouse Functionality:** Includes Left-Click, Right-Click, Drag & Drop, and Scrolling.
- **Visual Feedback:** The on-screen cursor changes color to reflect the current state (Moving, Freezing, Dragging) for a more intuitive experience.
- **Safety Stop Gesture:** A dedicated "closed fist" gesture instantly and safely terminates the program.
- **Highly Configurable:** All sensitivities, distances, and thresholds are centralized in `config.py` for easy tuning to your preferences and lighting conditions.
- **Modular Codebase:** Refactored into a clean, modular structure (`main`, `controls`, `utils`, `config`) for easy maintenance and future expansion.

---

## Gesture Guide

| Action | Gesture | Visual Feedback |
| :--- | :--- | :--- |
| **Move Cursor** | Point with Index & Middle Fingers | Blue Cursor Dot |
| **Freeze Cursor** | Begin pinching Thumb toward Index | Yellow Cursor Dot |
| **Left Click / Drag** | Pinch Thumb & Index Finger | Red Cursor Dot (while dragging) |
| **Right Click** | Pinch Thumb & Ring Finger | (Instant action) |
| **Activate Scroll** | Raise Index, Middle, & Ring Fingers | "SCROLL MODE" text |
| **Scroll Up/Down** | Move hand Up/Down in Scroll Mode | (Page scrolls) |
| **Stop Program** | Separate all fingers, then Close Fist | "STOPPING..." text |

---

## System Requirements

- Python 3.11+
- A webcam (internal or external)
- Operating System: Windows, macOS, or Linux

---

## Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/Holopad.git](https://github.com/your-username/Holopad.git)
    cd Holopad
  
2.  **Create a Virtual Environment (Recommended):**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    This project includes a setup script to install all required packages from `requirements.txt`.
    ```bash
    python setup.py
    ```
    *Alternatively, you can install them manually:*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    ```bash
    python main.py
    ```
    
5.  **To Stop:**
    Either press **`q`** on the OpenCV window or use the **Stop Gesture** (close your fist).

---

## Configuration

This project is designed to be easily tuned. All sensitivity values, distances, and thresholds are located in **`config.py`**.

If you find the cursor too sensitive, the click too difficult, or the scroll too fast, you can adjust these values:

- `SENSITIVITY`: Controls cursor smoothing.
- `CLICK_DISTANCE_THRESHOLD`: How close your fingers need to be to register a click.
- `CLICK_INTENT_THRESHOLD`: How close your fingers need to be to "freeze" the cursor.
- `SCROLL_SENSITIVITY`: Controls the speed of the scroll.
- `DEADZONE`: Ignores tiny hand movements to prevent "jitter".

---

## Project Structure

The codebase is refactored for clarity and maintainability:

- **`main.py`**: The main application entry point. Handles the camera feed, image processing, and the main gesture orchestration loop.
- **`cursor_control.py`**: Contains all "handler" functions that perform mouse actions (e.g., `handle_pointing`, `handle_scrolling`) and manages the system's state (e.g., `dragging`).
- **`utils.py`**: A module for all "helper" and detection functions (e.g., `is_fist()`, `get_gesture_distance()`). It performs calculations but does not execute actions.
- **`config.py`**: A central file for all constants, thresholds, and configuration variables.
- **`setup.py`**: A utility script to set up the environment and install dependencies.