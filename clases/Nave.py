import random

class Unidad:
    # Clase base para cada unidad de combate del juego.
    def __init__(self, nombre, ataque, defensa, vida, velocidad, coste):
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.vida_max = vida
        self.vida = vida
        self.velocidad = velocidad
        self.coste = coste

    def esta_viva(self):
        # Devuelve True si la unidad aún tiene vida.
        return self.vida > 0

    def recibir_daño(self, daño):
        # Aplica daño, resta defensa y actualiza la vida.
        daño_real = max(0, daño - self.defensa // 2)
        self.vida = max(0, self.vida - daño_real)
        return daño_real

    def atacar(self):
        # Calcula cuántos puntos de daño hace este ataque.
        return random.randint(self.ataque, self.ataque * 2)

    def __str__(self):
        return f"{self.nombre} (Vida: {self.vida}/{self.vida_max}, Ataque: {self.ataque}, Defensa: {self.defensa})"


class Nave(Unidad):
    # Nave espacial con estadísticas de combate.
    def __init__(self, nombre, ataque, defensa, vida, velocidad, coste):
        super().__init__(nombre, ataque, defensa, vida, velocidad, coste)


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

CLASES_NAVES = {
    1: EstrellaDeLaMuerte,
    2: Ejecutor,
    3: HalconMilenario,
    4: NaveRealNaboo,
    5: CazaEstelarJedi,
}
