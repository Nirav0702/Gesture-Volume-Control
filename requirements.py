import os
import subprocess
import sys


def install(package):
    os.system("pip install " + str(package))
    reqs = subprocess.check_output([sys.executable, "-m", "pip", "show", str(package)])

    print(str(reqs) + "\n")
    print("Installed " + package.upper() + "\n")


install("mediapipe")
install("opencv-python")
install("pycaw")
install("tk")
install("Pillow")