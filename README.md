# Onymochat

### _Empowering journalists and whistleblowers_

[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)]() [![Python Versions](https://img.shields.io/badge/Python-3.9-blue.svg)](https://github.com/SamratDuttaOfficial/onymochat) [![Release](https://img.shields.io/badge/Release-beta-red.svg)]() [![Testted_On](https://img.shields.io/badge/Tested_On-Windows_|_Linux-brightgreen.svg)]()
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/SamratDuttaOfficial/onymochat) [![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](https://github.com/SamratDuttaOfficial/onymochat)  

Onymochat is an end-to-end encrypted, decentralized, anynomous chat application. You can also host your anonymous .onion webpage with Onymochat.

- Onymochat works over the Tor.
- Anyone can start their own chat server for two users from their own PC.
- It's end to end encrypted.
- It's basically magic. ✨  

## Features

- Start your own chat server for two users from your own PC.
- Users can get connected to the chat server with authentication keys.
- You can launch your chat client and chat with anyone who have your public key and server details (after he/she/they joins the server).
- You can launch your own anonymous .onion webpage with Onymochat. You can use this anonymous website for your journalistic works and whistleblowing.

You don't have to rely upon any third party app to provide you a platform/server to anonymously chat with your friend. You can host your own server and if the person you want to chat with has the server's public key and authentication key, he/she/they can join the server with his/her/their chat client and chat with you. 

Only two people can chat with one server. The chat data is deleted whenever the server is closed. The chat is end to end encrypted, so even if someone hacks into the server somehow, they won't be able to get to know what two people are taling about. It uses 1024 bit RSA keys for encryption. You connect to the chat server over the Tor network, which gives you anonymity. 

## Security

Let's see what makes Onyomochat the most secure chat application (probably):

- End to end 1024 bit RSA encryption for messages.
- Version 3 Onion Service for your .onion webpage.
- Version 2 Onion Service for your chat server.
- Connection to server over the Tor network.

## Installation

### Environment Setup

Onymochat requires [Python 3.9](https://www.python.org/downloads/) or above to run. I have tested it with Python 3.9. Make sure that you have Python added to your PATH. When you install Python in your Windows system, make sure ot check 'Add Python 3.x to PATH'. If you forget to do it, see [this tutorial](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/) to know how to add Python to your PATH for Windows.

#### Install Python

##### For Windows and Mac

Download Python 3.9 from [here](https://www.python.org/downloads/release/python-397/). Use the installer to install Python in your System. Download 'macOS 64-bit universal2 installer' for Mac OS. Download 'Windows x86-64 executable installer' for your Windows 64 Bit system and 'Windows x86 executable installer' for Windows 32 bit system.

##### For Linux

Use the following command to install Python 3.9 on your linux system.

```sh
apt-get install python3.9
```

#### Check pip

Make sure you have pip installed in your system. Use the following command to check if you have pip installed.

```sh
pip --version
```

If you see a message like 'pip 21.2.2' then you have pip installed on your system. Otherwise, follow [this tutorial](https://pip.pypa.io/en/stable/installation/) to install pip in your system. Generally, Python comes with an ensurepip module, which can install pip in a Python environment.

```sh
python -m ensurepip --upgrade
```

### Download Repository

Go to the GitHub repository of Onymochat: https://github.com/SamratDuttaOfficial/onymochat

Click on the green 'Code' button and click on 'Download ZIP' and unzip the archive somewhere to use Onymochat.

Or, use the command below if you have git installed in your system.

```sh
git clone https://github.com/SamratDuttaOfficial/onymochat
```

### Install Requirements

Open up your terminal (CMD on Windows) and go to the folder where you've cloned/unzipped Onymochat. Example:

```sh
cd C:\User\Desktop\Onymochat-master
```

Then install all the requirements from the requirements.txt file.

**Windows:** 

```
pip install -r requirements.txt
```

**Linux and Mac OS:**

```
pip3 install -r requirements.txt
```

**If you're on Linux**, you might need to install Tkinter separately in the following way:

```sh
sudo apt install python3-tk
```

This will install all of the requirements, except Tor.

#### Install Tor

Download and install Tor browser from the official Tor Project website: https://www.torproject.org/download/

Take a note of where you're installing Tor/Tor Browser, it will be required later.

### How to Use

After installation, open the 'onymochat' subdirectory in your terminal. This directory should have a file like ```run_onymochat.py```. Run this file.

```sh
python run_onymochat.py
```

If you are on linux, run that file using the following command instead:

```sh
python3 run_onymochat.py
```

This will run the onymochat program in your terminal. This will greet you with a menu. Just input the number of the option you want to go to, and hit the enter button.

First, configure Onymochat with Tor. 

#### Configure Onymocaht with Tor

Run the program and go to option 0 (zero).

Then, on the next prompt, enter the path to tor.exe in the TorBrowser folder. This is important to configure Onymochat with Tor. You have to do this step only once after installation. Paste the path to tor.exe in the TorBrowser (or any similar name) folder.

Example (For Windows): ```C:\user\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe```

Example (For Mac): ```Applications\TorBrowser.app\Tor\tor.real```

Linux users just write `'tor'` without the quotations.

**Now you are ready to use Onymochat**

#### Things You Can Do

Here are all the things you can do with Onymochat.

1. Create new hidden service and chat server
2. Generate encryption keys for chat
3. Run chat client
4. Create onion webpage
5. Generate QR codes for chat server
6. Generate QR codes for onion page
7. Generate QR codes for your encryption keys

#### How to Chat?

Here are some steps you need to follow to chat with someone through Onymochat.

**CAUTION: NEVER SHARE ANY OF YOUR PRIVATE KEYS WITH ANYONE**

##### Step 1

First, select option **1** to create a new **hidden service and server** and follow the instructions given in your terminal/command window. This will be the server where the chat data will be temporarily saved (all chat data will be lost when the hidden service and server is closed). You can press Ctrl + C to close this **hidden service and server** when you are done chatting.

Then, share the hidden service public key and authentication key with someone you want to chat with. You can do it in person by meeting that person, or though any other communication mehtod. You can use the same hidden service (same public key and authentication key) to chat with multiple persons but this comes with the risk of sharing the same keys with everyone, and someone might use them later to spam you. Or, **the other person, with whom you want to chat with, can provide you his/her/their hidden service public key and authentication key** and you can use it too.

##### Step 2

Select option **2** to generate encryption keys for your chat. You need to share your public key with any person you want to chat with. 

##### Step 3

Select option **3** to run your chat client. There you won't need to create any new encryption keys for chatting if you don't want to. Creating more than one keys will be very hard to manage and might be the reason of some problems in future.

You will need to enter your or the other person's hidden service and server's **public key** and **authenticaion key** and also the other person's **public key for encryption** to chat with that person.

#### How to Create an Anonymous (.onion) Webpage

##### Step 1

In the 'onymochat' directory, go to the 'onion_webpage' directory. Edit the **index.html** HTML according to your preference. This will be the page for your anonymous webpage.


##### Step 2

Select option **4** from the main menu. You can generate a new URL for your .onion webpage and save the private key of that webpage to resume the webpage later with the same URL. Or, you can use a pre-saved private key to resume your website with a perticular URL you've generated before. 
#### Generate QR Codes for Encryption Keys

Option **4**, **5**, **6**, and **7** is to generate QR codes for different keys used in Onymochat. This QR codes are saved in ```\files\qr_codes```. You can print them and share with other people you want to communicate with. 

#### Exit Program

Exit the program by selecting option **8** from the main menu. 

---

## Author

Created by Samrat Dutta

Github: https://github.com/SamratDuttaOfficial

Linkedin: https://www.linkedin.com/in/SamratDuttaOfficial

Buy me a coffee: https://www.buymeacoffee.com/SamratDutta

---

## Github

Please visit the Github repository to download Onymochat and see a quick tutorial.

https://github.com/SamratDuttaOfficial/onymochat

Pull requests are always welcome.

