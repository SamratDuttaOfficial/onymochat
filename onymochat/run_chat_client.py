import gc
import threading
import datetime
from random import random
from hidden_service_query import QueryHiddenService
from stem.control import Controller
import stem
from stem.process import launch_tor_with_config
import os
import time
import tkinter
import tkinter.scrolledtext
import crypto

# extra
import socks  # SocksiPy module
import socket

# sys.tracebacklimit = 0
# Hiding traceback errors, cause it throws a traceback error every time we throw an exception in the stop() function.

path = os.path.dirname(os.path.realpath(__file__)) + "/"
dir_path = path + "files/keys/"

SOCKS_PORT = 9050
CONTROL_PORT = 9051
global tor
tor = None

user_sep = '#USERNAME#'  # User separator.
msg_sep = '#MESSAGE#'  # Message separator.
line_sep = '#NEW_LINE#'  # Line separator.
timestamps = []
special_keywords = [user_sep, msg_sep, line_sep, '\n']

global gui_done
global running
global window, chat_label, text_area, msg_label, input_area, send_button, connected_label
global user
global public_key, private_key, others_public_key
global urllib_query
global controller
global disconnected
stop_thread = False
disconnected = True


def print_lines(line):
    if 'Bootstrapped' in line:
        print(line)


def update_chat(messages):
    global text_area
    global timestamps

    new_messages = []  # Starting with a fresh list every time.
    for message in messages:
        if message:
            try:
                time_sent, username_and_text = message.split(user_sep)
                if time_sent not in timestamps:
                    timestamps.append(time_sent)
                    username, text = username_and_text.split(msg_sep)
                    time_sent = time_sent[:-10]  # Cutting off extra stuffs.
                    if username != user:
                        text = crypto.decrypt(text, private_key)
                        text = text[:-4]  # Last 4 characters are just for a new line.
                        new_messages.append('[' + str(time_sent) + '] ' + str(username) + ': ' + str(text))
            except ValueError as error:
                if "Incorrect decryption" not in str(error):
                    print('Error: %s' % error)

    if gui_done:
        text_area.config(state='normal')
        for new_message in new_messages:
            text_area.insert('end', new_message + "\n")
        text_area.yview('end')
        text_area.config(state='disabled')


def insert_sent(message):
    global text_area
    global timestamps

    time_sent = str(datetime.datetime.now())
    time_sent = time_sent[:-10]  # Cutting off extra stuffs.
    message = message[:-4]  # Last 4 characters are just for a new line.
    new_message = '[' + str(time_sent) + '] ' + str(user) + ': ' + str(message)

    if gui_done:
        text_area.config(state='normal')
        text_area.insert('end', new_message + "\n")
        text_area.yview('end')
        text_area.config(state='disabled')


def insert_text(message, newline=True):
    global text_area

    if gui_done:
        text_area.config(state='normal')
        if not newline:
            text_area.delete("end-1l", "end")
        text_area.insert('end', "" + message + "\n")
        text_area.yview('end')
        text_area.config(state='disabled')


def send():
    global input_area
    global others_public_key
    global urllib_query
    global disconnected

    # To see how urllib queries are used to send messages see the run_hidden_service_and_serve.py file.
    message = input_area.get('1.0', 'end')  # this means get the whole text
    for keywrd in special_keywords:
        message = message.replace(keywrd, ' ... ')  # Remove special keywords.

    if len(message) >= 80:
        # print("Input text is too long. Maximum allowed length is 80 characters (a new line is 5 characters long).")
        insert_text("Maximum allowed length is 80 characters (a new line is 5 characters long).")
        return

    enc_success = True
    try:
        enc_message = crypto.encrypt(message, others_public_key)  # encrypted with the other person's public key.
    except ValueError as e:
        print("The public key of the person you want to chat with is probably not a valid key."
              "\nPlease enter a valid public key.")
        enc_success = False

    if not enc_success:
        stop()

    route = '/%s/%s' % (user, enc_message)  # route is like '/<username>/<message_sent>'
    if not disconnected:
        messages_string = urllib_query.query(route)
        if 'Unable to reach' in messages_string:
            disconnected = True
            if running:
                # Sometimes running becomes false and still it gets printed. So check it beforehand.
                print("Unable to reach the server. Make sure the hidden service is still running on the host computer.")
            check_count = 0
            while check_count < 10:
                if running:
                    # Sometimes running becomes false and still it gets printed. So check it beforehand.
                    print('Retrying...')
                    insert_text("Failed to send. Reconnecting...")
                    messages_string = urllib_query.query()
                if 'Unable to reach' in messages_string:
                    check_count = check_count + 1
                    time.sleep(2)
                    continue
                else:
                    disconnected = False
                    if running:
                        # Sometimes running becomes false and still it gets printed. So check it beforehand.
                        print('Connected.')
                        insert_text("Connected", newline=False)
                    break
            if check_count >= 10:     # After checking for 10 times
                if disconnected:
                    print("Unable to reach server. Some error occurred. Try again later.")
                    stop()
        else:
            insert_sent(message)
            input_area.delete('1.0', 'end')  # Clean the input area.


def receive():
    global running
    global urllib_query
    global disconnected
    global gui_done

    while running:
        messages_string = urllib_query.query()
        if 'Unable to reach' in messages_string:
            disconnected = True
            if running:
                # Sometimes running becomes false and still it gets printed. So check it beforehand.
                print("Unable to reach the server. Make sure the hidden service is still running on the host computer.")
                if "Query Error:":
                    print(messages_string)
            check_count = 0
            while check_count < 10:
                if running:
                    # Sometimes running becomes false and still it gets printed. So check it beforehand.
                    print('Retrying...')
                    insert_text("Disconnected. Retrying... (Please Wait)")
                    messages_string = urllib_query.query()
                if 'Unable to reach' in messages_string:
                    check_count = check_count + 1
                    time.sleep(10)
                    continue
                else:
                    disconnected = False
                    if running:
                        # Sometimes running becomes false and still it gets printed. So check it beforehand.
                        print('Connected.')
                        insert_text("Connected")
                        messages = messages_string.split(line_sep)
                        update_chat(messages)
                    break
        else:
            disconnected = False
            messages = messages_string.split(line_sep)
            update_chat(messages)
            time.sleep(1)


def gui_loop():
    global tor
    global gui_done
    global window, chat_label, text_area, msg_label, input_area, send_button, connected_label
    global running

    try:
        window = tkinter.Tk()
        window.configure(bg="lightgray")
        window.title('Onymochat')

        chat_label = tkinter.Label(window, text="Onymochat - Anonymous chatroom", bg="Lightgray")
        chat_label.config(font=("Arial", 12))
        chat_label.pack(padx=20, pady=5)

        text_area = tkinter.scrolledtext.ScrolledText(window)
        text_area.pack(padx=20, pady=5)
        text_area.config(state='disabled')

        msg_label = tkinter.Label(window, text="Type your message below", bg="Lightgray")
        msg_label.config(font=("Arial", 12))
        msg_label.pack(padx=20, pady=5)

        input_area = tkinter.Text(window, height=3)
        input_area.pack(padx=20, pady=5)

        send_button = tkinter.Button(window, text="SEND", bg="lightgray", command=send)
        send_button.config(font=("Arial", 12))
        send_button.pack(padx=20, pady=5)

        connected_label = tkinter.Label(window, text="The 'Send' button is disabled when you're disconnected.", bg="Lightgray")
        connected_label.config(font=("Arial", 8))
        connected_label.pack(padx=20, pady=5)

        gui_done = True

        window.protocol("WM_DELETE_WINDOW", stop)
        window.mainloop()
        # signal.signal(signal.SIGINT, stop)  # To handle ctrl+c

    except KeyboardInterrupt:
        stop()
    except RuntimeError:
        stop()
    except Exception as e:
        print("Error: " + e)
        stop()


def stop():
    global running
    global window
    global gui_done
    global controller

    print('Closing...')
    running = False
    try:
        if window:
            window.destroy()
            window = None  # Make the window none to help the garbage collector.
            print('Window closed.')
    except NameError:
        print("No window to be closed.")
    gui_done = False
    controller.reset_conf()
    print('Controller reset.')
    socks.setdefaultproxy()  # Resetting default proxy
    if tor:
        tor.terminate()
        print('Closed Tor.')
    print('Goodbye.')

    gc.collect()  # Garbage collector
    # exit(0)
    raise Exception("Program Closed")


def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]


def run_chat_client():
    global gui_done
    global running
    global private_key, public_key, others_public_key
    global user
    global urllib_query
    global controller
    global tor

    socks.setdefaultproxy()     # Resetting default proxy

    tor_path_file = open(path + "files/others/tor_path_file.txt", "r+")
    tor_path = str(tor_path_file.read())

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
    except OSError as exc:
        if (str(exc)).find("Maybe it's not in your PATH") != -1:
            print("'tor' isn't available on your system. Maybe it's not in your PATH."
                  "\nPlease check the Tor project documentation to know how to do it. Or just search it online!"
                  "\nTry to configure Onymochat with Tor from the main menu (if you haven't already)."
                  "\nClosing...")
            stop()
        elif (str(exc)).find("doesn't exist") != -1 | (str(exc)).find("isn't available on your system") != -1:
            print("Error in Tor Path. Please reconfigure Onymochat with Tor from the main menu."
                  "\nClosing...")
            stop()
        else:
            print("%s"
                  "\nTor might be already running. "
                  "\nIf the program fails, try the following:"
                  "\n- For Windows:"
                  "\n\t- Check the path to tor.exe. Make sure tor.exe resides in the Tor installation folder "
                  "with a directory structure similar to: Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe"
                  "\n\t- Try killing all previous instances of Tor using Task Manager. "
                  "Press ctrl + alt + delete and open Task Manager. Select Tor and click on End Task."
                  "\n- For Linux: Kill all previous instances of Tor and initiate Tor again."
                  "\n\t- $sudo killall tor"
                  "\n\t- $tor"
                  "\n- Check which ports are already in use."
                  "\n\t- Windows: netstat -ano -p tcp"
                  "\n\t- Linux: sudo netstat --all --listening --numeric --tcp"
                  "\n" % exc)
    except Exception as exc:
        print(exc)

    controller = Controller.from_port()
    controller.authenticate()

    socks_port = SOCKS_PORT

    # Set socks proxy and wrap the urllib module
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', socks_port)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo


    try:
        public_key, private_key = crypto.import_keys()
    except:  # For any exception, not just FileNotFoundError
        try:
            public_key, private_key = crypto.generate_keys()
        except Exception as e:
            if "Error in generate_keys" in str(e):
                print("An error occurred. Make sure you have entered a correct private key generated by Onymochat.")
                stop()

    hidden_service_id = input("Hidden Service Public Key: ")
    hidden_service_auth = input("Authentication Key: ")

    try:
        controller.set_conf('HidServAuth', '%s.onion %s' % (hidden_service_id, hidden_service_auth))
    except stem.InvalidRequest:
        print('Failed to configure client authorization for hidden services. '
              '\nMake sure the information you entered are correct.')
        stop()

    user = input("Your username: ")
    if user == "":
        user = "User" + random(100, 500)

    others_public_key = input("Input the public key of the person you want to chat with:\n")

    domain = hidden_service_id + '.onion'
    urllib_query = QueryHiddenService(domain, socks_port)

    gui_done = False
    running = True

    # gui_thread = threading.Thread(target=gui_loop)    # We have to run tkinter in main thread only.
    receive_thread = threading.Thread(target=receive)  # We are running this in a different thread, as infinite loop.
    receive_thread.daemon = True  # die when the main thread dies. VERY IMPORTANT!

    print('\nStarting...'
          '\nPlease close the chat window using the X button on top-right corner only!\n')

    # gui_thread.start()
    receive_thread.start()

    gui_loop()  # Running this function in the main thread.
    # Main thread is just the thread from where the program started. Here's it's just the main function.
