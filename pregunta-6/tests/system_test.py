from ..src.database import InterpreterDatabase
from ..src.libparse import ExpParser
from ..src.datamodel import Rule, Struct, Atom, Variable, UEQT, merge_scopes
import unittest


class SystemTest(unittest.TestCase):

    def test_parser(self):
        e = ExpParser()
        rule = e.inter(
            "ancestro(f(X, Y), Y) padre(X, pepe(a, Y)) ancestro(Z, Y)")

        self.assertEqual(
            rule,
            Rule(
                Struct("ancestro", [
                    Struct("f", [Variable("X"), Variable("Y")]),
                    Variable("Y")
                ]),
                [
                    Struct("padre", [
                        Variable("X"),
                        Struct("pepe", [Atom("a"), Variable("Y")])
                    ]),
                    Struct("ancestro", [
                        Variable("Z"),
                        Variable("Y")
                    ])
                ]
            )
        )

    def test_textual_subs(self):
        e = ExpParser()
        rule = e.inter(
            "ancestro(f(X, Y), Y) padre(X, pepe(a, Y)) ancestro(Z, Y)")

        scope = {
            UEQT(Variable('X'), Struct('g', [Atom('a'), Atom('b')])),
            UEQT(Variable('Y'), Atom('c'))
        }

        tx = rule.textual_sub(scope)
        expected_result = e.inter(
            "ancestro(f(g(a, b), c), c) padre(g(a, b), pepe(a, c)) ancestro(Z, c)")

        self.assertEqual(tx, expected_result)

    def test_scope_merge(self):
        e = ExpParser()
        A = {
            UEQT(e.inter('X'), e.inter('a')),
            UEQT(e.inter('Y'), e.inter('b'))
        }

        B = {
            UEQT(e.inter('X'), e.inter('a')),
            UEQT(e.inter('Y'), e.inter('Z')),
            UEQT(e.inter('Z'), e.inter('Y'))
        }

        expected = {
            UEQT(e.inter('X'), e.inter('a')),
            UEQT(e.inter('Y'), e.inter('b')),
            UEQT(e.inter('Z'), e.inter('b'))
        }

        self.assertEqual(merge_scopes(A, B), expected)

        A = {
            UEQT(e.inter('X'), e.inter('fun(Y, Z)'))
        }

        B = {
            UEQT(e.inter('Y'), e.inter('b'))
        }

        expected = {
            UEQT(e.inter('X'), e.inter('fun(b, Z)')),
            UEQT(e.inter('Y'), e.inter('b'))
        }

        self.assertEqual(merge_scopes(A, B), expected)

        A = {
            UEQT(e.inter('X'), e.inter('fun(a, Z)'))
        }

        B = {
            UEQT(e.inter('X'), e.inter('fun(K, b)'))
        }

        expected = {
            UEQT(e.inter('X'), e.inter('fun(a, b)')),
            UEQT(e.inter('Z'), e.inter('b')),
            UEQT(e.inter('K'), e.inter('a'))
        }

        self.assertEqual(merge_scopes(A, B), expected)

    def test_unification(self):
        e = ExpParser()

        a = e.inter("ancestro(X, Y) padre(X, Z) ancestro(Z, Y)")
        b = e.inter("ancestro(X, gaby)")

        scope, uni = a.unificate(b)

        expected_scope = {
            UEQT(e.inter('Y'), e.inter('gaby'))
        }

        expected_uni = [
            e.inter("padre(X, Z)"),
            e.inter("ancestro(Z, gaby)")
        ]

        self.assertEqual(scope, expected_scope)
        self.assertEqual(uni, expected_uni)

        a = e.inter("ancestro(f(X, Y), Y) padre(X, pepe(a, Y)) ancestro(Z, Y)")
        b = e.inter("ancestro(f(a, b), gaby)")

        scope, uni = a.unificate(b)

        expected_scope = None

        expected_uni = None

        self.assertEqual(scope, expected_scope)
        self.assertEqual(uni, expected_uni)

        a = e.inter("ancestro(f(X, Y), Y) padre(X, pepe(a, Y)) ancestro(Z, Y)")
        b = e.inter("ancestro(f(a, gaby), gaby)")

        scope, uni = a.unificate(b)

        expected_scope = {
            UEQT(e.inter('Y'), e.inter('gaby')),
            UEQT(e.inter('X'), e.inter('a'))
        }

        expected_uni = [
            e.inter("padre(a, pepe(a, gaby))"),
            e.inter("ancestro(Z, gaby)")
        ]

        self.assertEqual(scope, expected_scope)
        self.assertEqual(uni, expected_uni)

    def test_namespace(self):
        e = ExpParser()
        a = e.inter("ancestro(X, Y) padre(X, Z) ancestro(Z, Y, H, J)")

        self.assertEqual(a.namespace, {"X", "Y", "Z", "H", "J"})

    def test_query(self):
        s = InterpreterDatabase()
        e = ExpParser()

        s.define("padre(juan, jose)")
        s.define("padre(jose, pablo)")
        s.define("padre(pablo, gaby)")
        s.define("ancestro(X, Y) padre(X, Y)")
        s.define("ancestro(X, Y) padre(X, Z) ancestro(Z, Y)")

        expected_sols = [
            {UEQT(e.inter('X'), e.inter('pablo'))},
            {UEQT(e.inter('X'), e.inter('juan'))},
            {UEQT(e.inter('X'), e.inter('jose'))}
        ]
        count = 0
        expected_count = 3

        q = s.parse_ask("ancestro(X, gaby)")

        for sol in s.query([q]):
            if sol is None:
                break

            if count < len(expected_sols):
                self.assertEqual(sol, expected_sols[count])
            count += 1

        self.assertEqual(count, expected_count)
