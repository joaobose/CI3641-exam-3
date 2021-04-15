
def return_copy(f):
    # Decorador para retonar un deep copy del objeto retonado por f
    # Este docorador supone que f retona un objeto de tipo Exp

    def k(*args):
        return f(*args).copy()
    return k


def copy_scope(scope):
    """Realiza la copia de un scope"""
    return set([eq.copy() for eq in scope])


def scan_scope_for_merge(scope, other_scope):
    """Escanea un scope sobre otro como paso previo al merge"""
    to_unificate = []

    for eq in scope:
        for other_eq in other_scope:
            # Si hay definiciones con posibble conflicto ie: X = fun(a, Y) y X = fun(K, b)
            if other_eq.var == eq.var and other_eq != eq:
                # Si el el conflicto es solucionable
                if other_eq.value.is_unificable(eq.value):
                    # Agregar el par al conjunto de unificaciones necesarias
                    to_unificate.append(
                        (other_eq.var.copy(), other_eq.value, eq.value))
                else:
                    # Contradiccion
                    return False, None
            else:
                other_eq.value = other_eq.value.textual_sub({eq})

    other_scope.update(copy_scope(scope))

    return True, to_unificate


def project_scope_to_namespace(scope, namespace):
    """Proyecta un scope al namespace de una expresion"""
    if scope is None:
        return None
    return set([x for x in scope if str(x.var.token) in namespace])


def remove_transitive_bindings(scope):
    """Elimina bindings transitivos redundantes dentro de un scope"""

    # ie: {X = b, Y = b, X = Y, Y = X}
    # retorna {X = b, Y = b}

    to_remove = set()

    for eq in scope:
        for other_eq in scope:
            if eq != other_eq and eq.var == other_eq.value and other_eq.var == eq.value \
                    and (any([x.var == eq.var and x.value is not Variable for x in scope])
                         or any([x.var == other_eq.var and x.value is not Variable for x in scope])
                         ):
                to_remove.add(eq)
                to_remove.add(other_eq)

    return scope - to_remove


def remove_reflexive_bindings(scope):
    """Elimina bindings reflexivos de un scope"""

    # ie: {X = X, X = a, Y = Y}
    # retona {X = a}

    return set([eq for eq in scope if eq.var != eq.value])


def merge_scopes(scope_one, scope_two):
    """Realiza merge de dos scopes"""

    # ie: {X = fun(a, Z), D = n, P = O} merge con {X = fun(K, b), O = v}
    # retorna {X = fun(a, b), D = n, P = v, O = v, K = a, Z = b}

    result = copy_scope(scope_two)

    # Scan the first scope
    success, to_unificate_one = scan_scope_for_merge(scope_one, result)
    if not success:
        return None

    # Perform needed unifications
    for var, left, right in to_unificate_one:
        sub_scope, unified = left.unificate(right)
        if sub_scope is None:
            return None

        result = set([eq for eq in result if eq.var != var])
        result.add(UEQT(var, unified[0]))
        result.update(sub_scope)

    # Scan the second scope
    success, to_unificate_two = scan_scope_for_merge(scope_two, result)
    if not success:
        return None

    # Perform needed unifications
    for var, left, right in to_unificate_two:
        sub_scope, unified = left.unificate(right)
        if sub_scope is None:
            return None

        result = set([eq for eq in result if eq.var != var])
        result.add(UEQT(var, unified[0]))
        result.update(sub_scope)

    result = remove_reflexive_bindings(result)
    return remove_transitive_bindings(result)


class UEQT:
    # Unification equation term
    # Representa la ecuacion de terminos var = value
    # Esto es utilizado para representar el scope de unificacion

    def __init__(self, var, value):
        self.var = var
        self.value = value

    # Representacion string
    def __str__(self):
        return f'{str(self.var)} = {str(self.value)}'

    # Hash - para trabajar con el tipo set
    def __hash__(self):
        return hash(str(self))

    # Represenation un UEQT
    def __repr__(self):
        return str(self)

    # Igualdad de ecuaciones
    def __eq__(self, other):
        return str(self) == str(other)

    # Metodo para hacer deep copy de un UEQT
    def copy(self):
        return UEQT(self.var.copy(), self.value.copy())


class Exp(object):
    # Clase expresion base

    # Tipo de la expresion
    @property
    def kind(self):
        return self.__class__

    # Representacion
    def __repr__(self):
        return str(self)

    # predicado es unificable? asimetrico
    def l_is_unificable(self, other):
        return False

    # predicado es unificable? simetrico
    def is_unificable(self, other):
        return self.l_is_unificable(other) or other.l_is_unificable(self)

    # unificacion asimetrica
    def l_unificate(self, other):
        return None, None

    # unificacion simetrica
    def unificate(self, other):
        if self.l_is_unificable(other):
            return self.l_unificate(other)
        else:
            return other.l_unificate(self)


class Rule(Exp):
    # Clase que representa expresiones de la forma:
    # consecuente :- antecedentes
    # donde antecedentes es una lista de expresiones
    # tal que ninguna es de tipo Rule

    def __init__(self, consecuente, antecedentes):
        self.consecuente = consecuente
        self.antecedentes = antecedentes

    # Igualdad entre expresiones
    def __eq__(self, other):
        return other.kind is Rule and self.consecuente == other.consecuente \
            and len(other.antecedentes) == len(self.antecedentes) \
            and all([self.antecedentes[i] == other.antecedentes[i] for i in range(len(self.antecedentes))])

    # predicado es unificable? asimetrico
    def l_is_unificable(self, other):
        return self.consecuente.is_unificable(other)

    # predicado es unificable? simetrico
    # para reglas forzamos la anti simetria para evitar bugs
    def is_unificable(self, other):
        return self.l_is_unificable(self)

    # Metodo para hacer deep copy de un Rule
    def copy(self):
        return Rule(self.consecuente.copy(), [ant.copy() for ant in self.antecedentes if isinstance(ant, Exp)])

    # Sustitucion textual a partir de un scope
    def textual_sub(self, scope):
        copy = self.copy()

        for eq in scope:
            if self.is_fact:
                copy = Rule(
                    copy.consecuente.textual_sub({eq}), [True])
            else:
                copy = Rule(
                    copy.consecuente.textual_sub({eq}), [ant.textual_sub({eq}) for ant in copy.antecedentes])

        return copy

    # Propiedad es hecho?
    @property
    def is_fact(self):
        return len(self.antecedentes) == 1 and self.antecedentes[0] is True

    # Representacion str
    def __str__(self):
        antecedentes_str = ' '.join([f'{str(a)}' for a in self.antecedentes])
        return f'{str(self.consecuente)} :- {antecedentes_str}'

    # Unificacion asimterica
    def l_unificate(self, other):
        unification_scope, consec = self.consecuente.unificate(other)

        if self.is_fact:
            return unification_scope, consec

        unification_scope, _ = self.consecuente.unificate(other)
        if unification_scope is None:
            return None, None

        ants = [ant.textual_sub(unification_scope)
                for ant in self.antecedentes]

        return unification_scope, ants

    # Namespace - Variables que ocurren en la expresion
    @property
    def namespace(self):
        names = set()

        names.update(self.consecuente.namespace)

        if not self.is_fact:
            for ant in self.antecedentes:
                names.update(ant.namespace)

        return names


class Struct(Exp):
    # Clase que representa expresiones de la forma:
    # atomo(argumentos)
    # donde argumentos es una lista de expresiones
    # tal que ninguna es de tipo Rule

    def __init__(self, name, args):
        self.name = name
        self.args = args

    # Igualdad entre expresiones
    def __eq__(self, other):
        return other.kind is Struct and self.name == other.name and len(other.args) == len(self.args) \
            and all([self.args[i] == other.args[i] for i in range(len(self.args))])

    # predicado es unificable? asimetrico
    def l_is_unificable(self, other):
        return other.kind is Struct and self.name == other.name and len(other.args) == len(self.args) \
            and all([self.args[i].is_unificable(other.args[i]) for i in range(len(self.args))])

    # Metodo para hacer deep copy de un Struct
    def copy(self):
        return Struct(self.name, [arg.copy() for arg in self.args])

    # Sustitucion textual a partir de un scope
    def textual_sub(self, scope):
        copy = self.copy()

        for eq in scope:
            copy = Struct(
                copy.name, [arg.textual_sub({eq}) for arg in copy.args])

        return copy

    # Representacion str
    def __str__(self):
        args_str = ', '.join([f'{str(arg)}' for arg in self.args])
        return f'{self.name}({args_str})'

    # Unificacion asimterica
    def l_unificate(self, other):
        unified_args = []
        unified_scope = set()

        for i in range(len(self.args)):
            arg_scope, unified_arg = self.args[i].unificate(
                other.args[i])

            unified_scope = merge_scopes(unified_scope, arg_scope)
            if unified_scope is None:
                return None, None

            unified_args.append(unified_arg[0])

        return unified_scope, [Struct(self.name, unified_args)]

    # Namespace - Variables que ocurren en la expresion
    @property
    def namespace(self):
        names = set()

        for arg in self.args:
            names.update(arg.namespace)

        return names


class Atom(Exp):
    # Clase que representa expresiones de la forma:
    # atomo

    def __init__(self, token):
        self.token = token

    # Igualdad entre expresiones
    def __eq__(self, other):
        return other.kind is Atom and str(self) == str(other)

    # predicado es unificable? asimetrico
    def l_is_unificable(self, other):
        return other.kind is Atom and self == other

    # Metodo para hacer deep copy de un Atom
    def copy(self):
        return self

    # Sustitucion textual a partir de un scope
    def textual_sub(self, scope):
        return self

    # La representacion es su token
    def __str__(self):
        return self.token

    # Unificacion asimterica
    def l_unificate(self, other):
        return set(), [self]

    # Namespace - Variables que ocurren en la expresion
    @property
    def namespace(self):
        return set()


class Variable(Exp):
    def __init__(self, token):
        self.token = token

    # Igualdad entre expresiones
    def __eq__(self, other):
        return other.kind is Variable and self.token == other.token

    # predicado es unificable? asimetrico
    def l_is_unificable(self, other):
        return True

    # Metodo para hacer deep copy de un Variable
    def copy(self):
        return Variable(self.token)

    # Sustitucion textual a partir de un scope
    @return_copy
    def textual_sub(self, scope):
        for eq in scope:
            if eq.var == self:
                return eq.value

        return self

    # La representacion es su token
    def __str__(self):
        return self.token

    def l_unificate(self, other):
        scope = {UEQT(self.copy(), other.copy())}

        if other.kind is Variable:
            scope.add(UEQT(other.copy(), self.copy()))

        return remove_reflexive_bindings(scope), [other.copy()]

    # Namespace - Variables que ocurren en la expresion
    @property
    def namespace(self):
        return {str(self.token)}
