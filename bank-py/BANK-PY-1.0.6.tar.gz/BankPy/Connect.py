class Connect:
    class Path:
        def Pop(self):
            init = f'{self}\\__init__.py'
            try:
                sistema = open(init,'at')
            except:
                print("Não Encontramos nenhum arquivo no caminho definido")
            else:
                return init

    def Pop(self):
        try:
            sistema = open(self,'at')
        except:
            print("Não Encontramos nenhum arquivo no caminho definido")
        else:
            return self
        
    