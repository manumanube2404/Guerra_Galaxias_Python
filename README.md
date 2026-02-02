# 🌌 Proyecto: La Guerra de las Galaxias (2026)

Este proyecto implementa una arquitectura distribuida **Cliente-Servidor** en Python diseñada para la simulación estocástica de batallas espaciales. El sistema orquesta enfrentamientos en tiempo real entre dos entidades ("Reinos"), gestionando la comunicación de red mediante Sockets TCP/IP, concurrencia mediante hilos (threading) y lógica de negocio basada en modelos de objetos (POO).

## 📋 Descripción del Sistema

El software simula un conflicto bélico galáctico donde un servidor central actúa como "Game Master" o árbitro, y dos clientes actúan como jugadores. El flujo de ejecución se centra en la gestión de estados, validación de presupuestos y cálculo de daño por turnos.

### Componentes Principales

1.  **Servidor (Backend):**
    * Responsable del ciclo de vida de la sesión (conexión, batalla, desconexión).
    * Implementa un **Watchdog Timer** de 10 segundos para la sincronización de conexiones.
    * Procesa la lógica de combate: cálculo de daño (Ataque vs Defensa), velocidad de turno y condiciones de victoria.

2.  **Cliente (Frontend):**
    * Interfaz de línea de comandos (CLI) para la interacción del usuario.
    * Gestor de configuración de flota (selección de unidades).
    * Receptor de telemetría de batalla en tiempo real.

## ⚙️ Especificaciones Funcionales

### 1. Protocolo de Conexión
El sistema requiere la conexión sincronizada de dos clientes.
* **Inicio:** El servidor abre un socket de escucha.
* **Timeout:** Tras la conexión del primer cliente (`Jugador 1`), se activa una ventana de **10 segundos** para la conexión del `Jugador 2`. Si el tiempo expira, el servidor aborta la sesión y se reinicia.

### 2. Gestión de Recursos (Presupuesto)
Cada reino dispone de un presupuesto máximo (ej. **100.000 Créditos Galácticos**) para la adquisición de unidades bélicas.
* El sistema valida matemáticamente la configuración enviada por el cliente.
* Si `Σ(Coste Unidades) > Presupuesto`, la configuración es rechazada y se solicita el reingreso de datos.

### 3. Motor de Simulación
La batalla se resuelve mediante un algoritmo iterativo:
1.  **Iniciativa:** Determinada por la velocidad de las unidades vivas.
2.  **Resolución de Daño:** Se aplican fórmulas basadas en los atributos de las unidades (Ataque y Defensa).
3.  **Eliminación:** Las unidades cuya `Vida <= 0` son retiradas de las listas activas.
4.  **Terminación:** La simulación concluye cuando un bando pierde todas sus unidades.

## 📊 Tabla de Especificaciones de Unidades

Para la configuración estratégica, se deben considerar los siguientes atributos técnicos y costes.

### 🛸 Naves Espaciales (Clase Nave)
Unidades de alto coste, blindaje pesado y gran potencia de fuego.

| Tipo de Nave | Ataque | Defensa | Vida | Velocidad | Coste (Créditos) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Estrella de la Muerte** | 80 | 90 | 1500 | 20-30 | 4.500 |
| **Ejecutor** | 70 | 80 | 1200 | 35-50 | 4.000 |
| **Halcón Milenario** | 60 | 50 | 800 | 70 | 2.500 |
| **Nave Real de Naboo** | 40 | 60 | 600 | 50 | 2.000 |
| **Caza Estelar Jedi** | 50 | 40 | 400 | 80 | 1.500 |

### 🛡️ Mandalorianos (Clase Mandaloriano)
Unidades de infantería versátiles, clasificadas por niveles de habilidad.

| Tipo / Nivel | Ataque | Defensa | Vida | Velocidad | Coste (Créditos) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mandaloriano 1** | 20 | 15 | 100 | 60 | 800 |
| **Mandaloriano 2** | 25 | 20 | 120 | 50 | 1.000 |
| **Mandaloriano 3** | 30 | 25 | 140 | 40 | 1.200 |
| **Mandaloriano 4** | 35 | 30 | 160 | 30 | 1.500 |
| **Mandaloriano 5** | 40 | 35 | 180 | 20 | 2.000 |

## 🚀 Instrucciones de Ejecución

### Requisitos del Entorno
* Python 3.x
* Librerías estándar: `socket`, `threading`, `random`, `time`.

### Despliegue

1.  **Inicialización del Servidor:**
    Ejecutar el script principal del servidor.
    ```bash
    python servidor.py
    ```
    Seleccionar la opción `1. Iniciar Guerra` en el menú para habilitar el puerto.

2.  **Conexión de Clientes:**
    En terminales separadas, ejecutar los scripts de cliente.
    ```bash
    python cliente.py
    ```
    *Nota: Asegurar la conexión del segundo cliente dentro de la ventana de tiempo establecida.*

3.  **Interacción:**
    Seguir las instrucciones en pantalla para nombrar el Reino y asignar la cantidad de unidades deseadas respetando el límite de créditos.

## 📝 Criterios de Calidad y Evaluación

El proyecto ha sido desarrollado cumpliendo los siguientes estándares de evaluación:

* **Funcionalidad (40%):** Cumplimiento estricto de la lógica de simulación y reglas de negocio.
* **Calidad de Código (25%):** Implementación limpia de clases, modularidad y buenas prácticas.
* **Estabilidad (20%):** Robustez en la comunicación Cliente-Servidor y manejo de excepciones.
* **Colaboración (15%):** Distribución equitativa de cargas de trabajo.

---
*Documentación técnica generada para el proyecto "La Guerra de las Galaxias".*


https://prod.liveshare.vsengsaas.visualstudio.com/join?FD2A621E040BB96C5BDF4C83511D4B79EA29
