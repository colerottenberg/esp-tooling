import sys
import os
import esptool as esp
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextEdit, QLabel, QVBoxLayout
# Now for the simple class
# We need to create a simple CLI tool for flashing the esp32

class DropZone(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.label = QLabel('Drop a file here...', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        file_path = e.mimeData().urls()[0].toLocalFile()
        self.label.setText(f'File path: {file_path}')
        print(f'File path: {file_path}')
        flash(file_path)

def grab(version):
    print("Grabbing version: " + version)
    # Grab specific version bins from local repo or from github
    # Check if version exists in local repo
    ex = f"gh release download {version}  -D ./{version} --repo BlueVigil/top-panel-firmware"
    os.system(ex)
    # If it can enter the directory, then it exists
    

def selection(releases):
    menu = "Select an option:\n1. Flash\n2. Erase\n3. Exit\n"
    bin_menu = "Select a version:\n1. Stable\n2. Beta\n3. Exit\n"
    print(menu)
    choice = input("Enter your choice: ")
    if choice == "1":
        print(bin_menu)
        bin_choice = input("Enter your choice: ")
        if bin_choice == "1":
            flash(releases["stable"])
        elif bin_choice == "2":
            flash(releases["beta"])
        elif bin_choice == "3":
            sys.exit()
        else:
            print("Invalid choice")
            selection(releases)
    elif choice == "2":
        esp.main(['--chip', 'esp32', '--baud', '460800', 'erase_flash'])
    elif choice == "3":
        sys.exit()
    else:
        print("Invalid choice")
        selection(releases)

# Nice CLI title
# Not needed now that we have a GUI
print("-------------------")
print("ESP32 Flashing Tool")
print("-------------------")

# Load the releases.json file that contains what is stable and what is beta
json_file = open("releases.json")
releases = json.load(json_file)

# Boilerplate for the GUI
application = QApplication([])
main_window = QWidget()
main_window.setGeometry(0,0,200,120)
main_window.setWindowTitle("ESP32 Flashing Tool")

def flash(version):
    grab(version)
    print("Flashing version: " + version)
    boot = f"{version}/top-panel-firmware.ino.bootloader.bin"
    bin = f"{version}/top-panel-firmware.ino.bin"
    parts = f"{version}/top-panel-firmware.ino.partitions.bin"
    esp.main(['--chip', 'esp32', '--baud', '921600', '--before', 'default_reset', '--after', 'hard_reset', 'write_flash', '-z', '--flash_mode', 'dio', '--flash_freq', '80m', '--flash_size', '4MB', '0x1000', boot, '0x8000', parts, '0x10000', bin])
    application.quit()

# Adding a file selection button for custom bin filescustom bin files
pathBox = QTextEdit(parent=main_window)
pathBox.setPlaceholderText("Enter a path to dir")
pathBox.setGeometry(0, 60, 200, 30)

# Behavior for the flashing buttons
versionChoice = QComboBox(parent=main_window)
versionChoice.addItem("Stable")
versionChoice.addItem("Beta")
versionChoice.addItem("Custom")
versionChoice.setGeometry(0, 0, 200, 30)

# Flashing button
flashButton = QPushButton(parent=main_window, text="Flash")
flashButton.setGeometry(0, 30, 120, 30)
def version():
    if versionChoice.currentText() == "Stable":
        return releases["stable"]
    elif versionChoice.currentText() == "Beta":
        return releases["beta"]
    else:
        return pathBox.toPlainText()

flashButton.clicked.connect(lambda: flash(version()))

# Adding a erase button
eraseButton = QPushButton(parent=main_window, text="Erase")
eraseButton.move(120, 30)
eraseButton.clicked.connect(lambda: print(esp.main(['--chip', 'esp32', '--baud', '460800', 'erase_flash'])))

drop_zone = DropZone()
drop_zone.setParent(main_window)
drop_zone.setGeometry(0, 90, 200, 30)

# Final GUI calls
main_window.show()
application.exec_()
