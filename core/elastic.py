import config
from elasticsearch import Elasticsearch
import requests
class ElasticWrapper(object):
    """
    A wrapper for elasticsearch
    """

    def __init__(self):
        self.es = Elasticsearch(hosts=[config.ELASTIC_HOST])

    def insert_document(self, doc):
        if type(doc) == dict:
            try:
                self.es.index(
                    index=config.ELASTIC_INDEX,
                    doc_type='blockchain',
                    body=doc
                )
                return True
            except Exception as e:
                raise Exception(e)
        return False

    def flush_document(self):
        requests.delete(config.ELASTIC_HOST + '/' + config.ELASTIC_INDEX)
        return True

    def search_document(self, keyword):
        query = {
            'query': {
                'query_string': {
                    'query': '*' + keyword +'*'
                }
            }
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.get(config.ELASTIC_HOST + '/_search',
                         headers=headers,
                         json=query
        ).json()
        return r['hits']['hits']

