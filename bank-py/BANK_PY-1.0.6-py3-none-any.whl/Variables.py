class Write():
    class Variable():
        class Path():
            class Str():
                def Pop(self,nome_da_variavel,conteudo_da_variavel):
                    self = self +'\\__init__.py'
                    ide = nome_da_variavel
                    metod = str(f"'{conteudo_da_variavel}'")
                    variable = f'{ide} = {metod}'
                    try:
                        with open(self,'at') as tipagem:
                            tipagem.write(f'{variable}\n')
                    except:
                        print('Não achamos nada no ponto definido')
                

            class Int():
                def Pop(self,nome_da_variavel,conteudo_da_variavel):
                    self = self + '\\__init__.py'
                    ide = nome_da_variavel
                    metod = int(conteudo_da_variavel)
                    variable = f'{ide} = {metod}'
                    try:
                        with open(self,'at') as tipagem:
                            tipagem.write(f'{variable}\n')
                    except:
                        print('Não achamos nada no ponto definido')
              

            class Float():
                def Pop(self,nome_da_variavel,conteudo_da_variavel):
                    self = self +'\\__init__.py'
                    ide = nome_da_variavel
                    metod = float(conteudo_da_variavel)
                    variable = f'{ide} = {metod}'
                    try:
                        with open(self,'at') as tipagem:
                            tipagem.write(f'{variable}\n')
                    except:
                        print('Não achamos nada no ponto definido')
                    
            class Bool():
                
                def Pop(self,nome_da_variavel,conteudo_da_variavel):
                    self = self +'\\__init__.py'
                    ide = nome_da_variavel
                    metod = conteudo_da_variavel
                    if metod == True or metod == False:
                        variable = f'{ide} = {metod}'
                        try:
                            with open(self,'at') as tipagem:
                                tipagem.write(f'{variable}\n')
                        except:
                            print('Não achamos nada no ponto definido')
                    
                    else:
                        print('É Permitido Apenas Numero Boll')











        class Str():
            def Pop(self,nome_da_variavel,conteudo_da_variavel):
                ide = nome_da_variavel
                metod = str(f"'{conteudo_da_variavel}'")
                variable = f'{ide} = {metod}'
                try:
                    with open(self,'at') as tipagem:
                        tipagem.write(f'{variable}\n')
                except:
                    print('Não achamos nada no ponto definido')
                

        class Int():
            def Pop(self,nome_da_variavel,conteudo_da_variavel):
                ide = nome_da_variavel
                metod = int(conteudo_da_variavel)
                variable = f'{ide} = {metod}'
                try:
                    with open(self,'at') as tipagem:
                        tipagem.write(f'{variable}\n')
                except:
                    print('Não achamos nada no ponto definido')
              

        class Float():
            def Pop(self,nome_da_variavel,conteudo_da_variavel):
                ide = nome_da_variavel
                metod = float(conteudo_da_variavel)
                variable = f'{ide} = {metod}'
                try:
                    with open(self,'at') as tipagem:
                        tipagem.write(f'{variable}\n')
                except:
                    print('Não achamos nada no ponto definido')
                
        class Bool():
            def Pop(self,nome_da_variavel,conteudo_da_variavel):
                ide = nome_da_variavel
                metod = conteudo_da_variavel

                if metod == True or metod == False:
                    variable = f'{ide} = {metod}'
                    try:
                        with open(self,'at') as tipagem:
                            tipagem.write(f'{variable}\n')
                    except:
                        print('Não achamos nada no ponto definido')
                   
                else:
                    print('É Permitido Apenas Numero Boll')
    class Pop():
        def Print(self,menssagem):
            menssagem = f"'{menssagem}'"
            with open(self,'at') as Dd:
                Dd.write(f'print({menssagem})')