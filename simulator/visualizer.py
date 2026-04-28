# simulator/visualizer.py
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from collision_checker import OBSTACULOS
from robot_kinematics import obtener_esquinas_robot

def extraer_ruta_para_lego(nodo_final):
    ruta = []
    nodo_actual = nodo_final
    while nodo_actual.parent is not None:
        ruta.append({'wl': nodo_actual.wl_aplicado, 'wr': nodo_actual.wr_aplicado, 't': nodo_actual.t_aplicado})
        nodo_actual = nodo_actual.parent
    ruta.reverse()
    return ruta

def visualizar_simulacion(arbol):
    # ==========================================
    # LÓGICA DEL MENÚ DE RUTAS
    # ==========================================
    # Ordenamos los nodos del que llegó más lejos al que llegó menos
    arbol_ordenado = sorted(arbol, key=lambda n: math.hypot(n.x - 1.8, n.y - 1.8))
    
    # Seleccionamos 3 rutas separadas (la mejor, la 10ma mejor, y la 20va mejor para dar variedad)
    meta_1 = arbol_ordenado[0]
    meta_2 = arbol_ordenado[10] if len(arbol_ordenado) > 10 else arbol_ordenado[1]
    meta_3 = arbol_ordenado[20] if len(arbol_ordenado) > 20 else arbol_ordenado[-1]
    
    opciones = [meta_1, meta_2, meta_3]

    print("\n" + "="*45)
    print("🚗 MENÚ DE PLANIFICACIÓN DE TRAYECTORIAS 🚗")
    print("="*45)
    print("1. Ruta Óptima Principal (La más directa a la meta)")
    print("2. Ruta Alternativa A (Variación media)")
    print("3. Ruta Alternativa B (Variación corta)")
    print("="*45)
    
    seleccion = ""
    while seleccion not in ['1', '2', '3']:
        seleccion = input("Elige el número de la ruta que deseas simular (1, 2 o 3): ")
        
    mejor_meta = opciones[int(seleccion) - 1]
    print(f"\n=> Preparando animación para la Ruta {seleccion}...")

    # ==========================================
    # CONFIGURACIÓN DEL GRÁFICO
    # ==========================================
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 2.0)
    ax.set_ylim(0, 2.0)
    ax.set_title(f"Simulación Animada: Ruta {seleccion}", fontsize=14)
    
    for (xmin, xmax, ymin, ymax) in OBSTACULOS:
        rect = patches.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, color='black')
        ax.add_patch(rect)
        
    for nodo in arbol:
        if nodo.parent:
            ax.plot(nodo.path_x, nodo.path_y, color='lightblue', alpha=0.3, linewidth=0.5)

    nodos_ruta = []
    actual = mejor_meta
    while actual.parent is not None:
        nodos_ruta.append(actual)
        actual = actual.parent
    nodos_ruta.reverse()

    ruta_x, ruta_y, ruta_theta = [], [], []
    for n in nodos_ruta:
        ruta_x.extend(n.path_x)
        ruta_y.extend(n.path_y)
        ruta_theta.extend(n.path_theta)

    ax.plot(ruta_x, ruta_y, color='red', linewidth=2, label=f"Ruta Elegida ({seleccion})")
    
    esq_iniciales = obtener_esquinas_robot(ruta_x[0], ruta_y[0], ruta_theta[0])
    robot_poly = patches.Polygon(esq_iniciales, closed=True, edgecolor='green', facecolor='lightgreen', linewidth=2, zorder=5)
    ax.add_patch(robot_poly)
    ax.legend()
    plt.grid(True)

    # ==========================================
    # LÓGICA DE ANIMACIÓN DETALLADA (LENTA)
    # ==========================================
    def update(frame):
        # Ahora procesa cada frame uno por uno (sin saltarse pasos)
        x = ruta_x[frame]
        y = ruta_y[frame]
        theta = ruta_theta[frame]
        nuevas_esquinas = obtener_esquinas_robot(x, y, theta)
        robot_poly.set_xy(nuevas_esquinas)
        return robot_poly,

    # Interval=60 hace que tarde 60ms entre cada frame, haciéndolo más lento y detallado
    ani = animation.FuncAnimation(fig, update, frames=len(ruta_x), interval=60, blit=True)
    
    try:
        ani.save(f'../media/simulator_demo_ruta{seleccion}.gif', writer='pillow', fps=30)
    except Exception as e:
        pass

    plt.show()

    instrucciones = extraer_ruta_para_lego(mejor_meta)
    print(f"\n--- INSTRUCCIONES PARA EL LEGO (Ruta {seleccion}) ---")
    for j, mov in enumerate(instrucciones):
        deg_izq = mov['wl'] * (180 / math.pi)
        deg_der = mov['wr'] * (180 / math.pi)
        print(f"Bloque {j+1}: Motor Izq={deg_izq:.0f}°, Motor Der={deg_der:.0f}°, Tiempo={mov['t']:.2f}s")