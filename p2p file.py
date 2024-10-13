import socket
import threading
import os
import time

PEERS = [('192.168.137.17', 4001), ('192.168.137.20', 4002)]


def scan_files(base_dir='shared_files'):
    shared_files = {}
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            shared_files[file] = file_path 
    return shared_files


def run_server(host, port, shared_files):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  
    server_socket.listen(5)
    print(f"Node running as server on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr, shared_files)).start()


def handle_client(conn, addr, shared_files):
    print(f"Connected by {addr}")
    data = conn.recv(1024).decode()
    command, filename = data.split(':')

    if command == "SEARCH":
        if filename in shared_files:
            conn.sendall(f"FOUND:{filename}:{addr}".encode())  
        else:
            conn.sendall("NOT_FOUND".encode())

    elif command == "GET":
        if filename in shared_files:
            with open(shared_files[filename], 'rb') as f:
                conn.sendall(f"FILE_SIZE:{os.path.getsize(shared_files[filename])}".encode())
                time.sleep(1)  
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    conn.sendall(chunk)
            print(f"File '{filename}' sent to {addr}")
        else:
            conn.sendall("FILE_NOT_FOUND".encode())

    conn.close()


def search_file(filename):
    for peer in PEERS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(peer)
                s.sendall(f"SEARCH:{filename}".encode())
                response = s.recv(1024).decode()

                if response.startswith("FOUND"):
                    _, found_filename, addr = response.split(':')
                    return peer

        except ConnectionRefusedError:
            print(f"Cannot connect to {peer}")

    print(f"File '{filename}' not found in the network.")
    return None  



def get_file(peer, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(peer)
        s.sendall(f"GET:{filename}".encode())
        response = s.recv(1024).decode()

        if response.startswith("FILE_SIZE"):
            _, size = response.split(':')
            print(f"Receiving file '{filename}' from {peer} of size {size} bytes...")
            with open(f"downloaded_{filename}", 'wb') as f:
                bytes_received = 0
                while bytes_received < int(size):
                    data = s.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    bytes_received += len(data)

            print(f"File '{filename}' downloaded successfully.")
        else:
            print("File not found on the peer.")

# Fungsi untuk mengirim file ke peer
def send_file(peer, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(peer)
        s.sendall(f"GET:{filename}".encode())  # Kirim permintaan untuk mengirim file
        response = s.recv(1024).decode()

        if response.startswith("ACCEPT"):
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    s.sendall(chunk)
            print(f"File '{filename}' sent to {peer}.")
        else:
            print("File transfer denied.")

# Fungsi utama untuk menjalankan node
def run_node(host, port):
    shared_files = scan_files()  # Pindai file yang tersedia di direktori lokal

    threading.Thread(target=run_server, args=(host, port, shared_files)).start()

    time.sleep(1)  # Tunggu sebentar agar server siap menerima koneksi

    # Interactive menu
    while True:
        print("\nMenu:")
        print("1. Search for a file")
        print("2. Download a file")
        print("3. Send a file to peer")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            filename = input("Enter the name of the file to search: ")
            search_file(filename)  # Call search function
        elif choice == '2':
            filename = input("Enter the name of the file to download: ")
            peer = search_file(filename)
            if peer:
                get_file(peer, filename)  # Download file from found peer
        elif choice == '3':
            filename = input("Enter the name of the file to send: ")
            target_ip = input("Enter the target IP: ")
            target_port = int(input("Enter the target port: "))
            send_file((target_ip, target_port), filename)  # Send file to target peer
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Jalankan node
if __name__ == "__main__":
    # Masukkan IP dan port dari node ini
        

    run_node('192.168.137.17', 4001)
