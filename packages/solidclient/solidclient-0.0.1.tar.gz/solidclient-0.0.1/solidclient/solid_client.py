import requests
import jwcrypto.jwk
import jwcrypto.jwt
import json
import datetime
from rdflib import Graph

from solidclient.utils.utils import make_random_string


class SolidSession:
    # jwcrypto.jwk.JWK
    keypair = None
    access_token = None

    def __init__(self, keypair, access_token):
        self.keypair = keypair
        self.access_token = access_token

    @staticmethod
    def make_token(keypair, uri, method):
        jwt = jwcrypto.jwt.JWT(
            header={
                "typ": "dpop+jwt",
                "alg": "ES256",
                "jwk": keypair.export(private_key=False, as_dict=True)
            },
            claims={
                "jti": make_random_string(),
                "htm": method,
                "htu": uri,
                "iat": int(datetime.datetime.now().timestamp())
            })

        jwt.make_signed_token(keypair)
        return jwt.serialize()

    def make_headers(self, uri, method):
        return {
            "Authorization": ("DPoP " + self.access_token),
            "DPoP": self.make_token(self.keypair, uri, method)
        }

    def send_request(self, keypair, uri, method, data=None):
        headers = self.make_headers(uri, method)

        if method == "GET":
            resp = requests.get(uri, headers=headers)
            print(resp)
            print(resp.status_code)
            print(resp.text)
            print(resp.headers)

            return SolidResponse(
                resp.status_code,
                resp.headers["Content-Type"] if "Content-Type" in resp.headers else None,
                resp.text
            )

        elif method == "DELETE":
            resp = requests.delete(uri, headers=headers)

            return SolidResponse(
                resp.status_code,
                resp.headers["Content-Type"] if "Content_Type" in resp.headers else None,
                resp.text
            )

        # Is POST needed? Just PUT 4Head
        elif method == "POST":
            return 405

        elif method == "PUT":
            headers["Content-Type"] = "text/turtle"
            resp = requests.put(uri, headers=headers, data=data)

            return SolidResponse(
                resp.status_code,
                resp.headers["Content-Type"] if "Content-Type" in resp.headers else None,
                resp.text
            )

    def get(self, uri):
        return self.send_request(self.keypair, uri, "GET")

    # data = rdflib.Graph
    def put(self, uri, data):
        return self.send_request(self.keypair, uri, "PUT", data=data)

    def delete(self, uri):
        return self.send_request(self.keypair, uri, "DELETE")

    def post(self, uri):
        pass


class SolidResponse:
    status_code = None
    content_type = None

    # rdblib.Graph
    rdf_graph = None

    raw_text = None

    def __init__(self, status_code, content_type, raw_text):
        # Or other RDF types
        if content_type == "text/turtle":
            self.rdf_graph = Graph().parse(data=raw_text)

        self.status_code = status_code
        self.content_type = content_type
        self.raw_text = raw_text

    def get_graph(self):
        return self.rdf_graph


class SolidClient:

    def __init__(self, key, access_token):
        self.key = key
        self.access_token = access_token

    # Refresh_token
    @staticmethod
    def login(key, token):
        return SolidSession(key, token)

    def login_key_access_token(self):
        return SolidSession(
            jwcrypto.jwk.JWK.from_json(json.dumps(self.key)),
            self.access_token
        )
