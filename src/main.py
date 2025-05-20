from textnode import *
from blocknode import *
from nodeconverter import *

print("hello world")

def main():
    txtn = TextNode("This is some text", TextType.LINK, "https://www.boot.dev")
    print(text_node_to_html_node(txtn))
    print(txtn)

main()