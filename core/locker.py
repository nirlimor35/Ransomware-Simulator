import os
import time
import ctypes
import platform


def hide_file(filepath):
    """Hide file on Windows (simulate locker)"""
    if platform.system() == "Windows":
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(str(filepath), FILE_ATTRIBUTE_HIDDEN)
    elif platform.system() == "Linux":
        dirname, filename = os.path.split(filepath)
        if not filename.startswith('.'):
            os.rename(filepath, os.path.join(dirname, '.' + filename))


def lock_files_temporarily(file_list, duration=5):
    """
    Simulate temporary lock by renaming files with a lock prefix
    and restoring them after `duration` seconds.
    """
    locked = []
    for file in file_list:
        locked_name = file + ".locked"
        os.rename(file, locked_name)
        locked.append((locked_name, file))
        print(f"[LOCKED] {file}")
    print(locked)
    time.sleep(duration)

    for locked_name, original_name in locked:
        os.rename(locked_name, original_name)
        print(f"[UNLOCKED] {original_name}")


lock_files_temporarily(["/Users/nir.limor/Documents/Post-Quantum-Secure-Messaging-System/testing/test.txt"])
