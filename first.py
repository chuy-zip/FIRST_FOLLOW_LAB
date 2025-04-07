def is_terminal(symbol, terminals):
    return symbol in terminals

def first(symbol, grammar, terminals, first_sets, visited=None):
    if visited is None:
        visited = set()
    
    print(f"\nCalculando FIRST( {symbol} )...")
    print(f"Visitados: {visited}")

    # Caso base 1: Símbolo terminal
    if is_terminal(symbol, terminals):
        print(f"{symbol} es terminal entonces, FIRST( {symbol} ) = {{{symbol}}}")
        return {symbol}
    
    # Caso base 2: Épsilon
    if symbol == 'ε':
        print(f"ε encontrado → FIRST(ε) = {{ε}}")
        return {'ε'}
    
    # Evitar recursión infinita
    if symbol in visited:
        return set()
    visited.add(symbol)
    
    result = set()

    print(f"Producciones de {symbol}: {grammar.get(symbol, [])}")
    # Para cada producción del no terminal
    for production in grammar.get(symbol, []):
        symbols_in_prod = production.split()

        print(f"\nProcesando producción: {production}")
        print(f"Símbolos en producción: {symbols_in_prod}")
        
        # Caso: X -> ε 
        if not symbols_in_prod:
            result.add('ε')
            continue
            
        # Para cada símbolo en la producción X -> Y1, Y2...Yn
        for i, current_symbol in enumerate(symbols_in_prod):
            current_first = first(current_symbol, grammar, terminals, first_sets, visited.copy())
            print(f"FIRST( {current_symbol} ) = {current_first}")

            # Agregar todos los símbolos excepto ε, en este caso ya solo agregamos ε si llegamos al final
            # y vemos que el no terminal puede generar ε para todas sus producciones 
            result.update(current_first - {'ε'})
            
            # Si ε no está en current_first, no continuar ya que significa que hemos encontrado un terminal 
            # no es necesario seguir iterando en en los simbolos de la produccion. 
            if 'ε' not in current_first:
                print(f"ε ∉ FIRST( {current_symbol} ) → Terminando esta producción")
                break
                
            # Si llegamos al final y todos tienen ε, agregar ε
            if i == len(symbols_in_prod) - 1:
                print("Todos los símbolos pueden ser ε → Agregando ε al resultado")
                result.add('ε')
    
    print(f"\nFIRST( {symbol} ) final: {result}")
    return result

def calculate_first(grammar, terminals, first_follow_table):
    first_sets = {nt: set() for nt in grammar}
    
    for non_terminal in grammar:
        print(f"\nCALCULANDO EL FIRST DEL NO TERMINAL {non_terminal}")
        new_first = first(non_terminal, grammar, terminals, first_sets)
        first_sets[non_terminal].update(new_first)
        
        first_follow_table[non_terminal]["first"] = new_first
