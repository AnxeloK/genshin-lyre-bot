import sys
import json
import os
import threading
import time
from pywinauto import Application
from pywinauto.keyboard import send_keys
from win32api import keybd_event, MapVirtualKey
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, 
    QLineEdit, QListWidget, QHBoxLayout, QMessageBox, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt

SONGS_FILE = 'songs.json'

is_running = False
typing_thread = None

def load_songs():
    if os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_songs(songs):
    with open(SONGS_FILE, 'w') as file:
        json.dump(songs, file, indent=4)

def simulate_key_presses(input_string):
    global is_running
    global typing_thread
    if is_running:
        return
    is_running = True
    for char in input_string:
        if not is_running:
            break
        if char == '.':
            time.sleep(0.1)
        else:
            vk_code = ord(char.upper())
            keybd_event(vk_code, MapVirtualKey(vk_code, 0), 0, 0)
            time.sleep(0.05)
            keybd_event(vk_code, MapVirtualKey(vk_code, 0), 2, 0)
    is_running = False

def stop_typing_simulation():
    global is_running
    is_running = False

class EditSongDialog(QDialog):
    def __init__(self, song_name, song_string, on_save):
        super().__init__()
        self.on_save = on_save
        self.setWindowTitle("Edit Song")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #2c313c; color: white;")

        layout = QFormLayout()
        layout.setSpacing(15)

        self.name_input = QLineEdit(song_name)
        self.name_input.setPlaceholderText("Song Name")
        self.name_input.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #61dafb;
            background-color: #1e2024;
            color: white;
        """)

        self.string_input = QLineEdit(song_string)
        self.string_input.setPlaceholderText("Song String")
        self.string_input.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #61dafb;
            background-color: #1e2024;
            color: white;
        """)

        layout.addRow("Song Name:", self.name_input)
        layout.addRow("Song String:", self.string_input)

        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: #61dafb;
            color: #282c34;
            border: none;
            border-radius: 5px;
        """)
        save_button.clicked.connect(self.save_song)

        layout.addWidget(save_button)
        self.setLayout(layout)

    def save_song(self):
        new_name = self.name_input.text()
        new_string = self.string_input.text()
        self.on_save(new_name, new_string)
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.songs = load_songs()
        self.current_song_string = ""
        self.setWindowTitle("Song Player")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #282c34;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        title_label = QLabel("Songs List")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #61dafb;
            margin: 20px 0;
        """)
        main_layout.addWidget(title_label)

        self.song_list = QListWidget()
        self.song_list.addItems(self.songs.keys())
        self.song_list.setStyleSheet("""
            font-size: 18px;
            color: white;
            background-color: #1e2024;
            border: 1px solid #61dafb;
            padding: 10px;
            selection-background-color: #61dafb;
            selection-color: #282c34;
        """)
        self.song_list.currentItemChanged.connect(self.update_current_song)
        main_layout.addWidget(self.song_list)

        add_layout = QHBoxLayout()
        add_layout.setSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Song Name")
        self.name_input.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #61dafb;
            background-color: #1e2024;
            color: white;
        """)
        add_layout.addWidget(self.name_input)

        self.string_input = QLineEdit()
        self.string_input.setPlaceholderText("Song String")
        self.string_input.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #61dafb;
            background-color: #1e2024;
            color: white;
        """)
        add_layout.addWidget(self.string_input)

        add_button = QPushButton("Add New Song")
        add_button.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: #61dafb;
            color: #282c34;
            border: none;
            border-radius: 5px;
        """)
        add_button.clicked.connect(self.add_new_song)
        add_layout.addWidget(add_button)

        main_layout.addLayout(add_layout)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        select_button = QPushButton("Select Song")
        select_button.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: #61dafb;
            color: #282c34;
            border: none;
            border-radius: 5px;
        """)
        select_button.clicked.connect(self.setup_f9_hotkey)
        action_layout.addWidget(select_button)

        edit_button = QPushButton("Edit Song")
        edit_button.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        """)
        edit_button.clicked.connect(self.edit_song)
        action_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete Song")
        delete_button.setStyleSheet("""
            font-size: 16px;
            padding: 10px;
            background-color: #ff4c4c;
            color: white;
            border: none;
            border-radius: 5px;
        """)
        delete_button.clicked.connect(self.delete_song)
        action_layout.addWidget(delete_button)

        main_layout.addLayout(action_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setup_f9_hotkey()

    def setup_f9_hotkey(self):
        import keyboard
        try:
            keyboard.remove_hotkey('f9')
        except KeyError:
            pass
        keyboard.add_hotkey('f9', self.start_simulation)

    def start_simulation(self):
        global typing_thread
        if self.current_song_string and not is_running:
            typing_thread = threading.Thread(target=simulate_key_presses, args=(self.current_song_string,))
            typing_thread.start()

    def update_current_song(self, current, previous):
        if current:
            self.current_song_string = self.songs.get(current.text(), "")

    def add_new_song(self):
        name = self.name_input.text().strip()
        string = self.string_input.text().strip()
        if not name or not string:
            QMessageBox.critical(self, "Error", "Both fields must be filled out.")
            return
        if name in self.songs:
            QMessageBox.critical(self, "Error", "Song with this name already exists.")
            return
        self.songs[name] = string
        save_songs(self.songs)
        self.song_list.addItem(name)
        self.name_input.clear()
        self.string_input.clear()

    def edit_song(self):
        current_item = self.song_list.currentItem()
        if current_item:
            selected_song = current_item.text()
            dialog = EditSongDialog(selected_song, self.songs[selected_song], self.save_edited_song)
            dialog.exec()

    def save_edited_song(self, new_name, new_string):
        selected_item = self.song_list.currentItem()
        if selected_item:
            old_name = selected_item.text()
            if old_name != new_name and new_name in self.songs:
                QMessageBox.critical(self, "Error", "Song with this name already exists.")
                return
            del self.songs[old_name]
            self.songs[new_name] = new_string
            save_songs(self.songs)
            self.song_list.clear()
            self.song_list.addItems(self.songs.keys())

    def delete_song(self):
        current_item = self.song_list.currentItem()
        if current_item:
            selected_song = current_item.text()
            confirm = QMessageBox.question(
                self, "Confirm Deletion",
                f"Are you sure you want to delete '{selected_song}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                del self.songs[selected_song]
                save_songs(self.songs)
                self.song_list.takeItem(self.song_list.row(current_item))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
