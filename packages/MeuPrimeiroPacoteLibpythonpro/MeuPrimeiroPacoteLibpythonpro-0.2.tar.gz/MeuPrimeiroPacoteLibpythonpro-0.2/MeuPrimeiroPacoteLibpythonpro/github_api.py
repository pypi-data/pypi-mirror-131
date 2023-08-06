import requests


def busca_avatar(usuario):
    """Busca o avatar de um usuário no github
    :param usuario: str como o nome do usuário no github
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/{usuario}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(busca_avatar('Arthurregismais'))
