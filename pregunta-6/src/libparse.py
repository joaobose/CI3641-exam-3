from lark import Lark, Transformer
from .datamodel import Rule, Struct, Atom, Variable, UEQT, merge_scopes


class ExpTransformer(Transformer):
    # Transformer del parser

    def defi(self, val):
        consecuente = val.pop(0)
        return Rule(consecuente, val)

    def struct(self, val):
        name = val.pop(0)
        return Struct(name, val)

    def var(self, val):
        token, = val
        return Variable(token)

    def atom(self, val):
        token, = val
        return Atom(token)


class ExpParser:
    # Parser de Lark

    def __init__(self):
        self.parser = Lark(r"""
            ?defi: expr (" " expr)*

            ?expr: struct
                | atom 
                | var

            atom: ATOM
            var: VAR

            ATOM: /[a-z][A-Za-z0-9_]*/
            VAR: /[A-Z][A-Za-z0-9_]*/

            struct: ATOM "(" [expr (", " expr)*] ")"

            """, start='defi')

    def parse(self, string):
        return self.parser.parse(string)

    def transform(self, tree):
        return ExpTransformer().transform(tree)

    def inter(self, string):
        return self.transform(self.parse(string))
