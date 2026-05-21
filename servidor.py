import socket
import threading
import random
import sys

from clases.Nave import TIPOS_NAVES, CLASES_NAVES
from clases.Mandaloriano import crear_mandaloriano, STATS_MANDALORIANOS
from clases.Reino import Reino

HOST = '127.0.0.1'
PORT = 65432
MAX_CREDITOS = 100000

# --- Utilidades de comunicación ---

def enviar(conn, mensaje):
    conn.sendall((mensaje + "\n").encode())


def recibir(conn):
    """Lee una línea completa desde el socket y devuelve el texto sin saltos."""
    buffer = b""
    while True:
        chunk = conn.recv(1024)
        if not chunk:
            break
        buffer += chunk
        if b"\n" in buffer:
            linea, _ = buffer.split(b"\n", 1)
            return linea.decode().strip()
    return ""

# --- Configuración del reino de cada cliente ---

def configurar_reino(conn, numero):
    enviar(conn, "Introduce nombre de tu Reino:")
    nombre = recibir(conn)
    while True:
        reino = Reino(nombre)

        enviar(conn, "CREAMOS TU FLOTA GALÁCTICA")
        for i in range(1, 6):
            nombre_nave, _, coste = TIPOS_NAVES[i]
            while True:
                creditos_restantes = MAX_CREDITOS - reino.coste_total
                enviar(conn, f"Tienes {creditos_restantes} créditos disponibles.")
                enviar(conn, f"¿Cuántas naves '{nombre_nave}' quieres? (cada una cuesta {coste}):")
                try:
                    cantidad = int(recibir(conn))
                    if cantidad < 0:
                        enviar(conn, "Introduce un número entero no negativo.")
                        continue
                    if reino.coste_total + cantidad * coste > MAX_CREDITOS:
                        faltan = reino.coste_total + cantidad * coste - MAX_CREDITOS
                        enviar(conn, f"Créditos insuficientes. Te faltan {faltan} créditos.")
                        continue
                    for _ in range(cantidad):
                        reino.agregar_nave(CLASES_NAVES[i]())
                    break
                except ValueError:
                    enviar(conn, "Introduce un número válido, por ejemplo 0, 1, 2...")

        enviar(conn, "CREAMOS TU LEGIÓN DE MANDALORIANOS")
        for nivel in range(1, 6):
            coste_mand = STATS_MANDALORIANOS[nivel][4]
            while True:
                creditos_restantes = MAX_CREDITOS - reino.coste_total
                enviar(conn, f"Tienes {creditos_restantes} créditos disponibles.")
                enviar(conn, f"¿Cuántos Mandalorianos de nivel {nivel} quieres? (cada uno cuesta {coste_mand}):")
                try:
                    cantidad = int(recibir(conn))
                    if cantidad < 0:
                        enviar(conn, "Introduce un número entero no negativo.")
                        continue
                    if reino.coste_total + cantidad * coste_mand > MAX_CREDITOS:
                        faltan = reino.coste_total + cantidad * coste_mand - MAX_CREDITOS
                        enviar(conn, f"Créditos insuficientes. Te faltan {faltan} créditos.")
                        continue
                    for _ in range(cantidad):
                        reino.agregar_mandaloriano(crear_mandaloriano(nivel))
                    break
                except ValueError:
                    enviar(conn, "Introduce un número válido, por ejemplo 0, 1, 2...")

        if reino.unidades:
            break
        enviar(conn, "No puede haber un Reino sin unidades. Volvemos a configurar tu flota.")

    enviar(conn, f"Coste total del Reino '{reino.nombre}': {reino.coste_total} créditos")
    enviar(conn, "Configuración recibida. En breve comienza la batalla...")
    return reino

# --- Lógica de batalla por turnos ---

def simular_batalla(reino1, reino2, conn1, conn2):
    def broadcast(msg):
        # Enviamos el mensaje a los dos clientes y lo mostramos en consola.
        print(msg)
        for conn in (conn1, conn2):
            try:
                enviar(conn, msg)
            except Exception:
                pass

    broadcast(f"\n=== CAMPO DE BATALLA GALÁCTICO ===")
    broadcast(f"=== BATALLA: {reino1.nombre} vs {reino2.nombre} ===")

    turno = 0
    while reino1.sigue_en_pie() and reino2.sigue_en_pie():
        turno += 1
        broadcast(f"\n=== TURNO {turno} ===")
        broadcast("COMIENZA LA FASE DE ATAQUES")

        atacantes = reino1.unidades_vivas() + reino2.unidades_vivas()
        random.shuffle(atacantes)
        atacantes.sort(key=lambda unidad: unidad.velocidad, reverse=True)

        contador = 1
        for atacante in atacantes:
            if not atacante.esta_viva():
                continue

            if atacante in reino1.unidades_vivas():
                objetivos = reino2.unidades_vivas()
                atacante_reino = reino1.nombre
                defensa_reino = reino2.nombre
            else:
                objetivos = reino1.unidades_vivas()
                atacante_reino = reino2.nombre
                defensa_reino = reino1.nombre

            if not objetivos:
                break

            objetivo = random.choice(objetivos)
            danio = atacante.atacar()
            danio_real = objetivo.recibir_danio(danio)
            muerto = not objetivo.esta_viva()
            estado = "DESTRUIDO/ELIMINADO" if muerto else f"HERIDO (Vida: {objetivo.vida}/{objetivo.vida_max})"

            broadcast(f"{contador}. {atacante.nombre} ({atacante_reino[:3]}) -> {objetivo.nombre} ({defensa_reino[:3]}) [DAÑO: {danio_real}] - {estado}")
            contador += 1

        broadcast(f"\nESTADO TURNO {turno}:")
        broadcast(f"| {'REINO':<20} | {'NAVES':^6} | {'MANDALORIANOS':^13} |")
        broadcast(f"| {reino1.nombre:<20} | {len(reino1.naves_vivas()):^6} | {len(reino1.mandalorianos_vivos()):^13} |")
        broadcast(f"| {reino2.nombre:<20} | {len(reino2.naves_vivas()):^6} | {len(reino2.mandalorianos_vivos()):^13} |")

    broadcast(f"\n=== RESULTADO FINAL DE LA GUERRA ===")
    ganador, perdedor = (reino1, reino2) if reino1.sigue_en_pie() else (reino2, reino1)
    broadcast(f"GANADOR: {ganador.nombre}")
    broadcast(f"\nESTADÍSTICAS DE LA BATALLA:")
    broadcast(f"| {'REINO':<25} | {'PÉRDIDAS':^18} | {'SOBREVIVIENTES':^18} |")
    for reino in (reino1, reino2):
        perdidas_naves, perdidas_mand = reino.calcula_perdidas()
        perdidas = f"{perdidas_naves} Naves, {perdidas_mand} Mand."
        sobrevivientes = f"{len(reino.naves_vivas())} Naves, {len(reino.mandalorianos_vivos())} Mand."
        broadcast(f"| {reino.nombre:<25} | {perdidas:^18} | {sobrevivientes:^18} |")
    broadcast(f"\nCOSTE TOTAL DE LA BATALLA: {reino1.coste_total + reino2.coste_total} créditos")
    broadcast(f"\nDuración: {turno} turnos")

    try:
        enviar(conn1, f"{'¡GANADOR!' if ganador == reino1 else '¡DERROTA!'} {ganador.nombre} ha vencido.")
        enviar(conn2, f"{'¡GANADOR!' if ganador == reino2 else '¡DERROTA!'} {ganador.nombre} ha vencido.")
    except Exception:
        pass

# --- Gestión de conexiones ---

def iniciar_guerra():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)
    server.settimeout(10)  # 10 segundos para que se conecten ambos clientes

    print("\nINICIANDO GUERRA GALÁCTICA")
    conexiones = []
    while len(conexiones) < 2:
        try:
            print(f"Esperando conexión de Reino {len(conexiones) + 1}...", end=" ", flush=True)
            conn, _ = server.accept()
            print("[CONECTADO]")
            conexiones.append(conn)
        except socket.timeout:
            print("\nTIMEOUT - esperando que se conecten los reinos restantes...")
            continue

    server.close()

    resultados = [None, None]

    def configurar(idx, conn):
        resultados[idx] = configurar_reino(conn, idx + 1)

    hilos = [threading.Thread(target=configurar, args=(i, conn)) for i, conn in enumerate(conexiones)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    reino1, reino2 = resultados
    print(f"\nREINO 1: {reino1.nombre} - {reino1.coste_total} créditos")
    print(f"REINO 2: {reino2.nombre} - {reino2.coste_total} créditos")

    enviar(conexiones[0], "Ambos Reinos configurados correctamente. INICIANDO BATALLA.")
    enviar(conexiones[1], "Ambos Reinos configurados correctamente. INICIANDO BATALLA.")

    simular_batalla(reino1, reino2, conexiones[0], conexiones[1])

    for conn in conexiones:
        conn.close()

# --- Menú principal del servidor ---

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
            print("Opción no válida. Elige 1 o 2.")


if __name__ == "__main__":
    main()
