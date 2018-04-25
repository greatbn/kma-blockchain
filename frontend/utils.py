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

