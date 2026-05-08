import random

class Mandaloriano:
    def __init__(self, nivel, ataque, defensa, vida, velocidad, coste):
        self.nivel = nivel
        self.nombre = f"Mandaloriano {nivel}"
        self.ataque = ataque
        self.defensa = defensa
        self.vida_max = vida
        self.vida = vida
        self.velocidad = velocidad
        self.coste = coste

    def esta_vivo(self):
        return self.vida > 0

    def recibir_danio(self, danio):
        danio_real = max(0, danio - self.defensa // 2)
        self.vida -= danio_real
        if self.vida < 0:
            self.vida = 0
        return danio_real

    def atacar(self):
        return random.randint(self.ataque, self.ataque * 2)

    def __str__(self):
        return f"{self.nombre} (Vida: {self.vida}/{self.vida_max})"


STATS_MANDALORIANOS = {
    1: (20, 15, 100, 60, 800),
    2: (25, 20, 120, 50, 1000),
    3: (30, 25, 140, 40, 1200),
    4: (35, 30, 160, 30, 1500),
    5: (40, 35, 180, 20, 2000),
}

def crear_mandaloriano(nivel):
    stats = STATS_MANDALORIANOS[nivel]
    return Mandaloriano(nivel, *stats)
