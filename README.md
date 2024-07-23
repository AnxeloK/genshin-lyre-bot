# Genshin Lyre Bot

**Genshin Lyre Bot** is a Python application designed to simulate keystrokes to play songs on the Genshin Impact lyre. It provides a graphical user interface (GUI) to manage songs, add new ones, edit existing songs, and delete them. The bot also supports hotkey functionality to start song playback.

## Features

- **Add New Songs**: Easily add new songs with a name and string of notes.
- **Edit Songs**: Modify existing songs’ names and note strings.
- **Delete Songs**: Remove songs from your list.
- **Play Songs**: Simulate keystrokes to play songs on the Genshin Impact lyre.
- **Hotkey Support**: Press `F9` to start playing the selected song and `Esc` to stop.

## Installation

### Requirements

- **Python 3.x**
- **Dependencies**: The following libraries are required:
  - `pywinauto`
  - `pyautogui`
  - `PyQt6`
  - `keyboard`
  - `win32api`

Install the required libraries using:

```bash
pip install -r requirements.txt
