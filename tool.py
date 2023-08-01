import sys
import os
import esptool as esp
import json
# Now for the simple class
# We need to create a simple CLI tool for flashing the esp32
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
    esp.main(['--chip', 'esp32', '--baud', '921600', '--before', 'default_reset', '--after', 'hard_reset', 'write_flash', '-z', '--flash_mode', 'dio', '--flash_freq', '80m', '--flash_size', '4MB', '0x1000', boot, '0x8000', parts, '0x10000', bin])

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
            selection()
    elif choice == "2":
        esp.main(['--chip', 'esp32', '--baud', '460800', 'erase_flash'])
    elif choice == "3":
        sys.exit()
    else:
        print("Invalid choice")
        selection()

if __name__ == '__main__':
    print("-------------------")
    print("ESP32 Flashing Tool")
    print("-------------------")
    # Load the releases.json file that contains what is stable and what is beta
    json_file = open("releases.json")
    releases = json.load(json_file)
    selection(releases)