import random

class Nave:
    def __init__(self, nombre, ataque, defensa, vida, velocidad, coste):
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.vida_max = vida
        self.vida = vida
        self.velocidad = velocidad
        self.coste = coste

    def esta_viva(self):
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


class EstrellaDeLaMuerte(Nave):
    def __init__(self):
        super().__init__("Estrella de la Muerte", 80, 90, 1500, random.randint(20, 30), 4500)

class Ejecutor(Nave):
    def __init__(self):
        super().__init__("Ejecutor", 70, 80, 1200, random.randint(35, 50), 4000)

class HalconMilenario(Nave):
    def __init__(self):
        super().__init__("Halcón Milenario", 60, 50, 800, 70, 2500)

class NaveRealNaboo(Nave):
    def __init__(self):
        super().__init__("Nave Real de Naboo", 40, 60, 600, 50, 2000)

class CazaEstelarJedi(Nave):
    def __init__(self):
        super().__init__("Caza Estelar Jedi", 50, 40, 400, 80, 1500)

TIPOS_NAVES = {
    1: ("Estrella de la Muerte", EstrellaDeLaMuerte, 4500),
    2: ("Ejecutor", Ejecutor, 4000),
    3: ("Halcón Milenario", HalconMilenario, 2500),
    4: ("Nave Real de Naboo", NaveRealNaboo, 2000),
    5: ("Caza Estelar Jedi", CazaEstelarJedi, 1500),
}
