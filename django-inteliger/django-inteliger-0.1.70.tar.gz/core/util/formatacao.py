def numero_string_br(valor=0, casas_decimais=2):
    """
    :Nome da classe/função: numero_string_br
    :descrição: Função para formatar numeros em string no formato brasileiro
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    :param valor:
    :param casas_decimais:
    :return:
    """
    try:
        return format(valor, '.{}f'.format(str(casas_decimais))).replace('.', '*').replace(',', '.').replace('*', ',')
    except:
        return '0,00'
