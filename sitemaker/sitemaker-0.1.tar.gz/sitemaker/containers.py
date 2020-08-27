from sitemaker.items import item

class container(item):

    def __init__(self,i=None):
        self.init()
        self.items=[]
        self.clss=cls
        

    def addItem(self,item):
        self.items.append(item.getItem())

    def addLine(self,ctx):
        i=item(ctx+"<br>")
        self.items.append(i)


class paragraph(container):

    def __init__(self,cls=None):
        self.init()
        self.items=[]
        self.clss=cls
        
    def build(self):
        self.content+="<p"
        if self.clss:
            self.content+=" class=\""+self.clss + "\" "
        self.content+=">\n"
        for j in self.items:
            self.content+=j.build()
        self.content+="</p>"
        return self.content
        
class tagged(container):
    def __init__(self,tag="",i=None,cls=None):
        self.init()
        self.items=[]
        self.clss=cls
        self.tag=tag

    
    def build(self):
        self.content+="<p"
        if self.clss:
            self.content+=" class=\""+self.clss + "\" "
        self.content+=">\n"
        for j in self.items:
            self.content+=j.build()
        self.content+="</p>"
        return self.content


class div(tagged):
     def __init__(self,i=None,cls=None):
        self.init()
        self.items=[]
        self.clss=cls
        self.tag="div"
        if i:
            self.items.append(i)


class span(item):
    def __init__(self,i=None,cls=None):
        self.init()
        self.items=[]
        self.clss=cls
        self.tag="span"
        if i:
            self.items.append(i)
