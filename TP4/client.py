import socket
import json
import argparse
from cryptography.fernet import Fernet

GROUP = "Xi JinPIng Revenge"


def cargar_clave(ruta):
    with open(ruta, "rb") as key_file:
        return key_file.read()


def main():
    parser = argparse.ArgumentParser(
        description="Cliente TCP que envia mensajes JSON con la payload cifrada (Fernet/AES)."
    )
    parser.add_argument("--host", default="127.0.0.1", help="IP del servidor de destino")
    parser.add_argument("--port", type=int, default=5000, help="Puerto del servidor de destino")
    parser.add_argument("--key", default="clave.key", help="Archivo con la clave simetrica")
    args = parser.parse_args()

    cipher = Fernet(cargar_clave(args.key))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((args.host, args.port))
    print(f"Conectado a {args.host}:{args.port}")
    print("Escribi un mensaje y presiona Enter. Escribi 'salir' para terminar.\n")

    try:
        while True:
            texto = input("> ")
            if texto.strip().lower() == "salir":
                print("Cerrando conexion...")
                break
            if not texto:
                continue

            payload_cifrada = cipher.encrypt(texto.encode("utf-8")).decode("utf-8")
            mensaje = {"group": GROUP, "payload": payload_cifrada}
            client.sendall(json.dumps(mensaje).encode("utf-8"))

    except (KeyboardInterrupt, EOFError):
        print("\nCerrando conexion.")
    finally:
        client.close()


if __name__ == "__main__":
    main()
