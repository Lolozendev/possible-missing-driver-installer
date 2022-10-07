import requests
import time
import threading
import os
import sys
import shutil

def firmwarenames(string):
    firmware_list = []
    with open(string) as f:
        for line in f:
            firmware_list.append(line.split("/")[4].split(" ")[0])
    return firmware_list

def download_firmwares_multithread_show_progress(firmware_list,subdirectory="firmwares"):
    if not os.path.exists(subdirectory):
        os.mkdir(subdirectory)
    else:
        shutil.rmtree(subdirectory)
        os.mkdir(subdirectory)
    
    firmware_downloaded = []
    for firmware in firmware_list:
        r = requests.get("https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/i915/" + firmware, stream=True)
        if r.status_code == 200:
            with open(os.path.join(subdirectory,firmware), "wb") as f:
                print(firmware + " OK")
                start = time.time()
                total_length = int(r.headers.get("content-length"))
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        done = int(50 * f.tell() / total_length)
                        sys.stdout.write("\r[%s%s]" % ("=" * done, " " * (50-done)))
                        sys.stdout.flush()
                end = time.time()
                print(f.tell()/1024, "KB", end-start, "seconds")
                firmware_downloaded.append(firmware)
        else:
            print(firmware + " Failed")
    return firmware_downloaded
    
#write a function to print help message
def help():
    print("Usage: python firmware.py [firmware list file]")


if __name__ == "__main__":

    firmwaredirname = "i915"
    subdirectory = "firmwares"

    if len(sys.argv) < 2:
        print("Please give a file as parameter")
        help()
        sys.exit(1)
    firmware_list = firmwarenames(sys.argv[1])

    downloaded_firmwares = download_firmwares_multithread_show_progress(firmware_list,subdirectory)
    
    
    if not os.path.exists("/lib/firmware/"+firmwaredirname+"/"):
        print(f"Creating /lib/firmware/{firmwaredirname}/")
        os.system("sudo mkdir /lib/firmware/"+firmwaredirname)
    
    for firmware in downloaded_firmwares:
    
        if os.path.exists("/lib/firmware/"+firmwaredirname+"/" + firmware):
            print(f"Removing old /lib/firmware/{firmwaredirname}/{firmware}")
            os.system("sudo rm /lib/firmware/"+firmwaredirname+"/" + firmware)
        print(f"Copy {firmware} to /lib/firmware/{firmwaredirname}/")
        os.system("sudo cp firmwares/" + firmware + " /lib/firmware/"+firmwaredirname)
    
    print("removing downloaded firmwares directory")
    shutil.rmtree(subdirectory)

    print("Updating initramfs")
    os.system("sudo update-initramfs -u")

    print("Done! do you want to reboot now? (y/n)")
    if input() == "y":
        os.system("sudo reboot")
    else:
        print("Alright, but don't forget to reboot later")
    


    
