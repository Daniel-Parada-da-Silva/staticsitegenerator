from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UL = "Unordered_List"
    OL = "Ordered_List"

class BlockConverter():
    def markdown_to_blocks(markdown):
        blocks = markdown.split("\n\n")
        return [item for item in list(map(str.strip, blocks)) if item != ""]
    
    def block_to_block_type(text):
        txt = ""
        if re.match(r"^#{1,6} ", text):
            return BlockType.HEADING
        if re.match(r"^'''([\s\S]*?)'''$", text):
            return BlockType.CODE
        if re.match(r"^>", text):
            return BlockType.QUOTE
        if re.match(r"^(- .*\n?)+", text):
            return BlockType.UL
        if re.match(r"^(?:[1-9]\d*\. .*\n?)+", text):
            return BlockType.OL
        return BlockType.PARAGRAPH