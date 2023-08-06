import requests
import pprint # pretty print

class KGClient:
    def __init__(self, host, port, domain, user=None, password=None):
        self.url = lambda query: f'http://{host}:{port}/execute/{domain}/?query={query}'
        self.auth = None
        if user and password:
            self.auth = requests.auth.HTTPBasicAuth(user, password)
        self.set_pretty_print(False)
        
    def set_authentication(self, user, password):
        self.auth = requests.auth.HTTPBasicAuth(user, password)

    def set_pretty_print(self, pretty_print):
        self.pretty_print = pretty_print

    # helper function
    def query(self, text, pretty_print=None):
        url_string = self.url(text)

        # execute the query
        try:
            response = requests.get(url_string, auth=self.auth)
            if (response.status_code == 200):
                response_json = response.json()
                if (pretty_print if pretty_print != None else self.pretty_print):
                    pprint.PrettyPrinter(indent=1, width=30)
                    pprint.pprint(response_json)
                return response_json
            else:
                print(response.text)
                return None
        except requests.exceptions.ConnectionError as e:
            print("Could not reach server")
