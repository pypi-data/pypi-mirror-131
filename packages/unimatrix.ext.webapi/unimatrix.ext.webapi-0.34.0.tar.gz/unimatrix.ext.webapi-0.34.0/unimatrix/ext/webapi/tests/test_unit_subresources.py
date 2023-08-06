# pylint: skip-file
import unittest

from unimatrix.ext import webapi


class SubresourceTestCase(unittest.TestCase):

    class parent(webapi.Endpoint):
        resource_name = 'foo'
        path_parameter = 'foo_id'

        class child(webapi.Endpoint):
            resource_name = 'bar'
            path_parameter = 'bar_id'

        subresources = [child]

    def test_qualname_returns_proper_path_parent(self):
        endpoint = self.parent(None)
        self.assertEqual(endpoint.qualname, 'foo')

    def test_qualname_returns_proper_path(self):
        endpoint = self.parent.child(None)
        self.assertEqual(endpoint.qualname, 'foo.bar')

    def test_path_parameters(self):
        endpoint = self.parent.child(None)
        self.assertEqual(len(endpoint.parameters), 2)
        foo, bar = endpoint.parameters
        self.assertEqual(foo.name, 'foo_id')
        self.assertEqual(bar.name, 'bar_id')
