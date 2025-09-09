import sys
import subprocess
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QFileDialog, QMessageBox, QMainWindow, QTextEdit
)
from PyQt6.QtCore import Qt


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help - DRVAC")
        self.setGeometry(350, 250, 600, 400)

        layout = QVBoxLayout()
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setPlainText(
            "Davinci Resolve Video & Audio Converter For Linux (DRVAC)\n\n"
            "=== Requirements ===\n"
            "Before using this program, make sure the following are installed on your system:\n"
            "1. Python 3.x (installed by default on most Linux distros)\n"
            "2. PyQt6 (can be installed with: pip install PyQt6)\n"
            "3. FFmpeg (install on Arch Linux: sudo pacman -S ffmpeg)\n\n"
            "Without these, the program will not run properly.\n\n"
            "=== How to use ===\n"
            "1. Click 'Add Video Input' to select one or more video files.\n"
            "   The program will convert them to MOV format with PCM 24-bit audio.\n"
            "   Files will be saved as 'output1.mov', 'output2.mov', etc.\n\n"
            "2. Click 'Add Audio Input' to select one or more audio files.\n"
            "   The program will convert them to 24-bit WAV format.\n"
            "   Files will be saved as 'audio_output24bit1.wav', 'audio_output24bit2.wav', etc.\n\n"
            "3. Use the 'Settings' menu at the top to choose the destination folder.\n"
            "   By default, converted files are saved in the current working directory.\n\n"
            "4. Click 'Convert Video' or 'Convert Audio' to start conversion.\n\n"
            "=== Notes ===\n"
            "- This tool is designed for preparing files compatible with DaVinci Resolve.\n"
            "- Video tracks are copied without re-encoding (-c:v copy).\n"
            "- Audio tracks are converted to 24-bit PCM (-c:a pcm_s24le).\n"
        )
        layout.addWidget(help_text)
        self.setLayout(layout)


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About - DRVAC")
        self.setGeometry(400, 300, 500, 200)

        layout = QVBoxLayout()
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setPlainText(
            "Davinci Resolve Video & Audio Converter For Linux (DRVAC)\n\n"
            "Created by: Henrijs\n"
            "GitHub: https://github.com/hnrijs\n\n"
            "This program was made to simplify preparing video & audio\n"
            "files for DaVinci Resolve on Linux.\n"
        )
        layout.addWidget(about_text)
        self.setLayout(layout)


class DRVAC(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Davinci Resolve Video & Audio Converter For Linux (DRVAC)")
        self.setGeometry(300, 200, 700, 450)

        # === Default destination folder ===
        self.destination_folder = os.getcwd()

        # === Video & Audio paths ===
        self.video_paths = []
        self.audio_paths = []

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Video section
        self.video_label = QLabel("Video Converter")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_text = QTextEdit()
        self.video_text.setReadOnly(True)
        self.video_text.setPlaceholderText("No videos selected")

        self.add_video_btn = QPushButton("Add Video Input")   # <-- no (s)
        self.convert_video_btn = QPushButton("Convert Video") # <-- no S

        self.add_video_btn.clicked.connect(self.add_videos)
        self.convert_video_btn.clicked.connect(self.convert_videos)

        video_layout = QHBoxLayout()
        video_layout.addWidget(self.add_video_btn)
        video_layout.addWidget(self.convert_video_btn)

        # Audio section
        self.audio_label = QLabel("Audio Converter")
        self.audio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.audio_text = QTextEdit()
        self.audio_text.setReadOnly(True)
        self.audio_text.setPlaceholderText("No audios selected")

        self.add_audio_btn = QPushButton("Add Audio Input")   # <-- no (s)
        self.convert_audio_btn = QPushButton("Convert Audio") # <-- no S

        self.add_audio_btn.clicked.connect(self.add_audios)
        self.convert_audio_btn.clicked.connect(self.convert_audios)

        audio_layout = QHBoxLayout()
        audio_layout.addWidget(self.add_audio_btn)
        audio_layout.addWidget(self.convert_audio_btn)

        # Destination folder info
        self.dest_label = QLabel(f"Current Destination: {self.destination_folder}")
        self.dest_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.video_text)
        layout.addLayout(video_layout)

        layout.addWidget(self.audio_label)
        layout.addWidget(self.audio_text)
        layout.addLayout(audio_layout)

        layout.addWidget(self.dest_label)

        central_widget.setLayout(layout)

        # Menu bar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Settings")
        help_menu = menubar.addMenu("Help")
        about_menu = menubar.addMenu("About")

        choose_dest_action = settings_menu.addAction("Choose Destination Folder")
        choose_dest_action.triggered.connect(self.choose_destination)

        show_dest_action = settings_menu.addAction("Show Current Destination Folder")
        show_dest_action.triggered.connect(self.show_destination)

        help_action = help_menu.addAction("How to use / Requirements")
        help_action.triggered.connect(self.show_help)

        about_action = about_menu.addAction("Credits / GitHub")
        about_action.triggered.connect(self.show_about)

    # === Menu functions ===
    def choose_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.destination_folder = folder
            self.dest_label.setText(f"Current Destination: {folder}")
            QMessageBox.information(self, "Destination Set", f"Files will be saved in:\n{folder}")

    def show_destination(self):
        QMessageBox.information(self, "Current Destination", f"Files are saved in:\n{self.destination_folder}")

    def show_help(self):
        self.help_window = HelpWindow()
        self.help_window.show()

    def show_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    # === Video functions ===
    def add_videos(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Videos", "", "Video Files (*.mp4 *.mov *.avi *.mkv)")
        if files:
            self.video_paths = files
            self.video_text.setPlainText("\n".join(files))

    def convert_videos(self):
        if not self.video_paths:
            QMessageBox.warning(self, "Warning", "No video selected!")  # <-- no S
            return

        for idx, video in enumerate(self.video_paths, start=1):
            output = os.path.join(self.destination_folder, f"output{idx}.mov")
            cmd = ["ffmpeg", "-i", video, "-c:v", "copy", "-c:a", "pcm_s24le", output]
            subprocess.run(cmd)
        QMessageBox.information(self, "Done", f"Converted {len(self.video_paths)} video(s)")

    # === Audio functions ===
    def add_audios(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Audios", "", "Audio Files (*.mp3 *.wav *.flac)")
        if files:
            self.audio_paths = files
            self.audio_text.setPlainText("\n".join(files))

    def convert_audios(self):
        if not self.audio_paths:
            QMessageBox.warning(self, "Warning", "No audio selected!")  # <-- no S
            return

        for idx, audio in enumerate(self.audio_paths, start=1):
            output = os.path.join(self.destination_folder, f"audio_output24bit{idx}.wav")
            cmd = ["ffmpeg", "-i", audio, "-c:a", "pcm_s24le", output]
            subprocess.run(cmd)
        QMessageBox.information(self, "Done", f"Converted {len(self.audio_paths)} audio(s)")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DRVAC()
    window.show()
    sys.exit(app.exec())
