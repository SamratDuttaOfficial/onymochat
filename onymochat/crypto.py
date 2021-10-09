# Importing necessary modules
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os

# pycryptodome documentation: https://pycryptodome.readthedocs.io/en/latest/src/cipher/oaep.html
# Asymmetric Cryptography Tutorial: https://medium.com/@ashiqgiga07/asymmetric-cryptography-with-python-5eed86772731
from generate_qr import generate_qr

path = os.path.dirname(os.path.abspath(__file__)) + "/"
dir_path = path + "files/keys/"


def generate_key(private_key_input):
    if not private_key_input:
        # Generating private key (RsaKey object) of key length of 1024 bits
        private_key = RSA.generate(1024)
        # Generating the public key (RsaKey object) from the private key
        public_key = private_key.publickey()

        private_pem = private_key.export_key().decode()
        with open(dir_path + 'my_private_pem.pem', 'w') as pr:
            pr.write(private_pem)

        public_pem = public_key.export_key().decode()
        with open(dir_path + 'my_public_pem.pem', 'w') as pu:
            pu.write(public_pem)

        public_key_str = str(public_key.exportKey()).replace("\\n", "#N#")
        public_key_str = (str(public_key_str))[28:-25]

        private_key_str = str(private_key.exportKey()).replace("\\n", "#N#")
        private_key_str = (str(private_key_str))[33:-30]

        # In run_chat_client.py and generate_qr.py, the trimming range is different and we replace "\n" with "#N#".
        # Because the string starts with "b'" adn ends with "'", and "\n" exists as characters, not new lines.
        # So we replace "\\n" with "#N#" because "\\n" is actually "\n" in characters, not a new line.

        print("\nYour Public Key:\n\n" + public_key_str)
        print("\nYour Private Key:\n\n" + private_key_str)
        print("\nSave these keys in a safe place. "
              "\nIf you lose these keys, your contacts may never be able to contact you again!"
              "\nIf you lose these keys, you will not be able to decrypt messages encrypted with the public key."
              "\nNever share your private key with anyone under any circumstance!"
              "\nAnyone with your private key might be able to read your messages."
              "\nOnly share your public key with the person you want to chat with."
              "\nYou can't share your public key with anyone in the chat. You must do it elsewhere."
              "\n")

        generate_qr(public_key_str, "encryption_public_key")
        generate_qr(private_key_str, "encryption_private_key")

        print("The images of the QR codes for your chat client's new public and private key are saved in the "
              "location " + path + "files/qr_codes")
        print("You can take a print of the images as a backup for future use. Scanning the QR with any QR code scanner "
              "reveals the content.\n")
        # Writing down the private and public keys to 'pem' files
    else:
        private_key_input = "-----BEGIN RSA PRIVATE KEY-----" + private_key_input + "-----END RSA PRIVATE KEY-----"
        private_key_input = str(private_key_input.replace("#N#", "\n"))

        with open(dir_path + 'my_private_pem.pem', 'w') as pr:
            pr.write(private_key_input)

        # Importing keys from files, converting it into the RsaKey object
        private_key = RSA.import_key(open(dir_path + 'my_private_pem.pem', 'r').read())
        public_key = private_key.publickey()

    return public_key, private_key


def import_keys(print_existing_keys=False):
    generated_new_keys = False

    private_key = RSA.import_key(open(dir_path + 'my_private_pem.pem', 'r').read())
    public_key = RSA.import_key(open(dir_path + 'my_public_pem.pem', 'r').read())

    print("Your pre-saved public and private encryption keys are found!")
    upk_yn = False
    # This variable is used to denote whether a right input is received for use_presaved_keys

    while not upk_yn:
        use_presaved_keys = input("Do you want to keep using them? (Y/N): ")
        if (use_presaved_keys == "Y") | (use_presaved_keys == "y"):
            upk_yn = True
            print("")
            pass
        elif (use_presaved_keys == "N") | (use_presaved_keys == "n"):
            upk_yn = True
            print("If you generate new keys, your previous saved keys will be deleted forever! "
                  "\nYou might lose contact with anyone you have chatted before using those keys for encryption.")
            upkfc_yn = False
            while not upkfc_yn:
                use_presaved_keys_final_choice = input("Are you sure that you want to generate new keys? (Y/N): ")
                # This variable is used to denote whether a right input is received for use_presaved_keys_final_choice
                if (use_presaved_keys_final_choice == "Y") | (use_presaved_keys_final_choice == "y"):
                    # Previous public key
                    public_key_prev = open(dir_path + 'my_public_pem.pem', 'r').read()
                    public_key_str = str(public_key_prev).replace("\n", "#N#")
                    public_key_str = (str(public_key_str))[26:-24]
                    # Previous private key
                    private_key_prev = open(dir_path + 'my_private_pem.pem', 'r').read()
                    private_key_str = str(private_key_prev).replace("\n", "#N#")
                    private_key_str = (str(private_key_str))[31:-29]
                    # Display previous public and private keys
                    print("Keep your previous public and private key saved somewhere for safety!")
                    print("\nYour Previous Public Key:\n\n" + public_key_str)
                    print("\nYour Previous Private Key:\n\n" + private_key_str)
                    generate_qr(public_key_str, "previous_public_key_backup")
                    generate_qr(private_key_str, "previous_private_key_backup")
                    print("\nThe images of the QR codes for your chat client's previous public and private key are "
                          "saved in the location " + path + "files/qr_codes/")
                    print("You can take a print of the images as a backup for future use. Scanning the QR with any QR "
                          "code scanner reveals the content.")
                    print("\nGenerating new keys...\n")
                    # Generate new keys
                    public_key, private_key = generate_keys()
                    generated_new_keys = True
                    upkfc_yn = True
                elif (use_presaved_keys_final_choice == "N") | (use_presaved_keys_final_choice == "n"):
                    print("Using your pre-saved public and private encryption keys...\n")
                    upkfc_yn = True
                    pass
                else:
                    print("Invalid input!"
                          "\nYou must enter 'y' or 'n' for yes or no only!\n")
        else:
            print("Invalid input!"
                  "\nYou must enter 'y' or 'n' for yes or no only!\n")

    if print_existing_keys & (not generated_new_keys):
        # Pre-saved public key
        public_key_pre_saved = open(dir_path + 'my_public_pem.pem', 'r').read()
        public_key_str = str(public_key_pre_saved).replace("\n", "#N#")
        public_key_str = (str(public_key_str))[26:-24]
        # Pre-saved private key
        private_key_pre_saved = open(dir_path + 'my_private_pem.pem', 'r').read()
        private_key_str = str(private_key_pre_saved).replace("\n", "#N#")
        private_key_str = (str(private_key_str))[31:-29]
        # Display pre-saved public and private keys
        print("Keep your pre-saved public and private key saved somewhere for safety!")
        print("\nYour Pre-saved Public Key:\n\n" + public_key_str)
        print("\nYour Pre-saved Private Key:\n\n" + private_key_str)
        generate_qr(public_key_str, "previous_public_key_backup")
        generate_qr(private_key_str, "previous_private_key_backup")
        print("\nThe images of the QR codes for your chat client's pre-saved public and private key are "
              "saved in the location " + path + "files/qr_codes/")
        print("You can take a print of the images as a backup for future use. Scanning the QR with any QR "
              "code scanner reveals the content.")

    return public_key, private_key


def generate_keys():
    while True:
        have_keys = input("Do you have any old encryption keys to generate the new keys from? (Y/N): ")
        if (have_keys == "Y") | (have_keys == "y"):
            private_key_input = input("\nEnter your RSA private key:\n")
            print("")
            break
        elif (have_keys == "N") | (have_keys == "n"):
            private_key_input = None
            '''
            generate public and private keys with rsa.newkeys method. 
            This method accepts key length as its parameter. Key length should be at least 16.
            '''
            break
        else:
            print("Invalid input!"
                  "\nYou must enter 'y' or 'n' for yes or no only!\n")
    try:
        public_key, private_key = generate_key(private_key_input)
        return public_key, private_key
    except:
        # print("An error occurred. Make sure you have entered a correct private key generated by Onymochat.")
        raise Exception("Error in generate_keys")


def encrypt(message, public_key_input):
    message = message.encode(encoding="ascii", errors="replace")

    public_key_input = "-----BEGIN PUBLIC KEY-----" + public_key_input + "-----END PUBLIC KEY-----"
    public_key_input = str(public_key_input.replace("#N#", "\n"))

    with open(dir_path + 'public_pem_temp.pem', 'w') as public_pem_temp:
        public_pem_temp.write(public_key_input)

    # Importing keys from files, converting it into the RsaKey object
    public_key_temp = RSA.import_key(open(dir_path + 'public_pem_temp.pem', 'r').read())

    # Instantiating PKCS1_OAEP object with the public key for encryption
    cipher = PKCS1_OAEP.new(key=public_key_temp)
    # Encrypting the message with the PKCS1_OAEP object
    cipher_text = cipher.encrypt(message)
    cipher_text = cipher_text.decode('iso8859_2', 'ignore')

    return cipher_text


# def decrypt(cipher_text, private_key_input):
def decrypt(cipher_text, private_key):
    cipher_text = cipher_text.encode('iso8859_2', 'ignore')

    # Instantiating PKCS1_OAEP object with the private key for decryption
    decrypt = PKCS1_OAEP.new(key=private_key)
    # Decrypting the message with the PKCS1_OAEP object
    decrypted_message = decrypt.decrypt(cipher_text)
    return (str(decrypted_message))[2:-1]
