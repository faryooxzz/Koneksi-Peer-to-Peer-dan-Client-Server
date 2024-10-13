import socket
import threading
from datetime import datetime

# Fungsi untuk menangani koneksi dari setiap client
def handle_client(client_socket, client_address):
    # Catat waktu koneksi
    connection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[NEW CONNECTION] {client_address} connected at {connection_time}.")
    
    while True:
        try:
            # Terima pesan dari client dan catat waktu penerimaan
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            receive_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[RECEIVED] {client_address}: {message} at {receive_time}")
            
            # Kirim balasan ke client dan catat waktu pengiriman balasan
            client_socket.send("Message received!".encode('utf-8'))
            response_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[RESPONSE SENT] to {client_address} at {response_time}")
            
        except:
            break
    
    # Catat waktu disconnect
    disconnect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[DISCONNECT] {client_address} disconnected at {disconnect_time}.")
    client_socket.close()

# Setup server
server_ip = '192.168.137.17'
server_port = 4000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)
print(f"[LISTENING] Server is listening on {server_ip}:{server_port}")

while True:
    client_socket, client_address = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
