import random

from clases.Nave import Unidad


class Mandaloriano(Unidad):
    """Soldado mandaloriano con estadísticas de ataque, defensa y coste."""
    def __init__(self, nivel, ataque, defensa, vida, velocidad, coste):
        nombre = f"Mandaloriano {nivel}"
        super().__init__(nombre, ataque, defensa, vida, velocidad, coste)
        self.nivel = nivel

    def esta_vivo(self):
        """Compatibilidad con el resto del juego."""
        return self.esta_viva()

    def __str__(self):
        return f"{self.nombre} (Nivel {self.nivel}, Vida: {self.vida}/{self.vida_max})"


STATS_MANDALORIANOS = {
    1: (20, 15, 100, 60, 800),
    2: (25, 20, 120, 50, 1000),
    3: (30, 25, 140, 40, 1200),
    4: (35, 30, 160, 30, 1500),
    5: (40, 35, 180, 20, 2000),
}


def crear_mandaloriano(nivel):
    """Crea y devuelve un Mandaloriano del nivel indicado."""
    stats = STATS_MANDALORIANOS[nivel]
    return Mandaloriano(nivel, *stats)
