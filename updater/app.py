# Author: Ali Yasser Ali Abdallah
# Date: 2024
# Description: This script serves as a template for integrating an update feature into a PyQt application.
#              It uses the `Updater` class to check for new releases on a specified GitHub repository,
#              handles the download and installation of updates, and manages the visibility of the update-related
#              UI elements. The script also includes a mechanism to delete older versions of the tool, keeping
#              the application directory clean.

import os
import sys
from PyQt6 import QtWidgets
from updater import Updater
from gui import Ui_MainWindow

class ToolClass(QtWidgets.QWidget, Ui_MainWindow):
    """
    The main class for the PyQt application, inheriting from QWidget and the auto-generated UI class.
    It integrates the update feature using the `Updater` class.
    """

    def __init__(self):
        """
        Initializes the tool's main window and sets up the update feature. The updater is configured
        with the current version and GitHub repository details. It connects the update button to the
        updater's update function and checks for updates when the "Check" button is clicked.
        """
        super().__init__()
        self.setupUi(MainWindow)

        # Initialize Updater with the current version and repository details
        self.updater = Updater(
            current_version="v6.00",  # Replace with your tool's version
            repo_owner="ENGaliyasser",
            repo_name="Updateing-tool",
            progress_bar=self.progressBar
        )

        # Connect the update button to the updater's update function
        self.update.clicked.connect(self.updater.update_application)

        # Hide update-related UI elements initially
        self.progressBar.setVisible(False)
        self.update.setVisible(False)
        self.ask.setVisible(False)

        # Connect the "Check" button to the check_update function
        self.check.clicked.connect(lambda: self.updater.check_update(self.update, self.ask))

if __name__ == "__main__":
    """
    The main entry point of the application. It deletes old versions of the tool, 
    initializes the PyQt application, and shows the main window.
    """



    app = QtWidgets.QApplication(sys.argv)
    # Delete old versions
    Updater.delete_old_versions(current_version="v6.00")  # Replace with your tool's version
    MainWindow = QtWidgets.QMainWindow()
    ui = ToolClass()
    MainWindow.show()
    sys.exit(app.exec())