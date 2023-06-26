import logging
import os.path
import json

import allure
import curlify
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from requests import session, Session, Response


def load_json_schema(name: str):
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schems', name)
    with open(schema_path) as schema:
        return json.loads(schema.read())


class Custom_session(Session):
    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def request(self, method, url, *args, **kwargs) -> Response:
        response = super(Custom_session, self).request(
            method=method, url=self.base_url + url, *args, **kwargs
        )
        curl = curlify.to_curl(response.request)
        status_code = response.status_code
        logging.info(f"Status Code: {status_code}\n{curl}")
        with step(f"{method} {url}"):
            allure.attach(
                body=f"Status Code: {status_code}\n{curl}",
                name="Request curl",
                attachment_type=AttachmentType.TEXT,
                extension="txt",
            )

            try:
                response_body = response.json()
            except json.JSONDecodeError:
                response_body = response.text

            allure.attach(
                body=json.dumps(response_body, indent=2),
                name="Response Body",
                attachment_type=AttachmentType.JSON,
            )

        return response


reqres_session = Custom_session("https://reqres.in")
