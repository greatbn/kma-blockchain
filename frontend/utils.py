import requests

def search_document(SEARCH_API, keyword):
    try:
        query = {
            'query': {
                'query_string': {
                    'query': '*' + keyword +'*'
                }
            }
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.get(SEARCH_API + '/_search',
                        headers=headers,
                        json=query
        ).json()
        return r['hits']['hits']
    except Exception as e:
        raise Exception(e)

def check_hash(SEARCH_API, doc_hash):
    try:
        query = {
            'query': {
                'query_string': {
                    'query': doc_hash
                }
            }
        }
        r = requests.get(SEARCH_API + '/blockchain/_search',
                        json=query
        ).json()
        return len(r['hits']['hits'])
    except Exception as e:
        raise Exception(e)


def create_new_transaction(data):
    url = 'http://10.5.9.110:5000/new'
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        # import ipdb;ipdb.set_trace()
        r = requests.post(url, json=data, headers=headers)
        print r.status_code
        if r.status_code == 201:
            return r.json()
        else:
            return False
    except Exception as e:
        raise Exception(e)

    
if __name__ == '__main__':
    SEARCH_API = 'http://10.5.9.110:9200'
    doc_hash = "9hkE44yyc8AkvvW0RVM8mq2341123123"
    # print check_hash(SEARCH_API, doc_hash)
    data = {'doc_hash': u'2ac3b3ed71a8c2d4c955a0e1c9e2ccb62debcdadaa2b7358752ef4f3fef42d20', 's3_url': 'https://blockchain.s3.sapham.net/2ac3b3ed71a8c2d4c955a0e1c9e2ccb62debcdadaa2b7358752ef4f3fef42d20', 'title': u'How to make life easier?', 'description': u'Make life easier is important.', 'author': u'Sa Pham Dang'}
    import json

    create_new_transaction(data)