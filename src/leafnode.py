from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Value property must have a value")
        txt = self.value
        if self.tag != None:
            txt = f"<{self.tag}{self.props_to_html()}>{txt}</{self.tag}>"
        return txt