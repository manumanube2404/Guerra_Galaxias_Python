import socket
import sys

HOST = '127.0.0.1'
PORT = 65432

def main():
    print("=== CLIENTE - LA GUERRA DE LAS GALAXIAS (2026) ===")
    print("Conectando al servidor...", end=" ", flush=True)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print("ok")
    except ConnectionRefusedError:
        print(" No se pudo conectar. ¿Está el servidor activo?")
        sys.exit(1)

    buffer = b""
    while True:
        try:
            chunk = sock.recv(1024)
            if not chunk:
                print("\nConexión cerrada por el servidor.")
                break
            buffer += chunk
            while b"\n" in buffer:
                linea, buffer = buffer.split(b"\n", 1)
                mensaje = linea.decode().strip()
                if not mensaje:
                    continue

                if mensaje.endswith(": ") or mensaje.endswith(":"):
                    print(f"SERVIDOR: {mensaje}")
                    respuesta = input("> ").strip()
                    sock.sendall((respuesta + "\n").encode())
                else:
                    print(f"SERVIDOR: {mensaje}")

        except KeyboardInterrupt:
            print("\nDesconectado.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    sock.close()

if __name__ == "__main__":
    main()
