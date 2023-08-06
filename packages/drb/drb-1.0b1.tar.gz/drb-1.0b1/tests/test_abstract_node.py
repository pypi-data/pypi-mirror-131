import sys
import unittest
import os

from drb import DrbNode
from drb.exceptions import DrbNotImplementationException
from drb.utils.logical_node import DrbLogicalNode
from drb.predicat import Predicate


class MyPredicate(Predicate):
    def matches(self, node: DrbNode) -> bool:
        return 'a' == node.namespace_uri


class TestDrbNode(unittest.TestCase):
    mock_package_path = None
    node = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_package_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'resources', 'packages'))
        sys.path.append(cls.mock_package_path)

        cls.node = DrbLogicalNode(os.getcwd())
        cls.node.append_child(DrbLogicalNode('data1.zip'))
        cls.node.append_child(DrbLogicalNode('data1.zip', namespace_uri='a'))
        child = DrbLogicalNode('data2.txt')
        child.add_attribute('occurrence', 1)
        cls.node.append_child(child)
        child = DrbLogicalNode('data2.txt')
        child.add_attribute('occurrence', 2)
        cls.node.append_child(child)
        cls.node.append_child(DrbLogicalNode('data2.txt', namespace_uri='b'))

    @classmethod
    def tearDownClass(cls) -> None:
        sys.path.remove(cls.mock_package_path)

    def test_getitem_int(self):
        node = self.node[1]
        self.assertEqual('data1.zip', node.name)
        self.assertEqual('a', node.namespace_uri)
        self.assertEqual("<class 'zip.ZipNode'>", str(node.__class__))

        with self.assertRaises(IndexError):
            node = self.node[42]
        with self.assertRaises(IndexError):
            node = self.node[-1]

    def test_getitem_str(self):
        data = self.node['data2.txt']
        self.assertEqual(1, data.get_attribute('occurrence'))
        self.assertEqual("<class 'txt.TextNode'>", str(data.__class__))

        with self.assertRaises(KeyError):
            data = self.node['foobar']

    def test_getitem_tuple(self):
        with self.assertRaises(KeyError):
            data = self.node['data2.txt', ]

        data = self.node['data2.txt', 'b']
        self.assertIsInstance(data, DrbNode)
        self.assertEqual('data2.txt', data.name)
        self.assertEqual('b', data.namespace_uri)
        self.assertEqual("<class 'txt.TextNode'>", str(data.__class__))

        data = self.node['data2.txt', 2]
        self.assertIsInstance(data, DrbNode)
        self.assertEqual(2, data.get_attribute('occurrence'))
        self.assertEqual("<class 'txt.TextNode'>", str(data.__class__))

        data = self.node['data1.zip', 'a', 1]
        self.assertIsInstance(data, DrbNode)
        self.assertEqual('data1.zip', data.name)
        self.assertEqual('a', data.namespace_uri)
        self.assertEqual("<class 'zip.ZipNode'>", str(data.__class__))

        data = self.node['data1.zip', None, 1]
        self.assertIsInstance(data, DrbNode)
        self.assertIsNone(data.namespace_uri)
        self.assertEqual("<class 'zip.ZipNode'>", str(data.__class__))

        data = self.node['data1.zip', 2]
        self.assertIsNotNone(data)
        self.assertEqual('data1.zip', data.name)
        self.assertEqual('a', data.namespace_uri)

    def test_getitem_predicate(self):
        data = self.node[MyPredicate()]
        self.assertIsInstance(data, list)
        self.assertEqual(1, len(data))
        self.assertEqual("a", data[0].namespace_uri)
        self.assertEqual("<class 'zip.ZipNode'>", str(data[0].__class__))

    def test_truediv_str(self):
        data = self.node / 'data2.txt'
        self.assertIsInstance(data, DrbNode)
        self.assertEqual(1, data.get_attribute('occurrence'))
        self.assertEqual("<class 'txt.TextNode'>", str(data.__class__))

    def test_truediv_tuple(self):
        with self.assertRaises(DrbNotImplementationException):
            data = self.node / ('data2.txt',)

        data = self.node / ('data2.txt', 'b')
        self.assertIsInstance(data, DrbNode)
        self.assertEqual('data2.txt', data.name)
        self.assertEqual('b', data.namespace_uri)
        self.assertEqual("<class 'txt.TextNode'>", str(data.__class__))

        data = self.node / ('data2.txt', 1)
        self.assertIsInstance(data, DrbNode)
        self.assertEqual(1, data.get_attribute('occurrence'))
        self.assertEqual("<class 'txt.TextNode'>", str(data.__class__))

        data = self.node / ('data1.zip', 'a', 1)
        self.assertIsInstance(data, DrbNode)
        self.assertEqual('data1.zip', data.name)
        self.assertEqual('a', data.namespace_uri)
        self.assertEqual("<class 'zip.ZipNode'>", str(data.__class__))

        data = self.node / ('data1.zip', None, 1)
        self.assertIsInstance(data, DrbNode)
        self.assertEqual('data1.zip', data.name)
        self.assertIsNone(data.namespace_uri)
        self.assertEqual("<class 'zip.ZipNode'>", str(data.__class__))

        with self.assertRaises(KeyError):
            data = self.node / ('data1.zip', 42)
        with self.assertRaises(KeyError):
            data = self.node / ('foobar', 3)

    def test_truediv_predicate(self):
        data = self.node / MyPredicate()
        self.assertIsInstance(data, list)
        self.assertEqual(1, len(data))
        self.assertEqual("<class 'zip.ZipNode'>", str(data[0].__class__))

    def test_namespace_11(self):
        # Case 1.1: node with ns / user access with ns / aware = True
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml', namespace_uri=ns)

        root.append_child(ns_node)
        root.namespace_aware = True

        self.assertIsNotNone(root['xml', ns])
        with self.assertRaises(KeyError):
            self.assertIsNone(root['xml', ns + 'bad_ns'])

    def test_namespace_12(self):
        # Case 1.2: node with ns / user access with ns / aware = False
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml', namespace_uri=ns)

        root.append_child(ns_node)
        ns_node.namespace_aware = False

        self.assertIsNotNone(root['xml', ns])
        with self.assertRaises(KeyError):
            node = root['xml', ns + 'bad_ns']
            print(node)

    def test_namespace_21(self):
        # Case 2.1: node without ns / user access with ns / aware = True
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml')

        root.append_child(ns_node)
        root.namespace_aware = True

        with self.assertRaises(KeyError):
            node = root['xml', ns]
            print(node)

    def test_namespace_22(self):
        # Case 2.2: node without ns / user access with ns / aware = False
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml')

        root.append_child(ns_node)
        ns_node.namespace_aware = False

        with self.assertRaises(KeyError):
            node = root['xml', ns]
            print(node)

    def test_namespace_31(self):
        # Case 3.1: node with ns / user access without ns / aware = True
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml', namespace_uri=ns)

        root.append_child(ns_node)
        root.namespace_aware = True

        with self.assertRaises(KeyError):
            node = root['xml']
            print(node)

    def test_namespace_32(self):
        # Case 3.2: node with ns / user access without ns / aware = False
        root = DrbLogicalNode("root")
        ns = 'http://www.gael.fr/drb/item'
        ns_node = DrbLogicalNode('xml', namespace_uri=ns)

        root.append_child(ns_node)
        ns_node.namespace_aware = False

        self.assertIsNotNone(root['xml'])

    def test_namespace_41(self):
        # Case 4.1: node without ns / user access without ns / aware = True
        root = DrbLogicalNode("root")
        ns_node = DrbLogicalNode('xml')

        root.append_child(ns_node)
        root.namespace_aware = True

        self.assertIsNotNone(root['xml'])

    def test_namespace_42(self):
        # Case 4.1: node without ns / user access without ns / aware = False
        root = DrbLogicalNode("root")
        ns_node = DrbLogicalNode('xml')

        root.append_child(ns_node)
        ns_node.namespace_aware = False

        self.assertIsNotNone(root['xml'])

    def test_namespace_aware_transitivity(self):
        root = DrbLogicalNode('root')
        self.assertFalse(root.namespace_aware)

        a_child = DrbLogicalNode('a')
        a_child.append_child(DrbLogicalNode('aa'))
        a_child.append_child(DrbLogicalNode('ab', namespace_uri='a'))
        b_child = DrbLogicalNode('b')
        b_child.append_child(DrbLogicalNode('ba'))
        b_child.append_child(DrbLogicalNode('bb', namespace_uri='b'))
        root.append_child(a_child)
        root.append_child(b_child)

        # Default namespace_aware value (False)
        self.assertFalse(root['a'].namespace_aware)
        self.assertFalse(root['a']['aa'].namespace_aware)
        node = root['a']['ab']
        self.assertIsNotNone(node)
        self.assertFalse(node.namespace_aware)
        self.assertEqual('a', node.namespace_uri)
        self.assertFalse(root['a']['ab'].namespace_aware)
        self.assertFalse(root['b'].namespace_aware)
        self.assertFalse(root['b']['ba'].namespace_aware)
        node = root['b']['bb']
        self.assertIsNotNone(node)
        self.assertFalse(node.namespace_aware)
        self.assertEqual('b', node.namespace_uri)

        # set namespace_aware to True only on root node
        root.namespace_aware = True
        self.assertTrue(root['a'].namespace_aware)
        self.assertTrue(root['a']['aa'].namespace_aware)
        with self.assertRaises(KeyError):
            node = root['a']['ab']
        self.assertTrue(root['b'].namespace_aware)
        self.assertTrue(root['b']['ba'].namespace_aware)
        with self.assertRaises(KeyError):
            node = root['b']['bb']

        # Override namespace_aware property
        root.namespace_aware = False
        b_child.namespace_aware = True
        self.assertFalse(root['a'].namespace_aware)
        self.assertFalse(root['a']['aa'].namespace_aware)
        self.assertFalse(root['a']['ab'].namespace_aware)
        self.assertTrue(root['b'].namespace_aware)
        self.assertTrue(root['b']['ba'].namespace_aware)
        with self.assertRaises(KeyError):
            node = root['b']['bb']
