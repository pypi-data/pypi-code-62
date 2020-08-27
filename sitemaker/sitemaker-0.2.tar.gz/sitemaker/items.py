class item:

    def __init__(self,ctx=""):
        return self.init(ctx)

    def init(self,ctx=""):
        self.content=ctx
        
    def getItem(self):
        return self

    def setClass(self,cls):
        self.clss=cls

        
    def build(self):
        return self.content

class line(item):

    def __init__(self,ctx=""):
        self.init(ctx+"<br>")
    def setText(self,ctx=""):
        self.content=ctx+"<br>"
    def getItem(self):
        return self
        
class script(item):

    def __init__(self,ctx=""):
        self.init("<script>\n"+ctx+"\n</script>\n")
    def setText(self,ctx=""):
        self.content="<script>\n"+ctx+"\n</script>\n"
    def getItem(self):
        return self

class image(item):

    def __init__(self,src=None,cls=None):
        self.init()
        self.href=src
        self.alt=None
        self.clss=cls
        
    def setImage(self,src):
        self.href=src
        
    def setAlt(self,src):
        self.alt=src

        
    def build(self):
        
        self.content="<img "
        if self.alt:
                self.content+="alt=\""+self.alt+"\" "
        if self.href:
                self.content+="src=\""+self.href+"\" "
        if self.clss:
                self.content+="class=\""+self.clss+"\" "
        self.content+=">"
        return self.content
        
class link(item):

    def __init__(self,link=None,txt=None,cls=None):
        self.init()
        self.href=link
        self.text=txt
        self.clss=cls
        
    def setHref(self,src):
        self.href=src
        
    def setText(self,src):
        self.text=src
        
    def build(self):
        self.content="<a "
        if self.href:
                self.content+="href=\""+self.href+"\" "
        if self.clss:
                self.content+="class=\""+self.clss+"\" "
        self.content+=">"
        if self.text:
                self.content+=self.text
        self.content+="</a>"
        return self.content

