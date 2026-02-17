import subprocess

def disable_usb_storage():
    subprocess.run(["pkexec", "modprobe", "-r", "usb-storage"])
