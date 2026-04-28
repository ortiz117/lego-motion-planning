import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==========================================
# 1. PARÁMETROS DEL ROBOT Y MAPA
# ==========================================
# Medidas físicas del LEGO 
R_LLANTA = 0.0275  
L = 0.115          # Distancia entre llantas (eje)
ROBOT_LARGO = 0.135 # Largo total del rectángulo del carrito
ROBOT_ANCHO = 0.18 # Ancho total del rectángulo del carrito

# Mapa 2x2: Obstáculos (xmin, xmax, ymin, ymax)
OBSTACULOS = [
    (0.0, 1.0, 1.5, 2.0),
    (0.5, 1.0, 0.5, 1.0),
    (1.5, 1.65, 0.5, 1.5),
    (1.0, 2.0, 0.0, 0.1)
]

# ==========================================
# 2. MODELO CINEMÁTICO Y ESTRUCTURA DEL GRAFO
# ==========================================
class Nodo:
    def __init__(self, x, y, theta, wl=0, wr=0, t=0, parent=None):
        self.x = x
        self.y = y
        self.theta = theta
        self.parent = parent
        
        # Guardamos la configuración que nos llevó a este nodo (para el LEGO)
        self.wl_aplicado = wl
        self.wr_aplicado = wr
        self.t_aplicado = t
        
        self.path_x = []
        self.path_y = []
        self.path_theta = []

def mover_robot(nodo_actual, wl, wr, t, dt=0.1):
    x, y, theta = nodo_actual.x, nodo_actual.y, nodo_actual.theta
    path_x, path_y, path_theta = [x], [y], [theta]
    
    pasos = int(t / dt)
    for _ in range(pasos):
        v = (R_LLANTA * wr + R_LLANTA * wl) / 2.0
        w = (R_LLANTA * wr - R_LLANTA * wl) / L
        
        x += v * math.cos(theta) * dt
        y += v * math.sin(theta) * dt
        theta += w * dt
        
        path_x.append(x)
        path_y.append(y)
        path_theta.append(theta)
        
    nuevo_nodo = Nodo(x, y, theta, wl, wr, t, parent=nodo_actual)
    nuevo_nodo.path_x = path_x
    nuevo_nodo.path_y = path_y
    nuevo_nodo.path_theta = path_theta
    return nuevo_nodo

# ==========================================
# 3. DETECTOR DE COLISIONES (ROBOT COMO RECTÁNGULO)
# ==========================================
def obtener_esquinas_robot(x, y, theta):
    """Calcula las 4 esquinas del robot rotado en el plano."""
    esquinas = []
    # Desplazamientos desde el centro a las esquinas (largo/2, ancho/2)
    dx_dy = [
        (ROBOT_LARGO/2, ROBOT_ANCHO/2),
        (ROBOT_LARGO/2, -ROBOT_ANCHO/2),
        (-ROBOT_LARGO/2, -ROBOT_ANCHO/2),
        (-ROBOT_LARGO/2, ROBOT_ANCHO/2)
    ]
    
    for dx, dy in dx_dy:
        # Matriz de rotación 2D
        esquina_x = x + (dx * math.cos(theta) - dy * math.sin(theta))
        esquina_y = y + (dx * math.sin(theta) + dy * math.cos(theta))
        esquinas.append((esquina_x, esquina_y))
    return esquinas

def punto_en_obstaculo(px, py):
    if px < 0 or px > 2.0 or py < 0 or py > 2.0:
        return True
    for (xmin, xmax, ymin, ymax) in OBSTACULOS:
        if xmin <= px <= xmax and ymin <= py <= ymax:
            return True
    return False

def hay_colision(x, y, theta):
    esquinas = obtener_esquinas_robot(x, y, theta)
    # Verificamos si alguna esquina del rectángulo del robot toca un obstáculo
    for ex, ey in esquinas:
        if punto_en_obstaculo(ex, ey):
            return True
    return False

def ruta_libre(nodo):
    for x, y, theta in zip(nodo.path_x, nodo.path_y, nodo.path_theta):
        if hay_colision(x, y, theta):
            return False
    return True

# ==========================================
# 4. ALGORITMO TIPO RRT (Grafo de Conexiones)
# ==========================================
def generar_grafo_rrt(nodos_objetivo=1000):
    # Empezamos en (0.2, 0.2) para no chocar con la pared de inicio
    raiz = Nodo(0.2, 0.2, 0.0) 
    arbol = [raiz]
    nodos_validos = 1
    
    print(f"Generando {nodos_objetivo} nodos libres de colisión...")
    
    while nodos_validos < nodos_objetivo:
        nodo_base = random.choice(arbol)
        
        # 10 combinaciones aleatorias desde el nodo base
        for _ in range(10):
            if nodos_validos >= nodos_objetivo:
                break
                
            wl = random.uniform(-8, 8)
            wr = random.uniform(-8, 8)
            t = random.uniform(0.5, 1.2)
            
            nuevo_nodo = mover_robot(nodo_base, wl, wr, t)
            
            if ruta_libre(nuevo_nodo):
                arbol.append(nuevo_nodo)
                nodos_validos += 1
                
    return arbol

# ==========================================
# 5. VISUALIZACIÓN Y EXTRACCIÓN DE TRAYECTORIA
# ==========================================
def extraer_ruta_para_lego(nodo_final):
    """Extrae las instrucciones inversas desde la meta hasta el inicio."""
    ruta = []
    nodo_actual = nodo_final
    while nodo_actual.parent is not None:
        ruta.append({
            'wl': nodo_actual.wl_aplicado, 
            'wr': nodo_actual.wr_aplicado, 
            't': nodo_actual.t_aplicado
        })
        nodo_actual = nodo_actual.parent
    ruta.reverse()
    return ruta

def visualizar_simulacion(arbol):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 2.0)
    ax.set_ylim(0, 2.0)
    ax.set_title("Planificación de Movimientos (Grafo RRT)")
    
    # Dibujar obstáculos
    for (xmin, xmax, ymin, ymax) in OBSTACULOS:
        rect = patches.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, color='black')
        ax.add_patch(rect)
        
    # Dibujar todas las ramas (grafo)
    for nodo in arbol:
        if nodo.parent:
            ax.plot(nodo.path_x, nodo.path_y, color='lightblue', alpha=0.5, linewidth=0.5)

    # Seleccionar el nodo más lejano como nuestra "meta" para la trayectoria
    nodo_meta = max(arbol, key=lambda n: math.hypot(n.x - 0.2, n.y - 0.2))
    
    # Dibujar la ruta seleccionada para el LEGO
    nodo_actual = nodo_meta
    while nodo_actual.parent:
        ax.plot(nodo_actual.path_x, nodo_actual.path_y, color='red', linewidth=2)
        nodo_actual = nodo_actual.parent
        
    # Dibujar el rectángulo del robot en la posición final de la ruta
    esq = obtener_esquinas_robot(nodo_meta.x, nodo_meta.y, nodo_meta.theta)
    robot_poly = patches.Polygon(esq, closed=True, edgecolor='green', facecolor='none', linewidth=2)
    ax.add_patch(robot_poly)

    plt.grid(True)
    plt.show()
    
    # Imprimir instrucciones para los bloques de LEGO
    instrucciones = extraer_ruta_para_lego(nodo_meta)
    print("\n--- INSTRUCCIONES PARA EL LEGO ---")
    for i, mov in enumerate(instrucciones):
        print(f"Paso {i+1}: Motor Izq (wl)={mov['wl']:.2f} rad/s, Motor Der (wr)={mov['wr']:.2f} rad/s, Tiempo={mov['t']:.2f} s")

if __name__ == "__main__":
    arbol = generar_grafo_rrt(1000)
    visualizar_simulacion(arbol)