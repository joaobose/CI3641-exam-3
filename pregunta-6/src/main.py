from .database import InterpreterDatabase

system = InterpreterDatabase()

while True:
    args = input('Introduzca su comando: ').split(" ", 1)

    command = args[0]

    if command == 'SALIR':
        break

    rest = args[1]

    try:
        if command == 'DEF':
            label, expresion = system.define(rest)
            if label == 'hecho':
                print(f'Se definió el {label} ’{rest}’')
                continue
            else:
                print(f'Se definió el {label} ’{str(expresion)}’')
                continue

        if command == 'ASK':
            query = system.parse_ask(rest)
            for sol in system.query([query]):
                if sol is None:
                    print('No es satisfacible')
                    break

                print(f'Satisfacible cuando ’{str(sol)}’. ¿Qué desea hacer?')
                opcion = input(f'[Consultando {rest}]: ')

                if opcion == 'RECHAZAR':
                    continue
                else:
                    print('Consulta aceptada ')
                    break

            continue
    except Exception as error:
        print(error)
