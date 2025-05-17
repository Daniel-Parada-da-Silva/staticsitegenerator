from textnode import *
from nodeconverter import NodeConverter

from enum import Enum

print("hello world")

def BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UL = "Unordered_List"
    OL = "Ordered_List"

def main():
    txtn = TextNode("This is some text", TextType.LINK, "https://www.boot.dev")
    print(NodeConverter.text_node_to_html_node(txtn))
    print(txtn)
    print("a")

main()