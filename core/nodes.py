from config import API_NODE
import socket
import requests

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
    nodes.append(API_NODE)
    for node in _nodes:
        n = "http://{}:{}".format(
            node['node_address'],
            node['node_port'])
        nodes.append(n)
    return nodes

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def register_self_node(port):
    ip = get_ip_address()
    # register with api node
    data = {
        'node_address': ip,
        'node_port': port,
        'is_confirm': True
    }
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(API_NODE + "/node-register",
                          json=data,
                          headers=headers)
        if r.status_code == 201:
            return True
        else:
            return False
    except Exception:
        return False

