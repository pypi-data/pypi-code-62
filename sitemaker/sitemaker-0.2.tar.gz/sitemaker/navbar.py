from sitemaker.items import item
HORIZORTAL=0
VERTICAL=1

class navbar(item):
    def __init__(self,typ=0,cls=None):
        self.init()
        self.items=[]
        self.type=typ
        self.clss=cls
        
    def addItem(self,i):
        self.items.append(i)
        
    def build(self):
        self.content="<nav"
        if self.clss:
            self.content+=" class=\"" +self.clss+ "\" "
        self.content+=">\n"
        self.content+="<ul>\n"
        for i in self.items:
            self.content+="<li"
            if self.type == 0:
                self.content+=" style=\"display: inline;\" "
            self.content+=">"
            self.content+=i.getItem().build()
            self.content+="</li>\n"
        self.content+="</ul>\n"
        self.content+="</nav>"
        return self.content
