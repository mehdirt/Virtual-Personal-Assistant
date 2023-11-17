import os
import subprocess as sp

# TODO: We can use PATHLIB library instead.
# You can add every path for every software
paths = {
    'notepad': "<Your File Path>",
    'discord': "C:\\Users\\mehdi\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe", # Example
    'calculator': "<Your File Path>"
}

# You can add any function to add
def open_camera() -> None:
    """Opens the device camera"""
    sp.run('start microsoft.windows.camera:', shell=True)

def open_notepad() -> None:
    """Opens notepad from the determined path"""
    os.startfile(paths['notepad'])

def open_discord() -> None:
    """Opens discord from the determined path"""
    os.startfile(paths['discord'])

def open_cmd() -> None:
    """Opens windows cmd"""
    os.system('start cmd')

def open_calculator() -> None:
    """Opens system calculator from the determined path"""
    sp.Popen(paths['calculator'])