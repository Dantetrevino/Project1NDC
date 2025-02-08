import socket
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

def connect_to_server(data, log):
    host = 'localhost'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data.encode())
        result = s.recv(1024).decode()
        log.insert(tk.END, f"Sorted Array: {result}\n")

def send_data(entry, log):
    data = entry.get()
    if data.endswith('#'):
        connect_to_server(data.strip('#'), log)
    else:
        messagebox.showerror("Error", "Input must end with '#'")

def create_client_gui():
    root = tk.Tk()
    root.title("Client")
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    entry = tk.Entry(frame, width=50)
    entry.pack(pady=10)

    send_button = tk.Button(frame, text="Send Data", command=lambda: send_data(entry, log))
    send_button.pack(pady=10)

    log = scrolledtext.ScrolledText(frame, width=60, height=10)
    log.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_client_gui()
