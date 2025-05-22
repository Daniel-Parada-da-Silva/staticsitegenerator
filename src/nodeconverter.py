import re
import os

from enum import Enum

from textnode import TextNode, TextType
from parentnode import ParentNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise Exception("text_node is not a TextNode")
    return text_node.to_html_node()

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    lst = list()
    for item in old_nodes:
        if item.text_type != TextType.TEXT:
            lst.append(item)
        else:
            text = item.text
            if text.count(delimiter) % 2 != 0:
                raise Exception("Invalid Markdown syntax: there is a non closed delimiter")
            splitted = text.split(delimiter)
            type_text = [TextType.TEXT, text_type]
            for i in range(len(splitted)):
                mdl = i % 2
                new_text = splitted[i]
                if len(new_text) > 0:
                    lst.append(TextNode(new_text, type_text[mdl]))
    return lst

def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)
    # return __process_markdown_common(regex, text)

def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)
    # return __process_markdown_common(regex, text)

def split_nodes_image(old_nodes):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    lst = list()

    for item in old_nodes:
        if item.text_type != TextType.TEXT:
            lst.append(item)
        else:
            lst.extend(__split_nodes_url(item.text, regex, TextType.IMAGE))
        
    return lst

def split_nodes_link(old_nodes):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    lst = list()

    for item in old_nodes:
        if item.text_type != TextType.TEXT:
            lst.append(item)
        else:
            lst.extend(__split_nodes_url(item.text, regex, TextType.LINK))
        
    return lst

def __split_nodes_url(text, regex, type):
    lst = list()
    txt = text
    matches = re.findall(regex, text)
    trimming = -1
    if type == TextType.IMAGE:
        trimming = -2
    
    for match in matches:
        delimiter = match[0] + "](" + match[1]
        aux = txt.split(delimiter, 1)
        trimmed = aux[0][:trimming]
        if len(trimmed) > 0:
            lst.append(TextNode(trimmed,TextType.TEXT))
        lst.append(TextNode(match[0], type, match[1]))
        txt = aux[1][1:]
    if len(txt) > 0:
        lst.append(TextNode(txt, TextType.TEXT))
    return lst

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

#### BLOCK

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [item for item in list(map(str.strip, blocks)) if item != ""]

def block_to_block_type(text):
    if re.match(r"^#{1,6} ", text):
        return BlockType.HEADING
    if re.match(r"^```([\s\S]*?)```$", text):
        return BlockType.CODE
    if re.match(r"^>", text):
        return BlockType.QUOTE
    if re.match(r"^(- .*\n?)+", text):
        return BlockType.UL
    if re.match(r"^(?:[1-9]\d*\. .*\n?)+", text):
        return BlockType.OL
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    root = ParentNode("div", list())
    for block in blocks:
        root.children.append(BlockNode(block, block_to_block_type(block)).to_html_node())
    return root

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
    
    def to_html_node(self):
        node = ParentNode("p", list())
        match(self.block_type):
            case(BlockType.CODE):
                node.tag = "pre"
                node.children.append(LeafNode("code", self.text[4:-3]))
                return node #This case doesn't need more processing
            case(BlockType.PARAGRAPH):
                self.text = " ".join(self.text.split("\n")) #We keep the node as it is
            case(BlockType.HEADING):
                splited = self.text.split(" ", 1)
                node.tag = f"h{len(splited[0])}"
                self.text = splited[1]
            case(BlockType.QUOTE):
                node.tag = "blockquote"
                self.text = self.text[1:].replace(">", "<br/>").strip()
            case(BlockType.OL):
                node.tag = "ol"
            case(BlockType.UL):
                node.tag = "ul"
            case _:
                raise Exception(f"Not a valid Node Type: {self.block_type}")
        node.children.extend(self.__text_to_children())
        return node
    
    def __text_to_children(self):
        if self.block_type == BlockType.OL or self.block_type == BlockType.UL:
            regex = r""
            lst = list[ParentNode]()
            if self.block_type == BlockType.OL:
                regex = r"\d+\.\s*(.+)"
            if self.block_type == BlockType.UL:
                regex = r"-\s*(.+)"
            for li in re.findall(regex, self.text):
                children = list(map(text_node_to_html_node, text_to_textnodes(li)))
                node = ParentNode("li", children)
                lst.append(node)
            return lst
        else:    
            return list(map(text_node_to_html_node, text_to_textnodes(self.text)))

def extract_title(markdown):
    lst = re.findall(r"^# (.+)\n", markdown)
    if len(lst) < 1:
        raise Exception("There is no title")
    return lst[0]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    template = read_from_file(template_path)
    markdown = read_from_file(from_path)
    title = extract_title(markdown)
    
    content = markdown_to_html_node(markdown).to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    write_into_file(dest_path, template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    path = dir_path_content
    lst = os.listdir(path)
    new_path = dest_dir_path
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for item in lst:
        current = path + item
        new_current = new_path + item
        if os.path.isfile(current):
            generate_page(current, template_path, new_current.replace(".md",".html"))
        else:
            generate_pages_recursive(current + "/", template_path, new_current + "/")

def read_from_file(path):
    f = open(path, "r", -1, encoding= "utf-8")
    txt = f.read()
    f.close()
    return txt

def write_into_file(path, content):
    f = open(path, "w", encoding= "utf-8")
    f.write(content)
    f.close()