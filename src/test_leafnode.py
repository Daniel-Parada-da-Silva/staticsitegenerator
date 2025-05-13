import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_impl(self):
        node = LeafNode()
        self.assertRaises(ValueError, node.to_html)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
if __name__ == "__main__":
    unittest.main()