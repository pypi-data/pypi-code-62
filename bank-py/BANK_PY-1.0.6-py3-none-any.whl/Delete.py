from os import system  
class Delete:
    class Path():
        def Pop(self):
            system(f'del {self}\\__init__.py ')
            system(f'rmdir {self}')

    def Pop(self):
        system(f'del {self}')


