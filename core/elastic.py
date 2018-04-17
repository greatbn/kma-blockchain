import config
from elasticsearch import Elasticsearch

class ElasticWrapper(object):
    """
    A wrapper for elasticsearch
    """

    def __init__(self):
        self.es = Elasticsearch(hosts=config.ELASTIC_HOSTS)

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
        return True

    def search_document(self, keyword):
        return True

