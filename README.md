# 🛡️ Python Ransomware Simulator

> ⚠️ Educational use only. Do not deploy this on production systems or without permission.

A simulation of a basic ransomware operation using Python including:

* AES file encryption
* ransom note dropping
* and file locking mechanisms (example, non-destructive)

## Motivation

The program is intended for cybersecurity red-team training, incident response drills, and educational demonstrations.

It will search for and encrypt files with the extension of `.txt`, `.docx` and `.xlsx` and will add the suffix of `.enc`
to them.

The project consists of one single Python class that contain the following callable methods

* `generate_key()`
* `run_simulation()`
* `run_mal_action()`
* `run_decrypt()`

## Usage

1. Clone the repository
2. Install dependencies:

   `pip install -r requirements.txt`

3. Use one or a combination of the following methods:
    1. `generate_key()` - will generate an AES256 key and loads it to memory.
       Takes the parameters:
        * password - **required**
        * salt_file - the salt file's name. not required for new keys, as the salt file will be generated if not
          supplied.
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

#### Note about the file locking mechanisms

There are two mechanisms exist in the code

* `hide_file()` - Make it look like files are deleted when they are actually hidden (Will not revert the effect when done)
  * Windows: Uses ctypes to set the file as hidden via the Windows API.
  * Linux/macOS: Renames the file with a dot prefix (.filename) to hide it from normal directory views.
* `lock_files_temporarily()` - Not actually locking the files, but simply adding the `.locked` suffix to all files for
  the duration set (Will revert the effect when done). The goal is to create panic and show transient system interruption without causing real harm.
  * Renames files with a .locked suffix (e.g., invoice.docx → invoice.docx.locked)
  * Waits for a given time (duration), then renames them back.
  * Simulates temporary denial-of-access behavior.

Real ransomware will sometimes will disrupts the access to files or the system beyond just encryption.
While encryption handles data confidentiality, the simulated locking mechanisms simulate disruption and urgency for the
victim,

mimicking behaviors like

| Functionality                        | Real-World Behavior Simulated                      |
|--------------------------------------|----------------------------------------------------|
| Hiding or renaming files             | Makes files seem missing or corrupted              |
| Temporarily locking file access      | Mimics exclusive file access or I/O locks          |
| Blocking user interaction (optional) | Simulates full-screen ransomware interfaces        |
| System-level panic simulation        | Mimics operational paralysis without actual damage |

Real ransomware often does more than just encrypt:
* File system disruption: It renames or corrupts files to increase psychological pressure.
* UI hijack: Many ransomware families launch fullscreen GUI windows that prevent user interaction.
* Locker-only ransomware: Some variants (e.g., police-themed scams) don't encrypt data but simply block user access.

In theory, if the locking mechanisms included were to do one or more of the real ransomware actions described above, those could be used regardless of the encryption action as it still makes the system unusable.

> 🛑 This code is licensed under the MIT License and provided strictly for educational use. <br>The author is not
> responsible for any misuse of this code. Do not run it on real systems or unauthorized environments. It is your
> responsibility to ensure compliance with laws and ethical standards.