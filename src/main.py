from textnode import *
from nodeconverter import NodeConverter

print("hello world")

def main():
    txtn = TextNode("This is some text", TextType.LINK, "https://www.boot.dev")
    print(NodeConverter.text_node_to_html_node(txtn))
    print(txtn)

main()