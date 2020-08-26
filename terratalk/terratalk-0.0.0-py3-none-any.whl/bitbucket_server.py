import requests
import urllib.parse

class BitbucketServer:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def comments(self, project_key=None, repository_slug=None, pull_request_id=None):
        request_url = f'{self.base_url}/rest/api/1.0/projects/{project_key}/repos/{repository_slug}/pull-requests/{pull_request_id}/activities'
        comments = []
        for value in self.paginator(request_url):
            if value['action'] == 'COMMENTED':
                comments.append(value)

        return comments


    def paginator(self, url, params={}):
        values = []

        while True:
            print(f'{url}?{urllib.parse.urlencode(params)}')
            r = requests.get(url, params=params, auth=(self.username, self.password))
            buf = r.json()

            values += buf['values']

            if buf['isLastPage']:
                break
            else:
                params['start'] = buf['nextPageStart']

        return values
