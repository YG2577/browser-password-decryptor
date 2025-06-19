# browser-password-decryptor
# 🔐 Browser Password Decryptor (Python)

This is a Python-based script that decrypts saved passwords from Chromium-based browsers like **Google Chrome** or **Microsoft Edge** on **Windows**.  
It is made for **educational purposes only** to help users recover their own saved credentials.

---

## ⚠️ Disclaimer

This tool is for **educational and ethical use only**.  
❌ Do **NOT** use it on anyone else's computer or account without permission.  
Unauthorized use is illegal and violates GitHub's terms.

---

## 🧠 How It Works

Browsers like Chrome save passwords encrypted using a master key stored in a file called `Local State`.  
This script does the following:

- Reads the master encryption key from the `Local State` file
- Extracts saved credentials from the browser's `Login Data` SQLite database
- Decrypts the passwords using Windows DPAPI and AES-GCM

---

## 📂 Project Structure

