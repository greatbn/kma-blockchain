def get_list_node(mongo_conn):
    """
    get from database and parse to a list of node
    example return:
    nodes = [
        'http://10.5.8.50:5000',
        'http://103.4.56.100:5000'
    ]
    """
    _nodes = mongo_conn.query_confirm_node()
    nodes = []
    for node in _nodes:
        n = "http://{}:{}".format(
            node['node_addresds'],
            node['node_port'])
        nodes.append(n)
    return nodes
