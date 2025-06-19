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
## 🚀 Usage

1. **Find the browser profile folder** that contains:
   - `Login Data`
   - `Local State`

   📂 On Windows, this is usually located at:
C:\Users<YourUsername>\AppData\Local\Google\Chrome\User Data\Default

2. **Run the script in your terminal or command prompt**:
```bash
python decrypt.py
```
3. When asked, paste the full path to the folder containing Login Data and Local State. For example:
   C:\Users\YG\AppData\Local\Google\Chrome\User Data\Default
4. The script will:
   - Extract saved website URLs, usernames, and passwords
   - Decrypt the passwords using Windows DPAPI + AES
   - Save the results into a file called output.txt in the same folder
     
5. Open output.txt to see the list of saved login credentials.

   
✅ Result
After running, you’ll see:
**************************************************
URL: https://example.com
Username: your@email.com
Password: mysecret123
**************************************************
