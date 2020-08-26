from os.path import exists as e
class HTML5:
    def __init__(self, htmlfilepath):
        if e(htmlfilepath):
            mode = 'a'
        else:
            mode = 'w'
        self.file = open(htmlfilepath, mode)
        if mode == 'a':
            self.file.write('\n')
        if mode == 'a':
            self.html = open(htmlfilepath, 'r').read()
        else:
            self.html = ''
        self.read = open(htmlfilepath, 'r')
        self.htmlfilepath = htmlfilepath
    def add(self, changes):
        self.html += changes
        self.html += '\n'
    def delete(self, changes):
        self.html.rstrip(changes)
    def commit(self):
        self.file.write(self.html)
    def correct(self):
        html = self.read.read() + self.html
        if not html.endswith('</html>'):
            self.html += '</html>'
        if not html.startswith('<DOCTYPE html>'):
            self.file.close()
            del self.file
            self.file = open(self.htmlfilepath, 'w')
            self.file.write('<DOCTYPE html>\n' + html)
    def getHTML(self):
        return self.read.read() + self.html
    def quit(self):
        del self.html
        self.file.close()
        del self.file
        del self.read
        del self.htmlfilepath
        del self
        return None
