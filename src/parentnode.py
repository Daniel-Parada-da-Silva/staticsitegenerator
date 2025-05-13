from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag property must have a value")
        if not isinstance(self.children, list):
            raise ValueError("Children must be a list")
        if False in list(map(lambda x: isinstance(x, HTMLNode),self.children)):
            raise ValueError("All Children should inherit from HTMLNode")
        txt = f"<{self.tag}{self.props_to_html()}>"
        for node in self.children:
            txt += node.to_html()
        txt = txt + f"</{self.tag}>"
        return txt