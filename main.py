import json
from first import calculate_first

def load_grammatic(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        grammatic = json.load(file)
    return grammatic

def get_terminals_and_non_terminals(grammar):
    non_terminals = set(grammar.keys())
    terminals = set()
    
    for productions in grammar.values():
        for production in productions:

            # dividir por los espacios vacios
            symbols = production.split()
            for symbol in symbols:
                # si no es un non_ter ni epsilon,es un terminal
                if symbol not in non_terminals and symbol != 'ε':
                    terminals.add(symbol)
    
    return non_terminals, terminals

def show_grammatic(grammatic):

    for non_terminal, productions in grammatic.items():

        total_prod = "" 
        for prod in productions:

            total_prod += prod + " | "
        
        total_prod = total_prod[:-2]
        
        print(f"{non_terminal} -> {total_prod}")

# creando una estructura para guardar el first y follow de cada no terminal despues
def create_first_follow_table(grammatic):

    table = {}
    
    for non_ter, value in grammatic.items():

        table[non_ter] = {'first': set(), 'follow': set()}

    return table

grammatic = load_grammatic("grammatic.json")
print(grammatic)

# la forma en la que formateamos la gramatica es la siguiente
# tenemos un diccionario de la forma: {"E'": ["+ T E'", 'ε'], ...}
# donde la llave es un no terminal del lado izquierdo de la producción, y la lista son sus producciones
# entonces "E'": ["+ T E'", 'ε'] se interpreta como E' -> + T E' | ε
# la razon por la que las expresiones estan separadas por espacios en blancos es para facilitar las operaciones
# con la gramatica
 
show_grammatic(grammatic)

first_follow_table = create_first_follow_table(grammatic)
print(first_follow_table)

non_terminals, terminals = get_terminals_and_non_terminals(grammatic)
print("No terminales:", non_terminals)
print("Terminales:", terminals)

calculate_first(grammatic, terminals, first_follow_table)
print("\n",first_follow_table)