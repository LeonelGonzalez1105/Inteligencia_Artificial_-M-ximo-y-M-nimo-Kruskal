import networkx as nx
import matplotlib.pyplot as plt

# --- ESTRUCTURA DE DATOS: UNION-FIND ---
# Esta clase es el "cerebro" que detecta si se forma un ciclo
class UnionFind:
    def __init__(self, nodos):
        self.parent = {nodo: nodo for nodo in nodos}
    
    def find(self, item):
        if self.parent[item] == item:
            return item
        return self.find(self.parent[item])
    
    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            self.parent[root1] = root2
            return True # Unión exitosa (no había ciclo)
        return False # Falló la unión (se formaría un ciclo)

# --- ALGORITMO DE KRUSKAL ---
def kruskal_logic(grafo_dict, modo_maximo=False):
    # 1. Obtener todas las aristas y sus pesos
    aristas = []
    nodos = list(grafo_dict.keys())
    
    for u in grafo_dict:
        for v, peso in grafo_dict[u].items():
            # Ordenamos (u, v) para no duplicar aristas (A-B es lo mismo que B-A)
            if u < v: 
                aristas.append((u, v, peso))
    
    # 2. ORDENAR ARISTAS
    # El truco: Si es Mínimo, de menor a mayor. Si es Máximo, al revés.
    aristas.sort(key=lambda x: x[2], reverse=modo_maximo)
    
    uf = UnionFind(nodos)
    mst_aristas = []
    costo_total = 0
    
    tipo = "MÁXIMO" if modo_maximo else "MÍNIMO"
    print(f"\n--- 🕵️ INICIANDO KRUSKAL (Modo: {tipo} Coste) ---")
    print(f"{'Arista':<15} | {'Peso':<5} | {'Acción'}")
    print("-" * 40)
    
    # 3. PROCESO DE SELECCIÓN
    for u, v, peso in aristas:
        # Intentamos unir los conjuntos
        if uf.union(u, v):
            print(f"{u}-{v:<11} | {peso:<5} | Agregada (Conecta componentes)")
            mst_aristas.append((u, v))
            costo_total += peso
        else:
            print(f"{u}-{v:<11} | {peso:<5} | Descartada (Formaría ciclo)")
            
    return mst_aristas, costo_total

# --- GRAFICACIÓN ---
def graficar_resultado(grafo_dict, aristas_res, costo, modo_maximo):
    G = nx.Graph()
    for u, vecinos in grafo_dict.items():
        for v, peso in vecinos.items():
            G.add_edge(u, v, weight=peso)
            
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    
    # Fondo (Todo el grafo disponible)
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='#E0E0E0')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.2, edge_color='black')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    
    # Solución
    color_linea = '#FF5733' if modo_maximo else '#2ECC71' # Rojo para Máx, Verde para Mín
    titulo_tipo = "MÁXIMO" if modo_maximo else "MÍNIMO"
    
    nx.draw_networkx_nodes(G, pos, nodelist=[n for edge in aristas_res for n in edge], node_size=1000, node_color=color_linea, alpha=0.6)
    nx.draw_networkx_edges(G, pos, edgelist=aristas_res, width=4, edge_color=color_linea)
    
    # Etiquetas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(f"Árbol de {titulo_tipo} Coste (Kruskal)\nSuma Total de Pesos: {costo}", fontsize=14)
    plt.axis('off')
    
    nombre_archivo = f"kruskal_{titulo_tipo.lower()}.png"
    plt.savefig(nombre_archivo)
    print(f"\nGráfica guardada como '{nombre_archivo}'")
    plt.show()

# --- DATOS: SISTEMA DE TUBERÍAS (Ejemplo) ---
# Pesos = Capacidad de flujo (para Máximo) o Costo de tubo (para Mínimo)
red_distribucion = {
    'Planta': {'Nodo_A': 10, 'Nodo_B': 6, 'Nodo_C': 5},
    'Nodo_A': {'Planta': 10, 'Nodo_D': 15, 'Nodo_B': 4},
    'Nodo_B': {'Planta': 6, 'Nodo_A': 4, 'Nodo_D': 12, 'Nodo_E': 8, 'Nodo_C': 7},
    'Nodo_C': {'Planta': 5, 'Nodo_B': 7, 'Nodo_E': 20},
    'Nodo_D': {'Nodo_A': 15, 'Nodo_B': 12, 'Nodo_F': 9},
    'Nodo_E': {'Nodo_B': 8, 'Nodo_C': 20, 'Nodo_F': 3},
    'Nodo_F': {'Nodo_D': 9, 'Nodo_E': 3}
}

# --- MENÚ PRINCIPAL ---
if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        print("   SIMULADOR KRUSKAL (Min & Max)")
        print("="*40)
        print("1. Calcular Árbol de MÍNIMO Coste (Ahorrar)")
        print("2. Calcular Árbol de MÁXIMO Coste (Priorizar)")
        print("3. Salir")
        
        opcion = input("\nElige una opción (1/2/3): ")
        
        if opcion == '3':
            print("¡Clase terminada!")
            break
            
        elif opcion in ['1', '2']:
            es_maximo = (opcion == '2')
            
            # Ejecutar lógica
            resultado, costo = kruskal_logic(red_distribucion, es_maximo)
            
            print(f"\nPROCESO TERMINADO. Costo Total: {costo}")
            print("Abriendo gráfica visual...")
            
            # Graficar
            graficar_resultado(red_distribucion, resultado, costo, es_maximo)
            print(" Cierra la ventana de la gráfica para volver al menú.")
            
        else:
            print(" Opción no válida, intenta de nuevo.")