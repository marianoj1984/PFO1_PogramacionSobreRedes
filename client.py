import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    
    while True:
        message = input("Escribe un mensaje (o 'éxito' para salir): ")
        client_socket.send(message.encode('utf-8'))
        if message.lower() == "éxito":
            break
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Respuesta del servidor: {response}")
    
    client_socket.close()

start_client()
