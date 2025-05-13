import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_impl(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)
    
    def test_has_props(self):
        node = HTMLNode("a", "Text", None, {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), " href=\"https://boot.dev\"")
    
if __name__ == "__main__":
    unittest.main()