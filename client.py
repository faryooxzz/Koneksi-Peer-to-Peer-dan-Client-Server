import socket
from datetime import datetime

# Setup client
client_ip = '192.168.137.17'
server_port = 4000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Catat waktu saat mencoba menghubungkan ke server
connect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"[CONNECTING] Trying to connect to server at {connect_time}.")

client.connect((client_ip, server_port))

# Catat waktu berhasil terhubung
connected_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"[CONNECTED] Connected to server at {connected_time}.")

# Mengirim pesan dan catat waktu pengiriman
message = input("Enter message to send: ")
send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
client.send(message.encode('utf-8'))
print(f"[MESSAGE SENT] Sent message at {send_time}.")

# Menerima balasan dari server dan catat waktu penerimaan
response = client.recv(1024).decode('utf-8')
receive_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"[RESPONSE RECEIVED] Server responded: {response} at {receive_time}.")

# Tutup koneksi
client.close()
disconnect_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"[DISCONNECTED] Disconnected from server at {disconnect_time}.")
