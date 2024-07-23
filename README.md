# Genshin Lyre Bot

The Genshin Lyre Bot is a desktop application that simulates typing of songs for the Genshin Impact game using a lyre. This application provides a graphical user interface for managing and playing songs.

## Features

- **Add New Songs**: Enter a name and the string representation of the song to add it to the list.
- **Edit Songs**: Modify existing songs' names and strings.
- **Delete Songs**: Remove songs from the list.
- **Play Songs**: Simulate key presses to play the selected song using the F9 hotkey.
- **Stop Typing Simulation**: Abort the current song playback by pressing the Escape key.

## Requirements

- Python 3.8 or later
- `pywinauto` library
- `pyqt6` library
- `pywin32` library
- `keyboard` library (for hotkey management)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AnxeloK/genshin-lyre-bot.git
    cd genshin-lyre-bot
    ```

2. **Install the required packages:**

    You can install the necessary Python libraries using `pip`:

    ```bash
    pip install pywinauto pyqt6 pywin32 keyboard
    ```

## Usage

1. **Run the application:**

    ```bash
    python main.py
    ```

2. **Add a New Song:**
   - Enter the song name and string in the input fields at the bottom of the window.
   - Click "Add New Song" to add the song to the list.

3. **Select and Play a Song:**
   - Select a song from the list.
   - Press the F9 key to start the simulation of the song playback.

4. **Edit a Song:**
   - Select the song from the list and click "Edit Song."
   - Modify the song name and string in the dialog that appears, then click "Save."

5. **Delete a Song:**
   - Select the song from the list and click "Delete Song."
   - Confirm the deletion in the prompt.

6. **Stop Song Playback:**
   - Press the Escape key to stop the current song playback.

## How Song Strings Work

- **Definition and Purpose:**
  - A song string is a sequence of characters that represents the notes or key presses needed to play a song on the lyre in Genshin Impact. The string encodes the sequence of key presses for the bot to simulate.
  
- **Structure:**
  - Each character in a song string typically corresponds to a specific note or action:
    - `A` might represent one note.
    - `B` might represent another note.
    - `.` (dot) might represent a pause or short delay of 0.1 seconds.
  
- **Example:**
  - For a song string like `"A B C . D E F G"`, the bot would:
    - Press the key for note `A`.
    - Press the key for note `B`.
    - Press the key for note `C`.
    - Wait 0.1 seconds.
    - Press the key for note `D`.
    - Press the key for note `E`.
    - Press the key for note `F`.
    - Press the key for note `G`.

- **Implementation:**
  - The bot uses these strings to simulate key presses. It reads the song string and sends key presses according to the sequence of characters, handling delays to match the timing of the song.

- **Editing and Saving:**
  - You can edit song strings through the application's interface and save changes to the `songs.json` file.

## Configuration

- **Songs File:** The application stores songs in a JSON file named `songs.json`. You can modify this file directly if needed.

## Troubleshooting

- **Multiple Instances:** Ensure that only one instance of the application is running to avoid conflicts.
- **Missing Libraries:** If you encounter errors related to missing libraries, make sure all required packages are installed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

Happy playing!
