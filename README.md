# 🛡️ Python Ransomware Simulator

> ⚠️ Educational use only. Do not deploy this on production systems or without permission.

This project simulates a basic ransomware operation using Python including:
* AES file encryption
* ransom note dropping
* and file locking mechanisms (example, non-destructive)

It is intended for cybersecurity red-team training, incident response drills, and educational demonstrations.

The program will search for and encrypt files with the extension of `.txt`, `.docx` and `.xlsx` and will add the suffix of `.enc` to them.

The project consists of one single Python class that contain the following callable methods
* `generate_key()`
* `run_simulation()`
* `run_mal_action()`
* `run_decrypt()`

## Usage
1. Clone the repository
2. Install dependencies:
    
   `pip install -r requirements.txt`

3. Use one or a combination of the following methods
   1. `generate_key()` - will generate an AES256 key and loads it to memory.
      Takes the parameters:
      * password - **required**
      * salt_file - the salt file's name. not required for new keys, as the salt file will be generated if not supplied.
   2. `run_simulation()` - Test run on a specific directory.
      Takes the parameters:
      * `base_path` - Testing directory's full path
      * `password` - Not required. defaults to the password: **supersecret**
   3. `run_mal_action()` - ⚠️ USE CATION!! ⚠️ - Will encrypt the entire file system found files
      Takes the parameters:
      * `password` - Choose a password for the full encryption 
   4. `run_decrypt()` - Will decrypt all encrypted files the method will be run against
      Takes the parameters:
      * `base_path` - The encrypted files directory's full path
      * `password` - The password that were used for encryption
      * `salt_file` - The salt file that was generated upon the encryption phase

This code is licensed under the MIT License and provided strictly for educational use.

> 🛑 The author is not responsible for any misuse of this code. Do not run it on real systems or unauthorized environments. It is your responsibility to ensure compliance with laws and ethical standards.