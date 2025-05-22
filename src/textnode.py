from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "Text"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
        if(self.text_type.value == TextType.LINK and self.url == None):
            raise Exception("Links must have an URL")
    
    def to_html_node(self):
        node = LeafNode(None, self.text)
        match(self.text_type):
            case(TextType.TEXT):
                pass #We keep the node as it is
            case(TextType.BOLD):
                node.tag = "b"
            case(TextType.ITALIC):
                node.tag = "i"
            case(TextType.CODE):
                node.tag = "code"
            case(TextType.LINK):
                node.tag = "a"
                node.props = {"href": self.url}
            case(TextType.IMAGE):
                node = LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise Exception(f"Not a valid Node Type: {self.text_type}")
        return node
    
    def __eq__(self, value):
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"