from textnode import *

print("hello world")

def main():
    txtn = TextNode("This is some text", TextType.LINKS, "https://www.boot.dev")
    print(txtn)

main()