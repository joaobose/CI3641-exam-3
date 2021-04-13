from .clase import Clase


class VirtualMethodsSystem:
    def __init__(self):
        # Diccionario con las definiciones del sistema
        self.definitions = {}

    def define(self, expression):
        """Define un tipo dada una expression en str"""

        # Parseamos la expresion
        name, super_name, methods = self.parse(expression)

        # Validamos que sea correcta la definicion
        self.validate(name, super_name, methods)

        # Creando nueva clase
        super_clase = None
        if super_name is not None:
            super_clase = self.definitions[super_name]

        clase = Clase(name, methods, super_clase)

        # Almacenando la nueva clase
        self.definitions[name] = clase

    def describe(self, name):
        """Retorna la descripcion de un tipo"""

        # Validando que el nombre exista
        if name not in self.definitions:
            raise Exception(f"El nombre '{name}' no se encuentra definido.")

        return self.definitions[name].methods_table_str

    def validate(self, name, super_name, methods):
        """Valida que una definicion sea correcta"""

        # Validando que el nombre no exista
        if name in self.definitions:
            raise Exception(f"El nombre '{name}' ya se encuentra definido.")

        # Validando que la super clase exista
        if super_name is not None and super_name not in self.definitions:
            raise Exception(f"La clase '{super_name}' no esta definida")

        # Validando si hay metodos repetidos
        if len(set(methods)) < len(methods):
            raise Exception(
                f"No pueden existir metodos repetidos en la definicion")

        # Validando que no existan ciclos de herencia
        # ...
        # ...
        # Listo XD, no es posible formar ciclos pues no se permite herencia
        # Con super clases que no esten definidad

    def parse(self, expression):
        """Parsea los elementos de una expression de definicion de tipo"""

        # Obtenemos los tokens de la expresion
        tokens = expression.split(' ')[::-1]

        # el nombre de la clase es el primer token
        name = tokens.pop()
        super_name = None

        # Si el siguente token es : entonces proximo token es
        # el nombre de la super clase
        if tokens[-1] == ':':
            tokens.pop()
            super_name = tokens.pop()

        # El resto de los tokens son la lista de los
        # nombres de los metodos
        methods = tokens[::-1]

        return name, super_name, methods
