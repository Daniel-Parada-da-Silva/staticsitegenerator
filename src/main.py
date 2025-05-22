import os
import shutil
import sys

from textnode import *
from blocknode import *
from nodeconverter import *

def publish(path: str, orgn: str, dest: str):
    lst = os.listdir(path)
    new_path = path.replace(orgn, dest)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for item in lst:
        current = path + item
        if os.path.isfile(current):
            shutil.copy(current, current.replace(orgn, dest))
        else:
            publish(current + "/", orgn, dest)

def main():
    basepath = sys.argv[1]
    orgn = "static"
    dest = sys.argv[2]
    
    shutil.rmtree("./{dest}/", ignore_errors = True)
    publish(f"./{orgn}/", orgn, dest)
    generate_pages_recursive("./content/", "./template.html", f"./{dest}/", basepath)

main()