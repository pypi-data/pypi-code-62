from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class VuetifyTreeProcessor(Treeprocessor):
    def run(self, root):
        for elem in root:
            if elem.tag == 'h1':
                elem.set('class', 'text-h1')
            elif elem.tag == 'h2':
                elem.set('class', 'text-h2')
            elif elem.tag == 'h3':
                elem.set('class', 'text-h3')
            elif elem.tag == 'h4':
                elem.set('class', 'text-h4')
            elif elem.tag == 'h5':
                elem.set('class', 'text-h5')
            elif elem.tag == 'h6':
                elem.set('class', 'text-h6')
            elif elem.tag == 'p':
                elem.set('class', 'text-body-1')


class PythonVuetifyMarkdown(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.add('pythonvuetifymarkdown', VuetifyTreeProcessor(), '>prettify')
