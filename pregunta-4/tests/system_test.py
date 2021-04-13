from ..src.system import VirtualMethodsSystem
import unittest


class SystemTest(unittest.TestCase):

    def test_workflow(self):
        s = VirtualMethodsSystem()

        s.define('A f g')
        self.assertTrue('A' in s.definitions)

        s.define('B : A f h')
        self.assertTrue('B' in s.definitions)

        self.assertEqual(
            s.describe('B'),
            'f -> B :: f\ng -> A :: g\nh -> B :: h'
        )

        with self.assertRaises(Exception):
            s.describe('C')

        with self.assertRaises(Exception):
            s.define('H : K a b')

        with self.assertRaises(Exception):
            s.define('H a a')

        with self.assertRaises(Exception):
            s.define('B a')

        s.define('D : B h')
        self.assertTrue('D' in s.definitions)

        self.assertEqual(
            s.describe('D'),
            'f -> B :: f\ng -> A :: g\nh -> D :: h'
        )
