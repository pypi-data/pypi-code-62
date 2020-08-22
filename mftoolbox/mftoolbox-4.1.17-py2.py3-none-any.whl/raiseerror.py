import inspect
from mftoolbox.constants import Color as c

def error_stack(error, message):
    """
    Imprime mensagem de erro criada pelo usuário
    Args:
        context: contexto onde o erro foi gerado
        error: nome do erro
        message: mensagem explicativa do erro

    Returns: apenas imprime o tipo de erro, a mensagem explicativa e a lista de chamadas

    """
    context = inspect.getframeinfo(inspect.currentframe(), context=1), inspect.getouterframes(inspect.currentframe(),context=1)
    error = "Erro: " + error
    print(c.dark_red_background + c.bold + c.white + error + " " * (60 - len(error)) + c.end)
    print(message)
    print('Lista de chamadas:')
    last = False
    for id1, item1 in enumerate(context[1]):
        if last:
            break
        item2 = item1[0]
        filename, lineno, function, code_context, code = inspect.getframeinfo(item2)
        if function == "<module>":
            last = True
        if function not in ('get_context', '__init__', 'error_stack'):
            function = function.replace("<module>", "__main__")
            print("file: {}, line: {}, function: {}".format(filename, lineno, function))
    exit(1)

class RaiseError(Exception):
    """
    Levanta um erro definido pelo usuário
    """

    def __init__(self, RaisedError, message):
        """

        Args:
            RaisedError: Nome do erro
            message: mensagem explicativa do erro
        """
        error_stack(RaisedError, message)