import sys
import os
import esptool as esp
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QTextEdit
# Now for the simple class
# We need to create a simple CLI tool for flashing the esp32
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
main_window.setGeometry(0,0,200,200)
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


# Final GUI calls
main_window.show()
application.exec_()
