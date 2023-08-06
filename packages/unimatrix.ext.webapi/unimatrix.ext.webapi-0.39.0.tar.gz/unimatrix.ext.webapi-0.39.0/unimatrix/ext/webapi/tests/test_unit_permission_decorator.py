# pylint: skip-file
import unittest

from unimatrix.ext import webapi


class NullPermissionDecoratorTestCase(unittest.TestCase):

    class view_class(webapi.EndpointSet):

        def retrieve(self):
            pass


    def test_get_permissions_returns_decorated(self):
        view = self.view_class('retrieve')
        self.assertEqual(view.get_permissions(), set())


class PermissionDecoratorTestCase(unittest.TestCase):

    class view_class(webapi.EndpointSet):

        @webapi.permission("foo")
        def retrieve(self):
            pass


    def test_get_permissions_returns_decorated(self):
        view = self.view_class('retrieve')
        self.assertEqual(view.get_permissions(), {"foo"})


class MultiPermissionDecoratorTestCase(unittest.TestCase):

    class view_class(webapi.EndpointSet):

        @webapi.permission("foo")
        @webapi.permission("bar")
        def retrieve(self):
            pass


    def test_get_permissions_returns_decorated(self):
        view = self.view_class('retrieve')
        self.assertEqual(view.get_permissions(), {"foo", "bar"})
