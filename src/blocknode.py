from enum import Enum
from parentnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UL = "Unordered_List"
    OL = "Ordered_List"

class BlockNode():
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = block_type
        self.children = list()