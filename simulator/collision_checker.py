# simulator/collision_checker.py

# Mapa 2x2: Obstáculos (xmin, xmax, ymin, ymax)
OBSTACULOS = [
    (0.0, 1.0, 1.5, 2.0),
    (0.5, 1.0, 0.5, 1.0),
    (1.5, 1.65, 0.5, 1.5),
    (1.0, 2.0, 0.0, 0.1)
]

def punto_en_obstaculo(px, py):
    """Verifica si un punto (x,y) está fuera del mapa o dentro de un obstáculo."""
    if px < 0 or px > 2.0 or py < 0 or py > 2.0:
        return True
    for (xmin, xmax, ymin, ymax) in OBSTACULOS:
        if xmin <= px <= xmax and ymin <= py <= ymax:
            return True
    return False

def hay_colision(esquinas):
    """Recibe las 4 esquinas del robot y verifica si alguna choca."""
    for ex, ey in esquinas:
        if punto_en_obstaculo(ex, ey):
            return True
    return False