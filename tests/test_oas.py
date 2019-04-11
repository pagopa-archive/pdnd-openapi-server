#
# run me with nosetests -vs test_oas.py
#
import logging
import sys
from base64 import encodestring

import connexion

from flask_testing import TestCase
from util import FakeResolver

me = sys.modules[__name__]


class BaseTestCase(TestCase):
    def create_app(self):
        logging.getLogger("connexion.operation").setLevel("ERROR")
        app = connexion.App(__name__, specification_dir=".")
        app.add_api("../openapi/daf-openapi.yaml")
        return app.app


def test_oas3():
    files = ("../openapi/daf-openapi.yaml",)

    def assert_parse_oas3(zapp, f):
        zapp.add_api(f, resolver=FakeResolver(me))

    for f in files:
        zapp = connexion.FlaskApp(__name__, specification_dir=".")
        yield assert_parse_oas3, zapp, f


class TestPublicController(BaseTestCase):
    """PublicController integration test stubs"""

    def test_get_echo_404(self):
        response = self.client.open("/echo", method="GET")
        self.assert404(
            response, "Response body is : " + response.data.decode("utf-8")
        )

    def test_get_status(self):
        response = self.client.open("/status", method="GET")
        self.assert200(
            response, "Response body is : " + response.data.decode("utf-8")
        )

    def test_get_jwt_401_no_credentials(self):  # Authorization
        response = self.client.open("/jwt", method="GET")
        self.assert401(
            response, "Response body is : " + response.data.decode("utf-8")
        )
        assert "title" in response.json

    def test_get_jwt_401_bad_credentials(self):
        response = self.client.open(
            "/jwt",
            method="GET",
            headers={
                "Authorization": "Basic "
                + encodestring(b"user:secret").decode().strip()
            },
        )
        self.assert401(
            response, "Response body is : " + response.data.decode("utf-8")
        )
        raise NotImplementedError

    def test_post_public_search_requires_auth(self):
        response = self.client.open("/public/search", method="POST")
        self.assert401(
            response, "Response body is : " + response.data.decode("utf-8")
        )
        assert "title" in response.json

    def test_post_public_search_bad_auth(self):
        response = self.client.open(
            "/public/search",
            method="POST",
            headers={
                "Authorization": "Bearer "
                + encodestring(b"user:secret").decode().strip()
            },
        )
        self.assert401(
            response, "Response body is : " + response.data.decode("utf-8")
        )
        assert "title" in response.json
