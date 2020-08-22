from os import mkdir

class Create():
    class Path():
        def Pop(self):
            """
            Ciar Uma Pasta Com Armazen de 
            Dados Dentro, diferente do Pop Normal
            Este Dados sé Você Estiver Desenvolvendo
            Algum Tipo de Aplicação Que Será Salva como
            Exe esta função e melhor pois será posivel ler 
            pega os dados Da Aplicação Aplicação ja no pop normal
            so é possivel peda os dados da aplicação executando como script

            self = "Nome Da Pasta a ser Criada"
            """

            try:
                mkdir(self)
            except:
                pass

            init = f'{self}\\__init__.py'

            try:
                dado = open(init,'at')
            except:
                dado = open(init,'wt+')
            else:
                print('Ja Foi Criada A Pasta Definida')
            finally:
                dado.close()
            

            
        


    def Pop(self):

        """
        Cria Um Armazen Para Dados
        Estes Dados Jamais Serão Perdidos
        Mais se você estiver criando uma aplicação
        Que será salva como exe esta função não é recomendada
        Pois Não será Possivel Pega os Dados apenas será possivel
        Pega Os Dados Rodando Como Script

        self = 'Nome Do Arquivo a Ser Criado'

        lenbrando não esqueça de adiciona a estenção .py :)
    
        """

        try:
            dado = open(self,'at')
        except:
            dado = open(self,'wt+')
        else:
            print('este arquivo ja foi criado')
        finally:
            dado.close()
        

    



