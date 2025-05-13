from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class NodeConverter():
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

    #def markdown_to_text_nodes(markdown_text):
