import socket
import threading
import random
import time
import sys

from Nave import TIPOS_NAVES, EstrellaDeLaMuerte, Ejecutor, HalconMilenario, NaveRealNaboo, CazaEstelarJedi
from Mandaloriano import crear_mandaloriano
from Reino import Reino

HOST = '127.0.0.1'
PORT = 65432
MAX_CREDITOS = 100000

CLASES_NAVES = {
    1: EstrellaDeLaMuerte,
    2: Ejecutor,
    3: HalconMilenario,
    4: NaveRealNaboo,
    5: CazaEstelarJedi,
}

def enviar(conn, mensaje):
    data = (mensaje + "\n").encode()
    conn.sendall(data)

def recibir(conn):
    buffer = b""
    while True:
        chunk = conn.recv(1024)
        if not chunk:
            break
        buffer += chunk
        if b"\n" in buffer:
            linea, buffer = buffer.split(b"\n", 1)
            return linea.decode().strip()
    return ""

def configurar_reino(conn, numero):
    enviar(conn, f"Introduce nombre de tu Reino:")
    nombre = recibir(conn)
    reino = Reino(nombre)

    enviar(conn, f"CREAMOS LA FLOTA DE NAVES")
    for i in range(1, 6):
        nombre_nave, clase, coste = TIPOS_NAVES[i]
        while True:
            enviar(conn, f"Número de Naves ({nombre_nave}): ")
            try:
                cantidad = int(recibir(conn))
                if cantidad < 0:
                    enviar(conn, "Introduce un número válido.")
                    continue
                coste_parcial = cantidad * coste
                if reino.coste_total + coste_parcial > MAX_CREDITOS:
                    enviar(conn, f"Créditos insuficientes. Disponibles: {MAX_CREDITOS - reino.coste_total}. Inténtalo de nuevo.")
                    continue
                for _ in range(cantidad):
                    reino.agregar_nave(CLASES_NAVES[i]())
                break
            except ValueError:
                enviar(conn, "Introduce un número válido.")

    from Mandaloriano import STATS_MANDALORIANOS
    enviar(conn, f"CREAMOS LA LEGIÓN DE MANDALORIANOS")
    for nivel in range(1, 6):
        coste_mand = STATS_MANDALORIANOS[nivel][4]
        while True:
            enviar(conn, f"Número de Mandalorianos (Nivel {nivel}): ")
            try:
                cantidad = int(recibir(conn))
                if cantidad < 0:
                    enviar(conn, "Introduce un número válido.")
                    continue
                coste_parcial = cantidad * coste_mand
                if reino.coste_total + coste_parcial > MAX_CREDITOS:
                    enviar(conn, f"Créditos insuficientes. Disponibles: {MAX_CREDITOS - reino.coste_total}. Inténtalo de nuevo.")
                    continue
                for _ in range(cantidad):
                    reino.agregar_mandaloriano(crear_mandaloriano(nivel))
                break
            except ValueError:
                enviar(conn, "Introduce un número válido.")

    enviar(conn, f"Coste total: {reino.coste_total} Créditos")
    enviar(conn, "Configuración enviada. Esperando inicio batalla...")
    return reino

def simular_batalla(reino1, reino2, conn1, conn2):
    def broadcast(msg):
        print(msg)
        try:
            enviar(conn1, msg)
        except:
            pass
        try:
            enviar(conn2, msg)
        except:
            pass

    broadcast(f"\n=== CAMPO DE BATALLA GALÁCTICO ===")
    broadcast(f"=== BATALLA: {reino1.nombre} vs {reino2.nombre} ===")

    turno = 0
    while reino1.sigue_en_pie() and reino2.sigue_en_pie():
        turno += 1
        broadcast(f"\n=== TURNO {turno} ===")
        broadcast("COMBATES:")

        unidades_r1 = reino1.naves_vivas() + reino1.mandalorianos_vivos()
        unidades_r2 = reino2.naves_vivas() + reino2.mandalorianos_vivos()

        combates = []
        atacantes = list(unidades_r1) + list(unidades_r2)
        random.shuffle(atacantes)

        contador = 1
        for atacante in atacantes:
            if atacante in unidades_r1:
                objetivos = reino2.naves_vivas() + reino2.mandalorianos_vivos()
                reino_atacante = reino1.nombre
                reino_defensor = reino2.nombre
            else:
                objetivos = reino1.naves_vivas() + reino1.mandalorianos_vivos()
                reino_atacante = reino2.nombre
                reino_defensor = reino1.nombre

            if not objetivos:
                break

            objetivo = random.choice(objetivos)
            danio = atacante.atacar()
            danio_real = objetivo.recibir_danio(danio)

            if hasattr(objetivo, 'esta_viva'):
                muerto = not objetivo.esta_viva()
            else:
                muerto = not objetivo.esta_vivo()

            if muerto:
                estado_str = "DESTRUIDO/ELIMINADO"
            else:
                estado_str = f"HERIDO (Vida: {objetivo.vida}/{objetivo.vida_max})"

            broadcast(f"{contador}. {atacante.nombre} ({reino_atacante[:3]}) -> {objetivo.nombre} ({reino_defensor[:3]}) [DAÑO: {danio_real}] - {estado_str}")
            contador += 1

        broadcast(f"\nESTADO TURNO {turno}:")
        broadcast(f"| {'REINO':<20} | {'NAVES':^6} | {'MANDALORIANOS':^13} |")
        broadcast(f"| {reino1.nombre:<20} | {len(reino1.naves_vivas()):^6} | {len(reino1.mandalorianos_vivos()):^13} |")
        broadcast(f"| {reino2.nombre:<20} | {len(reino2.naves_vivas()):^6} | {len(reino2.mandalorianos_vivos()):^13} |")

        if not reino1.sigue_en_pie() or not reino2.sigue_en_pie():
            break

    broadcast(f"\n=== RESULTADO FINAL DE LA GUERRA ===")
    if reino1.sigue_en_pie():
        ganador, perdedor = reino1, reino2
    else:
        ganador, perdedor = reino2, reino1

    broadcast(f"GANADOR: {ganador.nombre}")
    broadcast(f"\nESTADÍSTICAS DE LA BATALLA:")
    broadcast(f"| {'REINO':<25} | {'PÉRDIDAS':^12} | {'SOBREVIVIENTES':^14} |")
    broadcast(f"| {reino1.nombre:<25} | {len(reino1.naves) - len(reino1.naves_vivas())} Naves, {len(reino1.mandalorianos) - len(reino1.mandalorianos_vivos())} Mand. | {len(reino1.naves_vivas())} Naves, {len(reino1.mandalorianos_vivos())} Mand. |")
    broadcast(f"| {reino2.nombre:<25} | {len(reino2.naves) - len(reino2.naves_vivas())} Naves, {len(reino2.mandalorianos) - len(reino2.mandalorianos_vivos())} Mand. | {len(reino2.naves_vivas())} Naves, {len(reino2.mandalorianos_vivos())} Mand. |")
    broadcast(f"\nDuración: {turno} turnos")

    try:
        if reino1 == ganador:
            enviar(conn1, f"¡BATALLA TERMINADA! {ganador.nombre} - ¡GANADOR!")
            enviar(conn2, f"¡DERROTA! {ganador.nombre} ha vencido.")
        else:
            enviar(conn2, f"¡BATALLA TERMINADA! {ganador.nombre} - ¡GANADOR!")
            enviar(conn1, f"¡DERROTA! {ganador.nombre} ha vencido.")
    except:
        pass

def iniciar_guerra():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)
    server.settimeout(10)

    print("\nINICIANDO GUERRA GALÁCTICA")
    conexiones = []
    try:
        for i in range(1, 3):
            print(f"Esperando conexión de Reino {i}...", end=" ", flush=True)
            conn, addr = server.accept()
            print("[CONECTADO]")
            conexiones.append(conn)
    except socket.timeout:
        print("\nTIMEOUT - No se conectaron ambos reinos.")
        print("Reiniciando servidor automáticamente...")
        for c in conexiones:
            c.close()
        server.close()
        return

    server.close()

    reinos = []
    hilos = []
    resultados = [None, None]

    def configurar(idx, conn):
        resultados[idx] = configurar_reino(conn, idx + 1)

    for i, conn in enumerate(conexiones):
        t = threading.Thread(target=configurar, args=(i, conn))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    reino1, reino2 = resultados
    print(f"\n========================================")
    print(f"CONFIGURACIÓN REINO 1: {reino1.nombre} - Coste: {reino1.coste_total}")
    print(f"CONFIGURACIÓN REINO 2: {reino2.nombre} - Coste: {reino2.coste_total}")
    print(f"Ambos Reinos configurados. INICIANDO BATALLA!")

    enviar(conexiones[0], "Ambos Reinos configurados correctamente. INICIANDO BATALLA.")
    enviar(conexiones[1], "Ambos Reinos configurados correctamente. INICIANDO BATALLA.")

    simular_batalla(reino1, reino2, conexiones[0], conexiones[1])

    for conn in conexiones:
        conn.close()

def main():
    while True:
        print("\n=== SERVIDOR - LA GUERRA DE LAS GALAXIAS (2026) ===")
        print("1. Iniciar Guerra")
        print("2. Finalizar Servidor")
        opcion = input("Seleccionar opción para continuar: ").strip()

        if opcion == "1":
            iniciar_guerra()
        elif opcion == "2":
            print("Servidor finalizado.")
            sys.exit(0)
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
