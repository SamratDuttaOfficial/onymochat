import os
import re

path = os.path.dirname(os.path.realpath(__file__)) + "/"
dir_path = path + "files/keys/"


def save_open_keys(filename, key_type, name_type, do_what, extra_stmt=""):
    names_list = []
    keys_list = []

    try:
        with open(dir_path+filename, 'r', encoding='utf8') as file_object:
            for line in file_object:
                stripped_line = line.strip()
                name, key = stripped_line.split()
                names_list.append(name)
                keys_list.append(key)
    except FileNotFoundError:
        print("ERROR: The file " + filename + " doesn't exist. Please create a file with the same name in "
              "the directory: " + dir_path)
        raise Exception("Error in save_open_keys")
    except Exception as e:
        print(e)
        print("There might be a problem with the file structure of " + filename + " file. Please create a "
              "file with the same name in the directory: " + dir_path)
        raise Exception("Error in save_open_keys")

    print("\nList of " + name_type + "(s) saved in your system:")
    for name in names_list:
        print(name)
    print("------")

    while True:
        print("\nInput ADD to add a new new " + name_type + " to your system."
              "\nInput DELETE to delete an existing " + name_type + " from your system."
              "\nInput NONE to use a " + key_type + " manually without saving it."
              "\nOr, enter the name of the " + name_type + " you want to " + do_what + " (case sensitive).\n")
        select = input("Input: ")
        if select == "":
            print("Invalid Input!")
        elif (select == "ADD") | (select == "add"):
            new_name = input("Enter the name of the new " + name_type + ": ")
            new_name = re.sub(r'[^a-zA-Z0-9]', '', new_name)
            new_key = input("Enter the " + key_type + " of the new " + name_type + extra_stmt + ":\n")
            new_key = new_key.replace(" ", "")
            with open(dir_path+filename, "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0:
                    file_object.write("\n")
                # Append text at the end of file
                file_object.write(new_name + " " + new_key)
            to_return_key = new_key
            to_return_name = new_name
            break
        elif (select == "DELETE") | (select == "delete"):
            while True:
                to_delete = input("Enter the name of the " + name_type + " to delete: ")
                if to_delete == "":
                    print("Invalid Input!")
                else:
                    try:
                        index = names_list.index(to_delete)
                        del names_list[index]
                        del keys_list[index]
                        with open(dir_path + filename, "a+") as file_object:
                            file_object.truncate(0)
                            for i in range(len(names_list)):
                                # Move read cursor to the start of file.
                                file_object.seek(0)
                                # If file is not empty then append '\n'
                                data = file_object.read(100)
                                if len(data) > 0:
                                    file_object.write("\n")
                                # Append text at the end of file
                                file_object.write(names_list[i] + " " + keys_list[i])
                        print("Deleted successfully!")
                        print("\nList of names of " + name_type + "(s) saved in your system:")
                        for name in names_list:
                            print(name)
                        print("------")
                        break
                    except ValueError as e:
                        print(e)
                        print("The name of the " + name_type + " you entered is not saved in your system. Try again.")
                    except Exception as e:
                        print("Invalid Input! Error: " + e)
        elif (select == "NONE") | (select == "none"):
            raise Exception("Use " + key_type + " without saving.")
        else:
            try:
                to_return_key = keys_list[names_list.index(select)]
                to_return_name = select
                break
            except ValueError:
                print("The name of the " + name_type + " you entered is not saved in your system. Try again.")
            except Exception as e:
                print("Invalid Input! Error: " + e)

    return to_return_key, to_return_name


def delete_all_keys(filename):
    try:
        with open(dir_path + filename, "a+") as file_object:
            file_object.truncate(0)
        print("Deleted all contents of " + filename + " successfully!")
    except FileNotFoundError:
        print("ERROR: The file " + filename + " doesn't exist. Please search for the file manually and delete all the "
                                              "contents in that file manually "
                                              "(don't delete the file itself)." + dir_path)
    except Exception as e:
        print("Some error occurred. Error: " + str(e))
