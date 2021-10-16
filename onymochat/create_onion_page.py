#!/usr/bin/env python
from stem.control import Controller
import stem
from stem.process import launch_tor_with_config
import os

# For flask server
from flask import Flask
import logging

# Generating QR
from generate_qr import generate_qr

# Generating keys
import keys_manager

# Some tor tutorials: https://stem.torproject.org/api/control.html
# Tutorial has functions like controller.create_ephemeral_hidden_service
# Python controller for TOR: https://github.com/torproject/stem
# Tor tutorials: https://stem.torproject.org/tutorials/over_the_river.html
# In the above tutorial controller.create_ephemeral_hidden_service is for Onion Service v2 only!
# Tor tutorial - Opening Tor and setting exit-point: https://stem.torproject.org/tutorials/to_russia_with_love.html
# Flask routes tutorial: https://hackersandslackers.com/flask-routes/

# Finding Tor
path = os.path.dirname(os.path.realpath(__file__)) + "/"
dir_path = path + "files/keys/"

# Ports used in configuration for launching Tor.
SOCKS_PORT = 9050
CONTROL_PORT = 9051

server = Flask('Onymochat Webpage Server', template_folder='templates')
# Flask automatically runs on port 5000.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Only log errors. Nothing else.

# Read the index.html file.
html_file = open(path + "onion_webpage/index.html")
html_file_read = html_file.read()


# To print lines while Tor is opening
def print_lines(line):
    if 'Bootstrapped' in line:
        print(line)


# To get messages from base URL of the server
@server.route('/')  # Routing is used to map the specific URL with the associated function
def index():
    return html_file_read


'''
@app.route("/") is a Python decorator that Flask provides to assign URLs in our app to functions easily.
views always conclude with a return statement. Whenever we encounter a return statement in a route, 
we're telling the function to serve whatever we're returning to the user.
This means, when we send a GET request to the server (happens when we simply open the site, or in
hidden_service_query.query when we perform the query), the function under the @server.route gets executed.
Return statement serves whatever we're returning to the user. In simpler words, if we return 'Hello World",
"Hello World" will be added to the index page.

In the above function, if we send a "GET /User1/Hi HTTP/1.1" to the server, the index page will have
"<DATE TIME>#USERNAME#User1#MESSAGE#Hi" written on it.

This was a simple explanation. For better understanding, read this:  https://hackersandslackers.com/flask-routes/
'''


def stop():
    raise Exception("Program Closed")


# Main program below
def create_onion_page():
    tor_path_file = open(path + "files/others/tor_path_file.txt", "r+")
    tor_path = str(tor_path_file.read())

    print('Launching Tor...')

    tor = None  # Initialized tor as None for future use.

    try:
        '''
        tor = launch_tor_with_config(tor_cmd = tor_path, init_msg_handler = print_lines, 
                                     config = {'SocksPort': str(SOCKS_PORT)})

        * The control port is used for controlling Tor, usually via other software like Arm.
        * The Socks port is the port running as a SOCKS5 proxy. This is the one you want to use. 
        * Please note that Tor is not an HTTP proxy, so your script will need to be configured to use a SOCKS5 proxy.
        * Source: https://tor.stackexchange.com/questions/12627/whats-the-difference-between-controlport-and-socksport
        '''
        tor = launch_tor_with_config(tor_cmd=tor_path, init_msg_handler=print_lines,
                                     config={'SocksPort': str(SOCKS_PORT), 'ControlPort': str(CONTROL_PORT)})
        print("Launched Tor successfully!")
    except OSError as exc:
        if (str(exc)).find("Maybe it's not in your PATH") != -1:
            print("'tor' isn't available on your system. Maybe it's not in your PATH."
                  "\nPlease check the Tor project documentation to know how to do it. Or just search it online!"
                  "\nTry to configure Onymochat with Tor from the main menu (if you haven't already)"
                  "\nClosing...")
            stop()
        elif ("doesn't exist" in str(exc)) | \
                ("isn't available on your system" in str(exc)) | \
                ("not the tor executable" in str(exc)):
            print("Error in Tor Path. Please reconfigure Onymochat with Tor from the main menu."
                  "\nClosing...")
            stop()
        else:
            print("%s"
                  "\n\nTor might be already running. "
                  "\nIf the program fails, try the following:"
                  "\n- For Windows:"
                  "\n\t- Check the path to tor.exe. Make sure tor.exe resides in the Tor installation folder "
                  "with a directory structure similar to: Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe"
                  "\n\t- Try killing all previous instances of Tor using Task Manager. "
                  "Press ctrl + alt + delete and open Task Manager. Select Tor and click on End Task."
                  "\n- For Linux: Kill all previous instances of Tor and initiate Tor again."
                  "\n\t- $sudo killall tor"
                  "\n- Check which ports are already in use."
                  "\n\t- Windows: netstat -ano -p tcp"
                  "\n\t- Linux: sudo netstat --all --listening --numeric --tcp"
                  "\n" % exc)
    except Exception as exc:
        print(exc)

    try:
        controller = Controller.from_port()
    except stem.SocketError as exc:
        print("Unable to connect to tor on port " + str(SOCKS_PORT) + ": %s" % exc)
        tor.terminate()  # It is better to send a SIGTERM, since Tor will handle this and ensure it exits cleanly.
        stop()

    controller.authenticate()
    print('Controller authenticated & connected to port ' + str(controller.get_socks_listeners()[0][1]))

    hidden_services = controller.list_ephemeral_hidden_services()  # List of pre-existing hidden services.
    if len(hidden_services) > 0:
        print('Closing %d pre-existing hidden service(s):' % len(hidden_services))

    # CLosing pre-existing hidden services (if any).
    for hidden_service_id in hidden_services:
        controller.remove_hidden_service(hidden_service_id)
        print('- Closed a hidden service with ID %s', hidden_service_id)

    using_saved_keys = True
    onion_page_name = "temporary_page"
    try:
        onion_page_private_key, onion_page_name = keys_manager.save_open_keys(filename="onion_page_private_keys.txt",
                                                                              do_what="deploy",
                                                                              key_type="private key",
                                                                              name_type="onion page",
                                                                              extra_stmt=" (leave empty to create one)")
    except Exception as e:
        using_saved_keys = False
        if str(e) != "Use private key without saving.":
            print("Some error occurred. " + str(e))
        onion_page_private_key = str(input("\nEnter the private key for your onion page (leave empty to create one):"
                                           "\n"))

    if onion_page_private_key == "":
        onion_page_private_key = None

    print('\nInitiating/resuming a hidden service (V3 Onion Service). Please wait...')

    try:
        if onion_page_private_key:  # When user inputs a pre-saved private key.
            hidden_service = controller.create_ephemeral_hidden_service(
                {80: 5000},
                await_publication=True,
                key_type='ED25519-V3',
                key_content=onion_page_private_key,
                detached=True
            )
        else:  # When user doesn't input a pre-saved private key.
            hidden_service = controller.create_ephemeral_hidden_service(
                {80: 5000},
                await_publication=True,
                key_content='ED25519-V3',
                detached=True
            )
        # Flask automatically runs on port 5000. So we are making localhost port 5000 available on onion port 80.
    except stem.ProtocolError as exc:
        if (str(exc)).find("ADD_ONION response didn't have an OK status") != -1:
            print(exc)
            print("Try closing/killing Tor first, then try again later."
                  "\n- For Windows:"
                  "\n\t- Press ctrl + alt + delete and open Task Manager. Select Tor and click on End Task."
                  "\n- For Linux: "
                  "\n\t- $sudo killall tor")
            stop()
        else:
            print("Some error occurred. Error: " + str(exc))
            stop()

    '''
    * key_content='RSA1024' is for Onion services V2. This method doesn't work with Onion version V3.
    * ED25519-V3 is for Onion version V3. But it doesn't support client authentication (probably).
    * The default version of newly created hidden services is based on the HiddenServiceVersion value in your torrc.
    * torrc is located at 'Tor Browser/Browser/TorBrowser/Data/Tor'
    '''

    onion_domain = str(hidden_service.service_id) + '.onion'

    print("")
    print('Successfully initialized a hidden service!')
    print('\nOnion URL of Your Webpage: ' + onion_domain)

    if not onion_page_private_key:
        # For private key
        onion_page_private_key = str(hidden_service.private_key)
        print('\nOnion Page Private Key: ' + onion_page_private_key)
        if using_saved_keys:
            with open(dir_path + "onion_page_private_keys.txt", "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                # Append text at the end of file
                file_object.write(onion_page_private_key)
        generate_qr(onion_page_private_key, "onion_page_private_key_"+onion_page_name)
        # For public key (URL)
        onion_page_url = str(hidden_service.service_id) + ".onion"
        generate_qr(onion_page_url, "onion_page_url_"+onion_page_name)
    else:
        print('\nOnion Page Private Key: ' + onion_page_private_key)

    print('\nSave your private key in a safe place for future use.'
          '\nUsing the private key you can create the .onion web-page with the same URL in future.'
          '\nCAUTION: '
          'If you lose the private key, you will never be able to create the .onion web-page with the same URL again!'
          '\nCAUTION: Do not share your private key with anyone. '
          'Otherwise they too will be able to create the .onion web-page with the same URL as yours!'
          '\n')
    print("The images of the QR codes for your onion page's private key and url are saved in the location " +
          path + "files/qr_codes/")
    print("You can take a print of the images as a backup for future use. Scanning the QR with any QR code scanner "
          "reveals the content.\n")
    print('Server: PRESS CTRL+C TO CLOSE THE SERVER.'
          '\n\nNot closing the server properly might raise other problems in future.'
          '\nYou might have to press CTRL+C several times in order to close the server.\n')

    server.run()  # Running Flask on default port 5000.

    # The Flask server closes when Ctrl + c is pressed. After the server closes, everything else will close too.
    print('Exiting...')
    print('Webserver Closed.')
    controller.remove_ephemeral_hidden_service(hidden_service.service_id)
    print('Removed hidden service from controller.')
    if tor:
        tor.terminate()
        print('Closed Tor.')
    print('Goodbye!')
