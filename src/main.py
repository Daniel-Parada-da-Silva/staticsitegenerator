import os
import shutil

from textnode import *
from blocknode import *
from nodeconverter import *

def publish(path: str):
    lst = os.listdir(path)
    new_path = path.replace("static", "public")
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for item in lst:
        current = path + item
        if os.path.isfile(current):
            shutil.copy(current, current.replace("static", "public"))
        else:
            publish(current + "/")

def main():
    shutil.rmtree("./public/", ignore_errors = True)
    publish("./static/")
    generate_pages_recursive("./content/", "./template.html", "./public/")

main()