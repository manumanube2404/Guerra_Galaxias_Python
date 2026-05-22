import socket
import sys
import threading
import pygame

HOST = '127.0.0.1'
PORT = 65432

# --- Colores y fuentes ---
NEGRO     = (0, 0, 0)
AMARILLO  = (255, 215, 0)
BLANCO    = (255, 255, 255)
GRIS      = (140, 140, 140)
ROJO      = (220, 70, 70)
VERDE     = (80, 220, 120)
AZUL_OSC  = (10, 10, 40)

ANCHO, ALTO = 900, 650
MAX_LINEAS  = 22       # líneas visibles en el log
FUENTE_TAM  = 18

# --- Estado global compartido entre el hilo de red y el de pygame ---
mensajes   = []        # log de mensajes del servidor
esperando  = False     # indica si el servidor pide respuesta
ultimo_msg = ""        # último prompt recibido
lock       = threading.Lock()

sock = None            # socket global

# --- Hilo de red: recibe mensajes del servidor ---

def hilo_red():
    global esperando, ultimo_msg
    buffer = b""
    while True:
        try:
            chunk = sock.recv(1024)
            if not chunk:
                with lock:
                    mensajes.append("Conexión cerrada por el servidor...")
                break
            buffer += chunk
            while b"\n" in buffer:
                linea, buffer = buffer.split(b"\n", 1)
                msg = linea.decode().strip()
                if not msg:
                    continue
                with lock:
                    mensajes.append(f"SERVIDOR: {msg}")
                    if msg.endswith(": ") or msg.endswith(":"):
                        esperando = True
                        ultimo_msg = msg
                    else:
                        esperando = False
        except Exception as e:
            with lock:
                mensajes.append(f">> Error de red: {e}")
            break

# --- Dibujado principal ---

def dibujar(screen, fuente, fuente_titulo, input_texto):
    screen.fill(AZUL_OSC)

    titulo = fuente_titulo.render("LA GUERRA DE LAS GALAXIAS 2026", True, AMARILLO)
    screen.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 10))
    pygame.draw.line(screen, AMARILLO, (20, 48), (ANCHO - 20, 48), 2)

    with lock:
        lineas_mostrar = mensajes[-MAX_LINEAS:]

    y = 60
    for linea in lineas_mostrar:
        if "GANADOR" in linea or "¡GANADOR" in linea:
            color = VERDE
        elif "DERROTA" in linea or "DESTRUIDO" in linea or "ELIMINADO" in linea:
            color = ROJO
        elif "TURNO" in linea or "BATALLA" in linea:
            color = AMARILLO
        else:
            color = BLANCO

        texto = fuente.render(linea[:96], True, color)
        screen.blit(texto, (20, y))
        y += FUENTE_TAM + 2

    pygame.draw.line(screen, AMARILLO, (20, ALTO - 70), (ANCHO - 20, ALTO - 70), 1)
    if esperando:
        prompt = fuente.render(f"{ultimo_msg} {input_texto}_", True, VERDE)
    else:
        prompt = fuente.render("Esperando instrucciones del servidor...", True, GRIS)
    screen.blit(prompt, (20, ALTO - 55))

    pygame.display.flip()

# --- Main pygame ---

def main():
    global sock, esperando

    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("La Guerra de las Galaxias 2026")
    clock = pygame.time.Clock()
    fuente = pygame.font.SysFont("Courier New", FUENTE_TAM)
    fuente_tit = pygame.font.SysFont("Courier New", 22, bold=True)

    with lock:
        mensajes.append("Conectando al servidor...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        with lock:
            mensajes.append("Conexión establecida. ¡Listo para pelear!")
    except ConnectionRefusedError:
        with lock:
            mensajes.append("ERROR: No se pudo conectar. Asegúrate de que el servidor esté activo.")
        running = True
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
            dibujar(screen, fuente, fuente_tit, "")
            clock.tick(30)
        pygame.quit()
        sys.exit(1)

    t = threading.Thread(target=hilo_red, daemon=True)
    t.start()

    input_texto = ""
    running = True

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and esperando:
                if ev.key == pygame.K_RETURN:
                    respuesta = input_texto.strip()
                    if respuesta:
                        with lock:
                            mensajes.append(f"> {respuesta}")
                            esperando = False
                        sock.sendall((respuesta + "\n").encode())
                    input_texto = ""
                elif ev.key == pygame.K_BACKSPACE:
                    input_texto = input_texto[:-1]
                elif ev.key == pygame.K_ESCAPE:
                    input_texto = ""
                else:
                    if ev.unicode and ev.unicode.isprintable():
                        input_texto += ev.unicode

        dibujar(screen, fuente, fuente_tit, input_texto)
        clock.tick(30)

    sock.close()
    pygame.quit()


if __name__ == "__main__":
    main()
