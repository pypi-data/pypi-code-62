__ES_URL_KEY = "ES_URL"


# es_url = "es://172.16.2.141:9200|172.16.2.142:9200|172.16.2.143:9200|172.16.2.141:9300|172.16.2.142:9300|172.16.2.143:9300/?user=sca_admin&password=Sdiwi12DI12d"

# es_ip = ["172.16.2.141",
#          "172.16.2.142",
#          "172.16.2.143", ]
# es = Elasticsearch(es_ip, http_auth=("sca_admin", "Sdiwi12DI12d"), port=9200)

class EsConfig:
    default_host = "localhost"
    default_port = 9200

    def __init__(self, url=None):
        import re
        result = re.search(
            "^(es://){0,1}([\d\.\:|]+)[/\?]*(.*)$", url)
        groups = result.groups()
        self.hosts = groups[1].split("|")
        self.params = dict([it.split('=')
                            for it in groups[2].split('&')]) if groups[2] else {}
        self.http_auth = (self.params["user"], self.params["password"])


def es_connect(url=None, cert_path="/es-cert"):
    if not url:
        from .zconfig import get_param
        url = get_param(__ES_URL_KEY)
    assert url

    from elasticsearch import Elasticsearch
    import os

    conf = EsConfig(url)
    client = Elasticsearch(hosts=conf.hosts, http_auth=conf.http_auth, ca_certs=os.path.join(
        cert_path, "client-ca.crt"), client_cert=os.path.join(cert_path, "client.crt"), client_key=os.path.join(cert_path, "client-key.crt"))
    return client
