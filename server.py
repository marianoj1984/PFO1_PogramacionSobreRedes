import socket
import sqlite3
import threading
import datetime

# Inicializa la base de datos
def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        contenido TEXT NOT NULL,
                        fecha_envio TEXT NOT NULL,
                        ip_cliente TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Inicializa el socket del servidor
def init_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('localhost', 5000))
        server_socket.listen(5)
        print("Servidor escuchando en localhost:5000...")
        return server_socket
    except socket.error as e:
        print(f"Error al iniciar el servidor: {e}")
        return None

# Guarda un mensaje en la base de datos
def save_message(contenido, ip_cliente):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    fecha_envio = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO messages (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                   (contenido, fecha_envio, ip_cliente))
    conn.commit()
    conn.close()

# Maneja las conexiones de los clientes
def handle_client(client_socket, client_address):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message or message.lower() == "éxito":
            break
        save_message(message, client_address[0])
        response = f"Mensaje recibido: {datetime.datetime.now().strftime('%H:%M:%S')}"
        client_socket.send(response.encode('utf-8'))
    client_socket.close()

def start_server():
    init_db()
    server_socket = init_server()
    if server_socket:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Conexión establecida con {client_address}")
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

start_server()
