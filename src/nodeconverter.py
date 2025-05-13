from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class NodeConverter():
    def text_node_to_html_node(text_node):
        if not isinstance(text_node, TextNode):
            raise Exception("text_node is not a TextNode")
        return text_node.to_html_node()
    