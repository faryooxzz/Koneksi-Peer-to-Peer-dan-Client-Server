import socket
import threading
import time

def listen_for_peers(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Peer listening on {ip}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        message = client_socket.recv(1024).decode('utf-8')
        print(f"Received message: {message}")

        response = f"Peer received: {message}"
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

def send_message_to_peer(peer_ip, peer_port, message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Hitung waktu koneksi ke peer
        start_connection_time = time.time()
        client_socket.connect((peer_ip, peer_port))
        connection_time = time.time() - start_connection_time

        # Kirim pesan ke peer dan catat waktu pengiriman
        start_send_time = time.time()
        client_socket.send(message.encode('utf-8'))
        message_size = len(message)  # Ukuran pesan

        # Terima balasan dari peer
        response = client_socket.recv(1024).decode('utf-8')
        end_time = time.time()

        # Hitung latency, waktu respon, dan throughput
        latency = start_send_time - start_connection_time
        response_time = end_time - start_connection_time
        throughput = message_size / response_time  # bytes per second

        print(f"Response from {peer_ip}:{peer_port} -> {response}")
        print(f"Connection time: {connection_time:.6f} seconds")
        print(f"Latency: {latency:.6f} seconds")
        print(f"Response time: {response_time:.6f} seconds")
        print(f"Throughput: {throughput:.6f} bytes/second")

        client_socket.close()
    except ConnectionRefusedError as e:
        print(f"[ERROR] Connection refused: {e}")
    except Exception as e:
        print(f"[ERROR] Error occurred: {e}")

# Input IP dan port untuk peer
my_ip = input("Enter your IP address: ")
my_port = int(input("Enter your port: "))
peer_ip = input("Enter the IP address of the peer to connect: ")
peer_port = int(input("Enter the port of the peer to connect: "))

# Jalankan listener di thread terpisah
threading.Thread(target=listen_for_peers, args=(my_ip, my_port)).start()

# Input pesan dari pengguna
message = input("Enter message to send to peer: ")
send_message_to_peer(peer_ip, peer_port, message)