# DRVAC - Davinci Resolve Video & Audio Converter For Linux

**Created by hnrijs**  
GitHub: [https://github.com/hnrijs/DRVAC](https://github.com/hnrijs/DRVAC)

## Description
DRVAC is a Python program with a PyQt6 GUI for converting video and audio files for DaVinci Resolve on Linux. It allows you to convert videos to MOV format with PCM 24-bit audio, audio files to 24-bit WAV, add multiple video and audio files at once, and select a destination folder for all converted outputs.

**How to use DRVAC:**  
After cloning the repository, navigate to the DRVAC folder using `cd DRVAC` and run the program with `python3 drvac.py`. In the program, click **“Add Video Input”** to select one or more video files and **“Add Audio Input”** to select audio files. Choose a destination folder for the converted files. Click **“Convert Video”** to convert videos to `.mov` with 24-bit PCM audio and **“Convert Audio”** to convert audio files to 24-bit WAV. All selected files are processed in batch, and the converted files will appear in your chosen folder.

## Requirements
- Python 3.x  
- PyQt6
- FFmpeg

## Installation
Clone the repository:
```bash
git clone https://github.com/hnrijs/DRVAC.git
cd DRVAC
python3 drvac.py
