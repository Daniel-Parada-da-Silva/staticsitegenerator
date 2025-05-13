class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        txt = ""
        for item in self.props:
            txt = txt + f" {item}=\"{self.props[item]}\""
        return txt

    def __repr__(self):
        return (self.tag, self.value, self.children, self.props_to_html)