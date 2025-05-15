import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from nodeconverter import NodeConverter


class TestNodeConverter(unittest.TestCase):
    def test_split_node_delimiter_1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = NodeConverter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_split_node_delimiter_2(self):
        node = TextNode("`This is text with a code block` word", TextType.TEXT)
        new_nodes = NodeConverter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_split_node_delimiter_3(self):
        node = TextNode("`This is text with a code block word`", TextType.TEXT)
        new_nodes = NodeConverter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a code block word", TextType.CODE)
        ])
    
    def test_split_node_delimiter_4(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("`This is text with a code block` word", TextType.TEXT)
        node3 = TextNode("`This is text with a code block word`", TextType.TEXT)
        new_nodes = NodeConverter.split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a code block word", TextType.CODE)
        ])
    
    def test_text_split_node_delimiter_5(self):
        node = TextNode("This is a text with a **bold block** word", TextType.TEXT)
        new_nodes = NodeConverter.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_extract_markdown_images(self):
        matches = NodeConverter.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)