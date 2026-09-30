import re

# ==========================================
# Diseño del Nodo
# ==========================================
class Nodo:
    def __init__(self, palabra):
        self.palabra = palabra
        self.izquierda = None
        self.derecha = None
        # Manejo de duplicados mediante contador
        self.frecuencia = 1 

# ==========================================
# Implementación del Árbol Binario de Búsqueda
# ==========================================
class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    # Inserción de palabras
    def insertar(self, palabra):
        if self.raiz is None:
            self.raiz = Nodo(palabra)
        else:
            self._insertar_recursivo(self.raiz, palabra)

    def _insertar_recursivo(self, nodo, palabra):
        if palabra < nodo.palabra: # Subárbol izquierdo (menor alfabéticamente)
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(palabra)
            else:
                self._insertar_recursivo(nodo.izquierda, palabra)
        elif palabra > nodo.palabra: # Subárbol derecho (mayor alfabéticamente)
            if nodo.derecha is None:
                nodo.derecha = Nodo(palabra)
            else:
                self._insertar_recursivo(nodo.derecha, palabra)
        else:
            # Incremento de frecuencia si la palabra ya existe
            nodo.frecuencia += 1

    # ==========================================
    # Visualización del Árbol en Consola
    # ==========================================
    def mostrar_arbol_consola(self, nodo=None, prefijo="", es_izq=True, es_raiz=True):
        """Muestra una representación gráfica ASCII del árbol en la terminal."""
        if nodo is None:
            if es_raiz:
                nodo = self.raiz
                if nodo is None:
                    print("  (Árbol vacío)")
                    return
            else:
                return

        # Primero procesamos el subárbol derecho (se imprime arriba)
        if nodo.derecha:
            nuevo_prefijo = prefijo + ("│   " if es_izq and not es_raiz else "    ")
            self.mostrar_arbol_consola(nodo.derecha, nuevo_prefijo, False, False)

        # Imprimimos el nodo actual
        simbolo = "──> " if es_raiz else ("└── " if es_izq else "┌── ")
        frecuencia_str = f" (x{nodo.frecuencia})" if nodo.frecuencia > 1 else ""
        print(f"{prefijo}{simbolo}{nodo.palabra}{frecuencia_str}")

        # Luego procesamos el subárbol izquierdo (se imprime abajo)
        if nodo.izquierda:
            nuevo_prefijo = prefijo + ("    " if es_izq or es_raiz else "│   ")
            self.mostrar_arbol_consola(nodo.izquierda, nuevo_prefijo, True, False)

    # ==========================================
    # Recorridos
    # ==========================================
    def inorden(self, nodo, resultado):
        if nodo:
            self.inorden(nodo.izquierda, resultado)
            resultado.append(nodo.palabra)
            self.inorden(nodo.derecha, resultado)

    def preorden(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.palabra)
            self.preorden(nodo.izquierda, resultado)
            self.preorden(nodo.derecha, resultado)

    def postorden(self, nodo, resultado):
        if nodo:
            self.postorden(nodo.izquierda, resultado)
            self.postorden(nodo.derecha, resultado)
            resultado.append(nodo.palabra)

    # ==========================================
    # Cálculos y Estadísticas
    # ==========================================
    def contar_nodos(self, nodo):
        if nodo is None:
            return 0
        return 1 + self.contar_nodos(nodo.izquierda) + self.contar_nodos(nodo.derecha)

    def contar_nodos_internos(self, nodo):
        if nodo is None or (nodo.izquierda is None and nodo.derecha is None):
            return 0
        return 1 + self.contar_nodos_internos(nodo.izquierda) + self.contar_nodos_internos(nodo.derecha)

    def maximo_alfabetico(self):
        if self.raiz is None:
            return None
        actual = self.raiz
        while actual.derecha:
            actual = actual.derecha
        return actual.palabra

    def obtener_hojas(self, nodo, resultado):
        if nodo:
            if nodo.izquierda is None and nodo.derecha is None:
                resultado.append(nodo.palabra)
            self.obtener_hojas(nodo.izquierda, resultado)
            self.obtener_hojas(nodo.derecha, resultado)

    def obtener_internos(self, nodo, resultado):
        if nodo:
            if nodo.izquierda is not None or nodo.derecha is not None:
                resultado.append(nodo.palabra)
            self.obtener_internos(nodo.izquierda, resultado)
            self.obtener_internos(nodo.derecha, resultado)

# ==========================================
# Función Principal
# ==========================================
def limpiar_texto(texto):
    texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
    return texto_limpio.split()

def main():
    oracion = input("Introduce una oración para construir el árbol: ")
    palabras = limpiar_texto(oracion)

    if not palabras:
        print("La oración no contiene palabras válidas.")
        return

    arbol = ArbolBinarioBusqueda()
    for palabra in palabras:
        arbol.insertar(palabra)

    print("\n==========================================")
    print(" ESTROCTURA GRÁFICA DEL ÁRBOL EN CONSOLA")
    print("==========================================")
    arbol.mostrar_arbol_consola()
    print("==========================================\n")

    # Recorridos
    res_inorden, res_preorden, res_postorden = [], [], []
    arbol.inorden(arbol.raiz, res_inorden)
    arbol.preorden(arbol.raiz, res_preorden)
    arbol.postorden(arbol.raiz, res_postorden)
    
    print("--- Recorridos ---")
    print(f"1. Inorden (Alfabético): {res_inorden}")
    print(f"2. Preorden: {res_preorden}")
    print(f"3. Postorden: {res_postorden}")

    print("\n--- Métricas del Árbol ---")
    print(f"4. Número total de nodos (palabras únicas): {arbol.contar_nodos(arbol.raiz)}")
    print(f"5. Número de nodos internos: {arbol.contar_nodos_internos(arbol.raiz)}")
    print(f"6. Palabra con el máximo valor alfabético: {arbol.maximo_alfabetico()}")

    hojas, internos = [], []
    arbol.obtener_hojas(arbol.raiz, hojas)
    arbol.obtener_internos(arbol.raiz, internos)
    
    print(f"7. Información en las hojas: {hojas}")
    print(f"8. Información en los nodos internos: {internos}")

if __name__ == "__main__":
    main()