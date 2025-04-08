import json
import pandas as pd
from first import calculate_first
from follow import calculate_follow

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


# Cargar la gramática
grammatic = load_grammatic("grammatic.json")
print("Gramática:")
show_grammatic(grammatic)

# Crear la tabla para FIRST y FOLLOW
first_follow_table = create_first_follow_table(grammatic)
non_terminals, terminals = get_terminals_and_non_terminals(grammatic)
print("\nNo terminales:", non_terminals)
print("Terminales:", terminals)

# Calcular FIRST
calculate_first(grammatic, terminals, first_follow_table)
print("\nTabla tras calcular FIRST:")
print(first_follow_table)

# Calcular FOLLOW
calculate_follow(grammatic, first_follow_table, non_terminals, terminals)
print("\nTabla final con FIRST y FOLLOW:")
print(first_follow_table)

# Mostrar la tabla final en formato tabular
# Se crea un DataFrame usando los datos de la tabla
df = pd.DataFrame.from_dict(first_follow_table, orient='index')
df.index.name = "No Terminal"
df.reset_index(inplace=True)
# Convertir los conjuntos en cadenas ordenadas para una mejor visualización
df['first'] = df['first'].apply(lambda s: ", ".join(sorted(s)))
df['follow'] = df['follow'].apply(lambda s: ", ".join(sorted(s)))
print("\nTabla final:")
print(df.to_string(index=False))
