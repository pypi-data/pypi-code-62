import requests

class B2L:
    def __init__(self, token, mode = 0):
        self.token = token
        if mode == 1:
            self.base_path = 'http://host.docker.internal'
        elif mode == 2:
            self.base_path = 'http://localhost'
        else:
            self.base_path = 'https://brain2logic.com'

    def sourceList(self):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.get(self.base_path + '/source/', headers=headers)
        return response.json()
    
    def getSource(self, id):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.get(self.base_path + '/source/' + str(id) + '/', headers=headers)
        return response.json()

    def storyList(self):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.get(self.base_path + '/story/', headers=headers)
        return response.json()

    def getStory(self, id):
        headers = {'Authorization': 'Token ' + self.token}
        response = requests.get(self.base_path + '/story/' + str(id) + '/', headers=headers)
        return response.json()
