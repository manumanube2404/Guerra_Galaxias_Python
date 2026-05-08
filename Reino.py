class Reino:
    def __init__(self, nombre):
        self.nombre = nombre
        self.naves = []
        self.mandalorianos = []
        self.coste_total = 0

    def agregar_nave(self, nave):
        self.naves.append(nave)
        self.coste_total += nave.coste

    def agregar_mandaloriano(self, mand):
        self.mandalorianos.append(mand)
        self.coste_total += mand.coste

    def naves_vivas(self):
        return [n for n in self.naves if n.esta_viva()]

    def mandalorianos_vivos(self):
        return [m for m in self.mandalorianos if m.esta_vivo()]

    def sigue_en_pie(self):
        return len(self.naves_vivas()) > 0 or len(self.mandalorianos_vivos()) > 0

    def total_unidades(self):
        return len(self.naves_vivas()) + len(self.mandalorianos_vivos())
