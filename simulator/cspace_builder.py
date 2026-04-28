import random
import math
from robot_kinematics import mover_robot, obtener_esquinas_robot
from collision_checker import hay_colision

def ruta_libre(nodo):
    """Verifica paso a paso si la trayectoria generada choca."""
    for x, y, theta in zip(nodo.path_x, nodo.path_y, nodo.path_theta):
        esquinas = obtener_esquinas_robot(x, y, theta)
        if hay_colision(esquinas):
            return False
    return True

def generar_grafo_rrt(raiz, nodos_objetivo=1000):
    arbol = [raiz]
    nodos_validos = 1
    
    print(f"Generando {nodos_objetivo} nodos (Exploración RRT Avanzada)...")
    
    while nodos_validos < nodos_objetivo:
        # 1. Tirar un "dardo" aleatorio en el mapa 2x2 para jalar el árbol hacia allá
        rx = random.uniform(0.0, 2.0)
        ry = random.uniform(0.0, 2.0)
        
        # 2. Buscar el nodo del árbol que ya esté más cerca de ese dardo
        nodo_base = min(arbol, key=lambda n: math.hypot(n.x - rx, n.y - ry))
        
        mejor_nodo = None
        mejor_dist = float('inf')
        
        # 3. Probar 5 movimientos y quedarnos con el que más se acerque al dardo
        for _ in range(5):
            # Hack de la cinemática: Forzarlo a ir HASTA ADELANTE
            v = random.uniform(0.1, 0.6)      # m/s hacia adelante (evitar reversa)
            w = random.uniform(-2.5, 2.5)     # rad/s giro (izq/der)
            t = random.uniform(0.3, 0.8)      # pasos medianos
            
            # Convertir V y W deseada a velocidades de llanta wl y wr
            wl = (v - w * 0.15 / 2) / 0.027
            wr = (v + w * 0.15 / 2) / 0.027
            
            nuevo_nodo = mover_robot(nodo_base, wl, wr, t)
            
            if ruta_libre(nuevo_nodo):
                dist = math.hypot(nuevo_nodo.x - rx, nuevo_nodo.y - ry)
                if dist < mejor_dist:
                    mejor_dist = dist
                    mejor_nodo = nuevo_nodo
                    
        # Si un movimiento logró acercarse sin chocar, lo guardamos
        if mejor_nodo:
            arbol.append(mejor_nodo)
            nodos_validos += 1
            if nodos_validos % 200 == 0:
                print(f"Nodos expandidos: {nodos_validos}/{nodos_objetivo}...")
                
    return arbol