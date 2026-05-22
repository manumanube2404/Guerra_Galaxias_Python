# Clase que agrupa todas las unidades de un jugador
class Reino:
    def __init__(self, nombre):
        self.nombre = nombre
        self.naves = []
        self.mandalorianos = []
        self.coste_total = 0

    def agregar_nave(self, nave):
        # Agrega una nave al reino y suma su coste al total.
        self.naves.append(nave)
        self.coste_total += nave.coste

    def agregar_mandaloriano(self, mand):
        # Agrega un mandaloriano al reino y suma su coste al total.
        self.mandalorianos.append(mand)
        self.coste_total += mand.coste

    @property
    def unidades(self):
        # Devuelve todas las unidades del reino, naves y mandalorianos.
        return self.naves + self.mandalorianos

    def unidades_vivas(self):
        # Lista todas las unidades que siguen con vida.
        return [u for u in self.unidades if u.esta_viva()]

    def naves_vivas(self):
        return [n for n in self.naves if n.esta_viva()]

    def mandalorianos_vivos(self):
        return [m for m in self.mandalorianos if m.esta_viva()]

    def calcula_perdidas(self):
        # Devuelve cuántas unidades se han perdido hasta ahora.
        naves_tot = len(self.naves)
        mand_tot = len(self.mandalorianos)
        return naves_tot - len(self.naves_vivas()), mand_tot - len(self.mandalorianos_vivos())

    def sigue_en_pie(self):
        # El reino sigue en pie si tiene al menos una unidad viva.
        return bool(self.unidades_vivas())

    def resumen(self):
        # Genera un diccionario con el estado del reino.
        naves_vivas = len(self.naves_vivas())
        mand_vivos = len(self.mandalorianos_vivos())
        perdidas_naves, perdidas_mand = self.calcula_perdidas()
        return {
            "nombre": self.nombre,
            "coste_total": self.coste_total,
            "naves_vivas": naves_vivas,
            "mandalorianos_vivos": mand_vivos,
            "perdidas_naves": perdidas_naves,
            "perdidas_mandalorianos": perdidas_mand,
        }
