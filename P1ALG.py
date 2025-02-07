import socket
import os

# Server Code
def server():
    host = "127.0.0.1"  # Localhost
    port = 8080  # Port number for communication
    
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        
        filename = client_socket.recv(1024).decode()
        print(f"Client requested file: {filename}")
        
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                data = file.read()
                client_socket.sendall(data)
            print("File sent successfully!")
        else:
            client_socket.send(b"File not found")
            print("File not found")
        
        client_socket.close()
    
    server_socket.close()

# Client Code
def client(filename):
    host = "127.0.0.1"
    port = 8080
    
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Send filename to server
    client_socket.send(filename.encode())
    
    # Receive file data
    data = client_socket.recv(4096)
    if data == b"File not found":
        print("File not found on server")
    else:
        with open(f"received_{filename}", "wb") as file:
            file.write(data)
        print("File received successfully!")
    
    client_socket.close()

# Main function
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py <server|client> [filename]")
        sys.exit(1)
    
    if sys.argv[1] == "server":
        server()
    elif sys.argv[1] == "client" and len(sys.argv) == 3:
        client(sys.argv[2])
    else:
        print("Invalid usage.")
        sys.exit(1)

#first terminal put python P1ALG.py serve
# second terminal put python P1ALG.py client example.txt
# it will display a duplicated file on the side