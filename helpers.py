import os.path
import json

from requests import session, Session, Response


def load_json_schema(name:str):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'schems', name)
    with open(schema_path) as schema:
        return json.loads(schema.read())


class Custom_session(Session):
    def  __init__(self, base_url):
        self.base_url = base_url
        super().__init__()
    def request(self, method, url, *args, **kwargs) -> Response:
        return super(Custom_session, self).request(method=method, url=self.base_url + url, *args, **kwargs)


    # reqres_session = CustomSession("https://reqres.in")