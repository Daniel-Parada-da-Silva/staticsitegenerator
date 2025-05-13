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
        if isinstance(self.props, dict):
            for item in self.props:
                txt = txt + f" {item}=\"{self.props[item]}\""
        return txt

    def __repr__(self):
        children = 0
        if isinstance(self.children, dict):
            children = len(self.children)
        return f"Tag: {self.tag}, Value: {self.value}, Children: {children}, Props: {self.props_to_html()}"