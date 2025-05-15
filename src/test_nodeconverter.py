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
    
    def test_text_split_node_delimiter_6(self):
        node = TextNode("This **is a text** with a **bold block** word", TextType.TEXT)
        new_nodes = NodeConverter.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.TEXT),
            TextNode("is a text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_extract_markdown_images(self):
        matches = NodeConverter.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = NodeConverter.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a duplicate ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = NodeConverter.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a duplicate ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://boot.dev) and another [second link](https://youtube.es)",
            TextType.TEXT,
        )
        new_nodes = NodeConverter.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://youtube.es"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_2(self):
        node = TextNode(
            "This is text with an [link](https://boot.dev) and a duplicate [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = NodeConverter.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and a duplicate ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )