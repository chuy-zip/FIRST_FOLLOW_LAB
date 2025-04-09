def first_of_string(symbols, first_follow_table, terminals):

    result = set()
    # Si la secuencia está vacía, se retorna {ε}
    if not symbols:
        result.add("ε")
        return result

    # Se procesa cada símbolo de la secuencia
    for symbol in symbols:
        if symbol in terminals:
            # Si es terminal, se agrega directamente y se detiene el proceso
            result.add(symbol)
            return result
        else:
            # Si es un no terminal, se agregan los símbolos de su FIRST exceptuando ε
            first_set = first_follow_table[symbol]["first"]
            result.update(first_set - {"ε"})
            # Si no se puede derivar ε, se detiene aquí
            if "ε" not in first_set:
                return result
    # Si todos los símbolos podían derivar ε, se agrega ε al resultado
    result.add("ε")
    return result

def calculate_follow(grammar, first_follow_table, non_terminals, terminals):

    # Se asume que el primer no terminal de la gramática es el símbolo inicial.
    start_symbol = list(grammar.keys())[0]
    print(f"\nCalculando Follow de {start_symbol}")
    first_follow_table[start_symbol]["follow"].add("$")
    print(f"Caso 1: FOLLOW( {start_symbol} ) = { {'$'} }")

    changed = True
    while changed:
        changed = False
        # Iterar sobre cada producción de la gramática
        for A in grammar:
            for production in grammar[A]:
                symbols = production.split()
                for i, B in enumerate(symbols):
                    if B in non_terminals:
                        # Se define beta como la secuencia de símbolos que sigue a B en la producción
                        print(f"\nCalculando Follow de {B}")
                        beta = symbols[i+1:]
                        first_beta = first_of_string(beta, first_follow_table, terminals)

                        # Caso ii): Agregar FIRST(beta) - {ε} a FOLLOW(B)
                        before = len(first_follow_table[B]["follow"])
                        follow = first_beta - {"ε"}
                        first_follow_table[B]["follow"].update(follow)
                        print(f"Caso 2: FOLLOW({B}) = {first_follow_table[B]["follow"]}")
                        if len(first_follow_table[B]["follow"]) > before:
                            changed = True

                        # Caso iii): Si beta es vacío o FIRST(beta) contiene ε, se agrega FOLLOW(A) a FOLLOW(B)
                        if not beta or "ε" in first_beta:
                            before = len(first_follow_table[B]["follow"])
                            follow = first_follow_table[A]["follow"]
                            first_follow_table[B]["follow"].update(follow)
                            print(f"Caso 3: FOLLOW({B}) = {first_follow_table[B]["follow"]}")
                            if len(first_follow_table[B]["follow"]) > before:
                                changed = True
    return first_follow_table
