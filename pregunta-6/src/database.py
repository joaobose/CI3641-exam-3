from .libparse import ExpParser
from .datamodel import Atom, Variable, Rule, Struct, merge_scopes, project_scope_to_namespace


class InterpreterDatabase:
    def __init__(self):
        # Lista de reglas de la base de datos
        # Esto incluye hechos. Un hecho f(x) es representado
        # por la regla f(x) :- True
        self.rules = []
        self.parser = ExpParser()

    def define(self, raw):
        """Define un hecho o regla en la base datos del interprete"""

        # Parseando y validando
        expresion = self.parser.inter(raw)
        self.validate(expresion)

        def_label = 'regla'

        if expresion.kind is not Rule:
            def_label = 'hecho'
            expresion = Rule(expresion, [True])

        self.rules.append(expresion)

        return def_label, expresion

    def parse_ask(self, raw):
        """Parsea la expresion que se utilizara para realizar un query"""

        # Parseando y validando
        expresion = self.parser.inter(raw)
        self.validate(expresion)

        if expresion.kind is Rule:
            raise Exception(
                f'No se puede consultar una regla.')

        return expresion

    def validate(self, expresion):
        """Valida expresiones introducidas a la base de datos"""

        if expresion.kind is Variable:
            raise Exception(
                f'No se pueden expresar variables fuera de alguna estructura')

        if expresion.kind is not Rule:
            return

        if expresion.consecuente.kind is Variable or \
            not expresion.is_fact and any(
                [ant.kind is Variable for ant in expresion.antecedentes]):
            raise Exception(
                f'No se pueden expresar variables fuera de alguna estructura')

    @property
    def facts(self):
        # Sub conjunto de la reglas que sin hechos
        return [rule for rule in self.rules if rule.is_fact]

    def query(self, query):
        """Realiza una consulta a la base datos"""

        # Este metodo es un generator (iterador) de python
        # Cada elemento de la secuencia generada es un solucion al query
        # None se interpreta como solucion no satifacible

        query = query.copy()

        # Expandimos soluciones a partir del primer termino del query
        canditate = query.pop(0)

        # Verificamos si el candidato es un hecho
        is_fact = any(
            [canditate == fact.consecuente for fact in self.facts])

        # Si es un hecho, ese componente de la conjuncion ya es cierto.
        if is_fact:
            # Si candidate era el unico elemento de la conjuncion.
            if len(query) == 0:
                # ya toda la conjuncion es cierta
                yield set()
            else:
                # En caso contrario, consultamos al siguente elemento de la conjuncion
                for x in self.query(query):
                    if x is not None:
                        yield x
        else:
            # Exploramos posibilidades de unificacion
            for unificable in self.rules:

                # Si es unificable
                if canditate.is_unificable(unificable):
                    # Unificamos, obtenemos la nueva sub query
                    sub_scope, sub_query = canditate.unificate(
                        unificable)

                    # Reemplazamos el scope de unificacion en el resto de query
                    _query = [x.textual_sub(sub_scope) for x in query]

                    # Exploramos si la sub query es satisfacible (DFS)
                    for sub_query_result in self.query(sub_query):

                        # Si la sub query satisfacio a candidate.
                        if sub_query_result is not None:
                            # Reemplazamos el scope resultante en el resto de query
                            rest_query = [x.textual_sub(
                                sub_query_result) for x in _query]

                            # Agregamos el scope resultante al scope
                            rest_scope = project_scope_to_namespace(merge_scopes(
                                sub_scope, sub_query_result), canditate.namespace)

                            # Si el scope da contradiccion. Esta rama no tiene solucion.
                            if rest_scope is None:
                                continue

                            if len(rest_query) == 0:
                                # ya toda la conjuncion es cierta
                                yield rest_scope
                            else:
                                # En caso contrario, consultamos al siguente elemento de la conjuncion
                                for x in self.query(rest_query):
                                    if x is not None:
                                        yield merge_scopes(rest_scope, x)

        # Si por ninguno de los caminos pudimos satisfacer candidate
        # Entonces candidate es no satisfacible.
        # la conjuncion es false por corto circuito
        yield None
