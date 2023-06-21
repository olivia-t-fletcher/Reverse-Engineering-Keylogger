# CYBR473 Assignment 3: Build your own Malware
***

## Abstract
Assessment 3 is worth 40% of the overall grade. It involves implementing a remotely controlled keylogger and demonstrating that it works as intended.

## Assignment Goals
The goal of this assignment is to build a proof-of-concept malware that demonstrates your ability to think like an attacker and knowledge of the technical issues introduced in the lectures

## Assignment Criteria
This assignment has "Essential" and "Completion" parts. 
The assignment will be marked out of 100. The breakdown of the mark is as follows:
- [x] The Core part has 50% worth. The specific contribution of each requirement is specified in the task description. Note that you should complete this part first. You can only "unlock" the remaining 50% if you have accomplished the first part, specially, the tasks that are described with the keyword must.
- [x] The Completion part carries the remaining 50%. For this part, you will be presented with a list of actions potentially taken by a defender. You should interpret what you can incorporate in the malware to resist against that action and implement it.
  - The first correct mechanism to address each defensive action carries 5% (1% for the idea and 4% for the correct implementation).
  - For each defensive action, there may be multiple "independent" mechanisms that the malware can implement to make the defense harder. However, only your first mechanism carries 5% and any subsequent ones you implement will only carry 2% each. 

## Core [50%]
This part covers the basic principles related to malware functionality and how malware hides itself.

### Command and control architecture [10%]
You must implement the following commands:
* sleep id n: puts the malware id to sleep for n minutes.
* shutdown id: causes the malware id to shut itself down.
* delete id: makes the malware delete any logs collected so far. 

### Keylogging [10%]
Your malware must implement a keylogger. It should also convert unprintable characters into printable equivalents to make it easier to read the keylog file. For example, map the "Page Down" key to [PAGE DOWN]. 

### Exfiltration [5%]
Your malware should periodically upload the keylog file to the command-and-control server and delete the keylog file. It should only delete the keylog file after checking that it has been uploaded correctly.

### Data encoding [5%]
Your malware should implement encoding and decoding strategies to hide data in-memory, on-disk, and when sent over the network. So the data here includes strings within the malware as well as the data being exfiltrated, commands, etc.

You should implement the NULL XOR encryption from the book and lectures. The encryption key is one byte long and pre-assigned (hard-coded). 

### Beaconing [5%]
Your malware should use "beacons" to indicate that the malware is alive, functioning and ready for instructions. For the Core, it is sufficient to beacon at a regular time period of your choice. When the command-and-control server lists infected hosts, it should use this information to indicate whether each victim is believed to be active or inactive. 

### Package as Executable [5%]
You must package your malware as a standalone binary (compiled for a 32-bit Windows OS). 

### Phishing Email [5%]
You should prepare a "phishing" email aimed at [proff-name] that is designed to have the victim run it (which will then install itself).

## Completion [50% overall] 
This should be attempted only when you have finished all the Core parts. The intention here is to apply techniques to make your malware stealthier and evade network detection. The defender's aim is to locate the malware infection and develop countermeasures against it. In particular: 
* The defender will collect packet traces from the network and use the traffic analysis to identify the infected hosts via their data exfiltration and beaconing. 
* From the collected packet traces, apply brute-force attacks on any encoding schemes that are identified to work out the key.
* From the collected packet traces, identify HTTP artifacts that might suggest that it is not an actual browser but malware communicating with command-and-control server (so it can develop network signatures to block its traffic at the network gateway). 
* Identify the location of the command-and-control server so a takedown request can be actioned. 
* Spoof the C&C server itself to send shutdown commands to all hosts on the network to try and deactivate the malware. 
* Look for evidence of keylog data files on client machines. 
* Say the defender has managed to identify the machine that is infected and has a copy of your malware. You know that they are likely to use IDA-pro for disassembly to analyse your malware. 
* They may also run your malware executable in a debugger for analysis. 
* They will analyse your malware in a virtual machine such as VirtualBox. 
Implement counter-mechanisms to resist against each of this defense actions (to make their job more difficult). Note that for some of these tasks, although you can rely on the material from the book for ideas, the actual implementation may need some experimentation and further research. We are interested in your depth of exploration and your failures as well as your successes. 
