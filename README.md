# La Guerra de las Galaxias 2026

## Estructura 

- `servidor.py` - punto de entrada del servidor.
- `cliente.py` - cliente de texto para participar en la partida.
- `cliente_pygame.py` - cliente gráfico basado en Pygame.
- `clases/` - módulo que contiene las clases del juego:
  - `Nave.py`
  - `Mandaloriano.py`
  - `Reino.py`

## Ejecución

1. Ejecuta primero el servidor:
   ```bash
   python servidor.py
   ```

2. Ejecuta dos clientes en otras terminales:
   ```bash
   python cliente.py
   ```
   o
   ```bash
   python cliente_pygame.py
   ```

3. Sigue las instrucciones de cada cliente para configurar los reinos y comenzar la batalla.
