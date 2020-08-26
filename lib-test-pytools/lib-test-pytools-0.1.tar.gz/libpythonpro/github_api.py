import requests


def buscar_avatar(usuario):
    """
    Busca o avatar de um user do GitHub

    :param usuario: str
    :return: str
    """
    url = f'https://api.github.com/users/{usuario}'
    resposta = requests.get(url)
    return resposta.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('VitorGGs'))
