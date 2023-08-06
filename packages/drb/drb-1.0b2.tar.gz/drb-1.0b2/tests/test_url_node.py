import io
import os
import string
import unittest
import tempfile
import random

from drb.utils.url_node import UrlNode
from drb.exceptions import DrbException
from .utils import DrbTestPredicate


class TestUrlNode(unittest.TestCase):
    data = None
    path = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = ''.join(
            random.choice(string.ascii_letters) for _ in range(100))
        fd, cls.path = tempfile.mkstemp()
        with open(cls.path, 'w') as file:
            file.write(cls.data)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.path)

    def test_namespace_uri(self):
        node = UrlNode(self.path)
        self.assertIsNone(node.namespace_uri)

    def test_name(self):
        node = UrlNode(f'file://{self.path}')
        self.assertEqual(os.path.basename(self.path), node.name)

    def test_value(self):
        node = UrlNode(self.path)
        self.assertIsNone(node.value)

    def test_path(self):
        node = UrlNode(self.path)
        self.assertEqual(self.path, node.path.path)
        node = UrlNode(f'file://{self.path}')
        self.assertEqual(self.path, node.path.path)

    def test_parent(self):
        node = UrlNode(self.path)
        self.assertIsNone(node.parent)

    def test_attributes(self):
        node = UrlNode(self.path)
        self.assertEqual({}, node.attributes)

    def test_get_attribute(self):
        node = UrlNode(self.path)
        with self.assertRaises(DrbException):
            node.get_attribute('test')

    def test_children(self):
        node = UrlNode(self.path)
        self.assertEqual([], node.children)

    def test_has_child(self):
        node = UrlNode(self.path)
        self.assertFalse(node.has_child())

    def test_has_impl(self):
        node = UrlNode(self.path)
        self.assertTrue(node.has_impl(io.BytesIO))
        self.assertFalse(node.has_impl(str))

    def test_get_impl(self):
        node = UrlNode(self.path)
        with node.get_impl(io.BytesIO) as stream:
            self.assertEqual(self.data.encode(), stream.read())

        with self.assertRaises(DrbException):
            node.get_impl(str)

    def test_getitem(self):
        node = UrlNode(self.path)
        n = None
        with self.assertRaises(DrbException):
            n = node[0]
        with self.assertRaises(DrbException):
            n = node['foo']
        with self.assertRaises(DrbException):
            n = node['foo', 'bar']
        with self.assertRaises(DrbException):
            n = node['foo', 1]
        with self.assertRaises(DrbException):
            n = node['foo', 'bar', 1]
        with self.assertRaises(DrbException):
            n = node[DrbTestPredicate()]

    def test_truediv(self):
        node = UrlNode(f'file://{self.path}')
        n = None
        with self.assertRaises(DrbException):
            n = node / 'foo'
        with self.assertRaises(DrbException):
            n = node / ('foo', 'bar')
        with self.assertRaises(DrbException):
            n = node / ('foo', 1)
        with self.assertRaises(DrbException):
            n = node / ('foo', 'bar', 1)
        with self.assertRaises(DrbException):
            n = node / ('foo', 'bar')
        with self.assertRaises(DrbException):
            n = node / DrbTestPredicate()

    def test_len(self):
        node = UrlNode(self.path)
        self.assertEqual(0, len(node))

    def test_close(self):
        node = UrlNode(self.path)
        node.close()
