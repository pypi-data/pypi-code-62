from os import system

class Execute:

    def Pop(self):
        system(self)

    class Path():
        def Pop(self):
            self = self+'\\__init__.py'
            var = False
            try:
                a = open(self,'at')
            except:
                var = False

            else:
                var = True
            finally:
                a.close()
                
            if var == True:
                system(self)
            else:
                print('Não Foi Possivel Executa O Caminho Defindo')


