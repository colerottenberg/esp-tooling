"""
This tool was built by Cole Rottenberg(cole@bluevigil.com) for Blue Vigil
This is a tool for flashing the esp32 with the latest firmware. It is desgined to flash the top panel on the ALED using a dropdown however, any esp32 can be flashed using the custom drop box option
To operate this tool, simply run the script and select the version you want to flash. Then click the flash button. 
The button will turn red while flashing and green when finished. If you want to erase the esp32, click the erase button.
ESP32 must be plugged in before running this tool
"""
import sys, os, json, esptool as esp
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QComboBox,
    QLabel,
    QVBoxLayout,
)  # Now for the simple class
from PyQt5.QtGui import (
    QPalette,
    QColor,
)

# We need to create a simple CLI tool for flashing the esp32
# This is LLM generated so all creds go to those countless stack overflow posts
class DropZone(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.label = QLabel("Drop a folder of \nbinary here...", self)

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
        self.label.setText(f"File path: {file_path}")
        print(f"File path: {file_path}")
        flashCaller(file_path)


# GLOBALS SECTION:

# Json release file parsed into a dict
# Load the releases.json file that contains what is stable and what is beta
json_file = open("releases.json")
releases = json.load(json_file)

# Boilerplate for the GUI
application = QApplication([])
main_window = QWidget()
main_window.setGeometry(0, 0, 200, 210)
main_window.setWindowTitle("ESP32 Flashing Tool")

# Adding a Done/Finished Widget for after flashing
done_window = QWidget()
done_window.setGeometry(0, 0, 180, 60)
done_window.setWindowTitle("Done")
done_message = QLabel(parent=done_window, text="Finished Operation")
ok_button = QPushButton(parent=done_window, text="OK")
ok_button.move(30, 30)
ok_button.clicked.connect(lambda: application.quit())

# Adding a file selection button for custom bin filescustom bin files
# pathBox = QTextEdit(parent=main_window)
# pathBox.setPlaceholderText("Enter a path to dir")
# pathBox.setGeometry(0, 60, 200, 30)

# Behavior for the flashing buttons
versionChoice = QComboBox(parent=main_window)
versionChoice.addItem("ALED Stable")
versionChoice.addItem("ALED Beta")
versionChoice.setGeometry(0, 0, 200, 30)

# Flashing button
flashButton = QPushButton(parent=main_window, text="Flash")
flashButton.setGeometry(0, 30, 120, 30)

# FUNCTION SECTION:
# This is where we define all the functions that will be called by the buttons

# grabs version from box and checks json
def version():
    if versionChoice.currentText() == "ALED Stable":
        return releases["stable"]
    elif versionChoice.currentText() == "ALED Beta":
        return releases["beta"]
    else:
        raise Exception("Invalid version")


flashButton.clicked.connect(lambda: flashCaller(version()))

# Adding a erase button
eraseButton = QPushButton(parent=main_window, text="Erase")
eraseButton.move(120, 30)
eraseButton.clicked.connect(lambda: eraseCaller())

drop_zone = DropZone()
drop_zone.setParent(main_window)
drop_zone.setGeometry(0, 60, 200, 120)

# Now we define all function calls
def grab(version):
    print("Grabbing version: " + version)
    # Grab specific version bins from local repo or from github
    # Check if version exists in local repo
    ex = f"gh release download {version}  -D ./{version} --repo BlueVigil/top-panel-firmware"
    os.system(ex)
    # If it can enter the directory, then it exists


def flash(version):
    grab(version)
    print("Flashing version: " + version)
    boot = f"{version}/top-panel-firmware.ino.bootloader.bin"
    bin = f"{version}/top-panel-firmware.ino.bin"
    parts = f"{version}/top-panel-firmware.ino.partitions.bin"
    esp.main(
        [
            "--chip",
            "esp32",
            "--baud",
            "921600",
            "--before",
            "default_reset",
            "write_flash",
            "-z",
            "--flash_mode",
            "dio",
            "--flash_freq",
            "80m",
            "--flash_size",
            "4MB",
            "0x1000",
            boot,
            "0x8000",
            parts,
            "0x10000",
            bin,
        ]
    )


def flashCaller(version):
    # This will call the flash function with the version as well as quit the application and color the button
    palette = flashButton.palette()
    palette.setColor(QPalette.ButtonText, QColor("red"))
    flashButton.setPalette(palette)
    flash(version)
    palette.setColor(QPalette.ButtonText, QColor("green"))
    flashButton.setPalette(palette)
    done_window.show()


def eraseCaller():
    esp.main(["--chip", "esp32", "--baud", "460800", "erase_flash"])
    done_window.show()

# Nice CLI title
# Not needed now that we have a GUI
print("-------------------")
print("ESP32 Flashing Tool")
print("-------------------")

# EXE the App
main_window.show()
application.exec_()
print("Exiting...")
