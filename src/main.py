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
        if not os.path.isfile(current):
            publish(current + "/")
        else:
            shutil.copy(current, current.replace("static", "public"))

def main():
    shutil.rmtree("./public/", ignore_errors = True)
    publish("./static/")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()