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

        generate_qr(public_key_str, "encryption_public_key")

        print("The image of the QR code for your chat client's new public key is saved in the "
              "location " + path + "files/qr_codes")
        print("You can take a print of the image to share it with someone. Scanning the QR with any QR code scanner "
              "reveals the content.")
    except:
        print("No saved keys found. Run the chat client to generate new encryption keys.\n")


def generate_other_key_qr():
    qr_name = input("Enter the name of the QR: ")
    qr_content = input("Input the key/string to generate a QR code from: ")

    try:
        generate_qr(qr_content, qr_name)
        print("\nThe images of the QR codes are saved in the location " + qr_path)
        print("You can take a print of the images as a backup for future use. Scanning the QR with any QR code scanner "
              "reveals the content.\n")
    except Exception as e:
        print("Some error occurred! Error: " + e + "\n")

