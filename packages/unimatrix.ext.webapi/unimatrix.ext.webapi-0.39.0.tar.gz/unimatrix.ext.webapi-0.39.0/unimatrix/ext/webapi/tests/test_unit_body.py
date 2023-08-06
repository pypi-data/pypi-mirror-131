# pylint: skip-file
import unittest

import pydantic
from fastapi.testclient import TestClient

from unimatrix.ext import webapi


class DictBodyTestCase(unittest.TestCase):

    class view_class(webapi.PublicEndpointSet):

        async def create(self, dto: dict):
            return dto

    def setUp(self):
        self.app = webapi.Application(
            allowed_hosts=['*']
        )
        self.client = TestClient(self.app)
        self.view_class.add_to_router(self.app, '/')

    def test_body_is_parsed(self):
        response = self.client.post('/', json={'foo': 'bar'})
        dto = response.json()
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn('foo', dto)
        self.assertEqual(dto['foo'], 'bar')



class Model(pydantic.BaseModel):
	foo: str


class ModelBodyTestCase(DictBodyTestCase):

    class view_class(webapi.PublicEndpointSet):

        async def create(self, dto: Model):
            return dto
