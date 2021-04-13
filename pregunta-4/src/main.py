from .system import VirtualMethodsSystem

system = VirtualMethodsSystem()

while True:
    args = input("Introduzca su comando: ").split(" ", 1)

    command = args[0]

    if command == 'SALIR':
        break

    rest = args[1]

    try:
        if command == 'CLASS':
            system.define(rest)
            continue

        if command == 'DESCRIBIR':
            args = rest.split(" ", 1)
            name = args[0]
            desc = system.describe(name)
            print(desc)
            continue
    except Exception as error:
        print(error)
