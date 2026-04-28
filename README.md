# Planificación de Movimientos: Robot Diferencial LEGO Mindstorms

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LEGO](https://img.shields.io/badge/LEGO-Mindstorms-E3000B.svg)]()

>**Instituto Tecnológico Superior de Salvatierra**
>
>**Ing. en Tecnologías de la Información y Comunicaciones**
>
>**Materia: Planificación de Movimientos | Dr. Francisco Javier Montecillo Puente**

---

## Objetivo SMART
[cite_start]Implementar un **plan de movimientos en el prototipo físico del kit LEGO Mindstorms** [cite: 11][cite_start], generado a partir de un algoritmo de planificación cinemática que integra un modelo matemático, planificador de trayectorias, colisionador y simulador[cite: 11].

---

## Fases del Proyecto (Roadmap)
- [ ] **1. Construcción y Modelo:** Armado del LEGO [cite: 26] [cite_start]y definición del modelo cinemático 2D[cite: 27].
- [ ] **2. Simulador Cinemático:** Desarrollo en Python para simular movimientos en línea recta, giros (izquierda/derecha) y combinados[cite: 28].
- [ ] **3. Mapeo y Colisiones:** Representación de un mapa de 2x2 metros con obstáculos [cite: 19] [cite_start]y cálculo del espacio de configuración (C-space) libre de colisiones[cite: 21].
- [ ] **4. Planificación (Grafo):** Generación de un grafo partiendo de la coordenada 0.0, expandiendo nodos con combinaciones de configuración hasta alcanzar aproximadamente 1000 nodos válidos[cite: 22].
- [ ] **5. Ejecución Física:** Planteamiento de 3 trayectorias [cite: 30][cite_start], comprobadas en el simulador y ejecutadas en el carrito LEGO[cite: 29, 30].
- [ ] **6. Documentación:** Reporte de 30 hojas (metodología, ecuaciones, diagramas) [cite: 17] [cite_start]y video de evidencia[cite: 31, 32].

---

## Estructura del Repositorio
```text
lego-mindstorms-motion-planning/
├── docs/
│   └── lego_modelo_cinematico.docx   # Reporte completo de 30 hojas (metodología, desarrollo)
├── simulador/
│   ├── robot_kinematics.py           # Modelo cinemático 2D (diff-drive)
│   ├── collision_checker.py          # Detector de colisiones con obstáculos en mapa 2x2
│   ├── cspace_builder.py             # Construcción del grafo de configuración (~1000 nodos)
│   ├── trajectory_planner.py         # Generador de las 3 trayectorias (rectas, giros, combinadas)
│   └── visualizer.py                 # Visualización del mapa y trayectorias
├── lego_code/
│   └── robot_movements.py            # Código para ejecutar movimientos físicos en LEGO
├── media/
│   ├── cspace_result.png             # Figura 22: Ángulos libres de colisión
│   ├── simulator_demo.gif            # Demo del simulador en acción
│   └── video_demo.mp4                # Video del robot físico ejecutando trayectorias
└── README.md

```

## 💻 Guía de Configuración y Ejecución

Sigue estos pasos para levantar el proyecto en tu máquina local:

### 1. Crear el Entorno Virtual
Para mantener las dependencias aisladas, crea un entorno de Python:
```bash
python -m venv venv
```
### 2. Activar el Entorno
En Windows (PowerShell):
Si recibes un error de permisos, ejecuta primero el comando para habilitar scripts:

```bash
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
```
Luego activa el entorno:

```bash
.\venv\Scripts\activate
```

### 3. Instalar Requerimientos
Con el entorno activado, instala las librerías necesarias (Numpy, Matplotlib, Pillow):

```bash
pip install -r requirements.txt
```

### 4. Correr la Simulación
Para ejecutar el planificador, ver los movimientos básicos y elegir una ruta para el LEGO, corre:

```bash
python simulator/trajectory_planner.py
```
