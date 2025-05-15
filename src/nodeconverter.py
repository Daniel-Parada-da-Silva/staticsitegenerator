import re

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

    def extract_markdown_images(text):
        regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        return re.findall(regex, text)
        # return NodeConverter.__process_markdown_common(regex, text)
    
    def extract_markdown_links(text):
        regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        return re.findall(regex, text)
        # return NodeConverter.__process_markdown_common(regex, text)
    
    #def split_nodes_image(old_nodes):


    # def __process_markdown_common(regex, text):
    #     matches = re.findall(regex, text)
    #     lst = list()

    #     for match in matches:
    #         print(match)
    #         aux = match[2:].spilt("]", 1)
    #         txt = aux[0]
    #         link = aux[1][1:-1] #Obtains the 2nd part, trimming both the ( and the )
    #         lst.append((txt, link))
        
    #     return lst
