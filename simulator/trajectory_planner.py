# simulator/trajectory_planner.py
import matplotlib.pyplot as plt
from robot_kinematics import Nodo, mover_robot
from cspace_builder import generar_grafo_rrt
from visualizer import visualizar_simulacion

def probar_movimientos_basicos():
    """Genera la gráfica de los 4 movimientos requeridos."""
    fig, axs = plt.subplots(2, 2, figsize=(8, 8))
    fig.suptitle('Simulación de Movimientos Básicos', fontsize=14)
    
    movimientos = [
        ("Línea Recta", 5.0, 5.0, 1.0, axs[0,0]),
        ("Giro Derecha", 5.0, 0.0, 1.5, axs[0,1]),
        ("Giro Izquierda", 0.0, 5.0, 1.5, axs[1,0]),
        ("Combinado", None, None, None, axs[1,1])
    ]
    
    for titulo, wl, wr, t, ax in movimientos:
        ax.set_title(titulo)
        ax.set_xlim(0, 1.0)
        ax.set_ylim(0, 1.0)
        ax.grid(True)
        inicio = Nodo(0.2, 0.2, 0.0)
        ax.plot(0.2, 0.2, 'ro')
        
        if titulo == "Combinado":
            n1 = mover_robot(inicio, 5.0, 5.0, 0.5)
            n2 = mover_robot(n1, 0.0, 5.0, 0.8)
            n3 = mover_robot(n2, 5.0, 5.0, 0.5)
            for n in [n1, n2, n3]:
                ax.plot(n.path_x, n.path_y, 'b-')
        else:
            n_final = mover_robot(inicio, wl, wr, t)
            ax.plot(n_final.path_x, n_final.path_y, 'b-')
            
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("1. Probando movimientos básicos...")
    probar_movimientos_basicos()
    
    print("\n2. Construyendo C-Space y planificando trayectorias...")
    raiz = Nodo(0.2, 0.2, 0.0)
    arbol = generar_grafo_rrt(raiz, 1000)
    visualizar_simulacion(arbol)