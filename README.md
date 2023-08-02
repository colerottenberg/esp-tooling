# ESP Flashing & Erasing Tool for the Top Panel Firmware

## Requirements
This tool requires the use of the Github CLI and an authenticated Github account. You can install the Github CLI [here](https://cli.github.com/). You can authenticate your Github account by running `gh auth login` in the terminal. You can also use the Github CLI to authenticate with a personal access token. You can find more information about that [here](https://cli.github.com/manual/gh_auth_login). However, to use the tool without the Github CLI, you can manually place the expected binary directories with the repository directory and confirm their names are matching with is expected with the `releases.json` file.

## Installation
Clone the repository and install the dependencies:
```
git clone https://github.com/colerottenberg/esp-tooling
```
Now install the dependencies:
```
pip install -r requirements.txt
```
Or
```
python3 -m pip install -r requirements.txt
```
It is also recommended to install these dependencies in a virtual environment. using `virtualenv` or `venv`.

## Usage
```
python3 tool.py
```
Menu options include flashing the firmware, erasing the flash, and setting a custom path to the firmware binary directorty.
Either absolute or relative paths can be used. If the path is invalid, the tool will crash. The binary directory needs to contain the `top-panel-firmware.bootloader.bin` file, the `top-panel-firmware.partitions.bin` file, and the `top-panel-firmware.bin` file. 

## Versioning
The preset firmware versions are v3.1.6 as stable, and v1.1.8 as beta. When new versions are released, the tool will be updated to include them. The tool grabs the stable and beta versions from the `releases.json` file in the repository. If you want to add a new version, you can do so by changing an entry to the `releases.json` file. The tool will automatically detect the new version and will use that version instead of the previous version.