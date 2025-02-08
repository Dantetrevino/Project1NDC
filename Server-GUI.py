import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def SWAP_Server(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def Sort_TAM_Server(arr):
    low, mid, high = 0, 0, len(arr) - 1
    while mid <= high:
        if arr[mid] == 'T':
            SWAP_Server(arr, low, mid)
            low, mid = low + 1, mid + 1
        elif arr[mid] == 'A':
            mid += 1
        else:
            SWAP_Server(arr, mid, high)
            high -= 1

def handle_client(conn, addr, log):
    with conn:
        log.insert(tk.END, f"Connected by {addr}\n")
        data = conn.recv(1024).decode().strip('#')
        array = list(data)
        Sort_TAM_Server(array)
        conn.sendall(''.join(array).encode())
        log.insert(tk.END, f"Sorted data sent back to {addr}\n")

def server(log):
    host = 'localhost'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        log.insert(tk.END, "Server is listening...\n")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr, log)).start()

def start_server(log):
    threading.Thread(target=server, args=(log,), daemon=True).start()

def create_server_gui():
    root = tk.Tk()
    root.title("Server")
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    log = scrolledtext.ScrolledText(frame, width=60, height=20)
    log.pack(pady=10)
    
    start_button = tk.Button(frame, text="Start Server", command=lambda: start_server(log))
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_server_gui()
