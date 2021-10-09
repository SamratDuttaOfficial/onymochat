import os
import pyqrcode
from PIL import Image

path = os.path.dirname(os.path.realpath(__file__)) + "/"
dir_path = path + "files/keys/"
qr_path = path + "files/qr_codes/"


def generate_qr(s, image_name):
    image_path = qr_path + image_name + ".png"
    # Generate QR code
    url = pyqrcode.create(s)
    url.png(image_path, scale=8)

    # im = Image.open(image_path)
    # im.show()


def generate_encryption_keys_qr():
    try:
        public_key = open(dir_path + 'my_public_pem.pem', 'r').read()
        public_key_str = str(public_key).replace("\n", "#N#")
        public_key_str = (str(public_key_str))[26:-24]

        private_key = open(dir_path + 'my_private_pem.pem', 'r').read()
        private_key_str = str(private_key).replace("\n", "#N#")
        private_key_str = (str(private_key_str))[31:-29]

        generate_qr(public_key_str, "encryption_public_key")
        generate_qr(private_key_str, "encryption_private_key")
        print("\nThe images of the QR codes are saved in the location " + qr_path)
        print("You can take a print of the images as a backup for future use. Scanning the QR with any QR code scanner "
              "reveals the content.\n")
    except:
        print("No saved keys found. Run the chat client to generate new encryption keys.\n")


def generate_hidden_service_qr():
    try:
        hidden_service_private_key_file = open(dir_path + "hidden_service_private_key.txt", "r+")
        hidden_service_private_key = str(hidden_service_private_key_file.read())

        hidden_service_public_key_file = open(dir_path + "hidden_service_public_key.txt", "r+")
        hidden_service_public_key = str(hidden_service_public_key_file.read())

        hidden_service_authentication_key_file = open(dir_path + "hidden_service_authentication_key.txt", "r+")
        hidden_service_authentication_key = str(hidden_service_authentication_key_file.read())

        generate_qr(hidden_service_private_key, "hidden_service_private_key")
        generate_qr(hidden_service_public_key, "hidden_service_public_key")
        generate_qr(hidden_service_authentication_key, "hidden_service_authentication_key")
        print("\nThe images of the QR codes are saved in the location " + qr_path)
        print("You can take a print of the images as a backup for future use. Scanning the QR with any QR code scanner "
              "reveals the content.\n")
    except:
        print("No saved keys for the chat server found. Create a new hidden service and chat server to generate keys\n")


def generate_onion_page_qr():
    try:
        onion_page_private_key_file = open(dir_path + "onion_page_private_key.txt", "r+")
        onion_page_url_file = open(dir_path + "onion_page_url.txt", "r+")
    except FileNotFoundError:
        print("No saved keys for the onion page found. Create a new onion page to generate keys")
        return

    try:
        onion_page_private_key = str(onion_page_private_key_file.read())
        onion_page_url = str(onion_page_url_file.read()) + ".onion"
        # Generate QR
        generate_qr(onion_page_private_key, "onion_page_private_key")
        generate_qr(onion_page_url, "onion_page_url")
        print("\nThe images of the QR codes are saved in the location " + qr_path)
        print("You can take a print of the images as a backup for future use. Scanning the QR with any QR code scanner "
              "reveals the content.\n")
    except Exception as e:
        print("Some Error Occurred\n" + e)
        return
