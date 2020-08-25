import os
import requests
import json
import decimal
import time


class ApiUnous:
    _grant_type = 'password'
    _client_id = 'userIntegration'
    _mindset_user = os.environ.get('MINDSET_USER')
    _mindset_pass = os.environ.get('MINDSET_PASS')
    _mindset_url = os.environ.get('MINDSET_URL')
    _mindset_notify_url = os.environ.get('MINDSET_NOTIFY_URL')

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._get_token()}'
        }

    def integrar_produtos(self, list):
        return self._integrar(list, '/StageContent/api/Product/Post')

    def integrar_produtos_tamanhos(self, list):
        return self._integrar(list, '/StageContent/api/ProductSize/Post')

    def integrar_fornecedores(self, list):
        return self._integrar(list, '/StageContent/api/Supplier/Post')

    def integrar_pedidos(self, list):
        return self._integrar(list, '/StageMetrics/api/OpenOrder/Post')

    def integrar_lojas(self, list):
        return self._integrar(list, '/StageContent/api/Location/Post')

    def integrar_lojas_info(self, list):
        return self._integrar(list, '/StageContent/api/StoreInfo/Post')

    def integrar_metricas(self, list):
        return self._integrar(list, '/StageMetrics/api/Metric/Post')

    def notificar(self):
        params = {
            "EnterpriseKey": self._mindset_user,
            "enterprisePwd": self._mindset_pass,
            "jobName": 'CleanUpJob'
        }
        response = requests.get(url=self._mindset_notify_url, params=params)
        retorno = {
            "ok": response.ok,
            "notificou": response.text == '<boolean xmlns="http://schemas.microsoft.com/2003/10/Serialization/">true</boolean>'
        }
        return retorno

    def _integrar(self, data, url_endpoint):
        url = self._mindset_url + url_endpoint
        offset = 0
        limit = 10000
        for i in range(int(len(data) / limit) + 1):
            conteudo_a_integrar = data[offset:offset + limit]
            response = requests.post(url=url, data=json.dumps(conteudo_a_integrar, cls=DecimalEncoder),
                                     headers=self.headers)
            if not response.ok:
                break
            offset += limit
            conteudo_integrado = len(conteudo_a_integrar)
            print(f'{conteudo_integrado} REGISTROS INTEGRADOS')
            time.sleep(5)
        print('------------------------------------------')
        return response.ok, response.json()

    def limpar_pedidos(self):
        url = self._mindset_url + '/StageMetrics/api/OpenOrder/GetClearAllData'
        requests.get(url=url, headers=self.headers)

    def _get_token(self):
        response = requests.get(url=self._mindset_url + '/Auth/token', data={
            "grant_type": self._grant_type,
            "username": self._mindset_user,
            "password": self._mindset_pass,
            "client_id": self._client_id
        })
        return json.loads(response.text).get('access_token')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
