class Clase:
    def __init__(self, name, raw_methods, super_class):
        self.name = name
        self.super_class = super_class

        # Tabla de metodos virtuales
        self.methods = {}

        # La tabla de metodos virtuales inicial
        # es una copia de los metodos de la super clase
        # (de existir super clase)
        if super_class != None:
            self.methods = super_class.methods.copy()

        # Agregamos/sobreescribimos las definiciones de metodos de la clase
        for method in raw_methods:
            self.methods[method] = name

    @property
    def methods_table_str(self):
        """Representacion de la tabla de metodos virtuales de la clase"""

        return '\n'.join(
            [f'{m} -> {self.methods[m]} :: {m}' for m in self.methods.keys()])

    def __str__(self):
        """Representacion str de la clase"""

        return f'Class {self.name}\n{self.methods_table_str}\n'
