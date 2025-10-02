# PyQt Auto-Updating Tool

This repository contains a PyQt-based application with an integrated auto-updating feature. The tool is designed to automatically check for updates, download the latest version, and manage the installation process seamlessly. The update mechanism is designed to be modular, allowing easy integration into other PyQt applications.

## Features

- **Auto-Update Check:** Automatically checks the specified GitHub repository for the latest release.
- **Modular Design:** Easily integrate the updating feature into any PyQt application.
- **Progress Feedback:** Displays a progress bar during the download of the new version.
- **Safe Deletion of Old Versions:** Deletes the old executable after successfully launching the new version.
- **Customizable:** Modify the `updater.py` file to suit your application's update requirements.

## Files in This Repository

- **`updater.py`**: Handles the update check, download process, and deletion of outdated versions. It manages the entire update cycle, from checking the repository to launching the new version.
- **`back.py`**: The main script for the PyQt application, which integrates the update feature using the `Updater` class.
- **`gui.ui`**: The Qt Designer file used to create the GUI for the application. This file can be modified using Qt Designer and converted to a Python script using `pyuic5`.
- **`main.exe`**: The compiled executable of the PyQt application with the auto-updating feature. This is available in the [Releases](https://github.com/ENGaliyasser/Updateing-tool/releases) section.

## How It Works

1. **Initialization**: When the application starts, it checks for older versions of the application (`tobedeletedddddd.exe`) and deletes them.
   
2. **Update Check**: The user can check for updates by clicking the "Check" button in the GUI. If a new version is available, an update button becomes visible.
   
3. **Update Process**: Upon clicking the update button, the new version is downloaded. The current version renames itself to `tobedeletedddddd.exe` and launches the new version.
   
4. **Cleanup**: The new version, upon starting, searches for `tobedeletedddddd.exe` and deletes it, ensuring that only the latest version remains.

## Setup Instructions

### Prerequisites

- Python 3.x
- PyQt5

