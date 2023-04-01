import jsonrpcclient
import requests


class JSONRPCClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def call(self, method, params):
        response = requests.post(self.endpoint, json={
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params,
        })

        response.raise_for_status()
        result = response.json()['result']

        return result

if __name__ == '__main__':
    # Create a client for the JSON-RPC server at the specified endpoint
    client = JSONRPCClient('http://localhost:8000/jsonrpc')

    # Call a method on the server
    response = client.call('example_method', [1, 2, 3])
    print(response)
