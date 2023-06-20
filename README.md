# Cybr473 Keylogger
***

## Name
Delilah keylogger

## Description
This is a Python-based keylogger that captures and logs keystrokes on a computer. It runs in the background, recording all the keys pressed by the user and storing them in a log file. 

## Features
* Captures keystrokes from the keyboard
* Logs the captured keystrokes in a text file
* Runs in the background without interfering with the user's activities
* Stealth mode: the keylogger operates silently without any visible indication to the user
* Supports recording of special keys, such as function keys and modifier keys (Ctrl, Alt, Shift)
* Simple and lightweight implementation

## Usage
For educational purposes only, as per Victoria University class CYBR473 Assignment 3

## Disclaimer
Please note that the usage of this keylogger may be subject to legal restrictions. It is your responsibility to comply with applicable laws and regulations before using this software. The author assumes no liability for any misuse or unlawful use of this keylogger.

## Authors and acknowledgment
Liv Fletcher

## Project status
In development

## Next Steps
# Essential 
- [ ] [5%] Data encoding Implement decoding/encoding strategies
- [ ] [5%] Package file, Convert to executable
- [ ] [5%] Send Exploit, Build a social engineering exploit & send to professor
# Completion 50%
This should be attempted only when you have finished all the Core parts. The intention here is to apply techniques to make your malware stealthier and evade network detection. The defender's aim is to locate the malware infection and develop countermeasures against it. In particular: 
- [ ] The defender will collect packet traces from the network and use the traffic analysis to identify the infected hosts via their data exfiltration and beaconing.   
* **My interpretation:** All packets being sent to/from the server will be ecnrypted and 'blend' in with 'normal' net traffic, indistinguishable in tools such as Wireshark.
- [ ] From the collected packet traces, apply brute-force attacks on any encoding schemes that are identified to work out the key.  
* **My interpretation:** Current implementation uses a XOR encryption, however this maybe quite easy to brute force. If this proves simple to brute force in demonstration, I will attempt to employ a more difficult encryption method.
I include a more complex method to test this implementation.
- [ ] From the collected packet traces, identify HTTP artifacts that might suggest that it is not an actual browser but malware communicating with command-and-control server (so it can develop network signatures to block its traffic at the network gateway).  
* **My interpretation:** To attempt to ensure the packets sent to/from the server, I will employ a useragent so that the packets contain a 'full header' information so it appears like all other packets.
- [ ] Identify the location of the command-and-control server so a takedown request can be actioned.  
* **My interpretation:** When the packets are being properly encrypted, the traffic will not portray the location of the server.
- [ ] Spoof the C&C server itself to send shutdown commands to all hosts on the network to try and deactivate the malware.   
* **My interpretation:** Adding to encrypted communications, I believe adding an authentication page to my flask server will ensure no other actors are allowed access.
- [ ] Reboot the client machines so that the malware will be forced to shut down.   
* **My interpretation:** I will add the logger to the registry so that it automatically starts up on boot.
- [ ] Look for evidence of keylog data files on client machines.   
* **My interpretation:** I will ensure that after the gathered keylog data gets removed from the clients system, and leaves no remnants behind. (straight delete, no evidence in reycle bin etc)
- [ ] Say the defender has managed to identify the machine that is infected and has a copy of your malware. You know that they are likely to use IDA-pro for disassembly to analyse your malware.   
* **My interpretation:** Obfuscation method where I will load the logger executable with a packer (UPX) so disassembly tools such as IDA Pro cannot be used.
- [ ] They may also run your malware executable in a debugger for analysis.  
* **My interpretation:** Like above, I intend to load the logger with a packer (UPX) so debugger tools such as OllyDBG cannot be used.
- [ ] They will analyse your malware in a virtual machine such as VirtualBox.     
* **My interpretation:** Obfuscation method where the logger to sleeps if a VirtualMachine enviroment has been detected.

