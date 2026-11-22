# client.py
import socket

HOST = "127.0.0.1"  # Change to the server computer's IP for another computer
PORT = 5000

# Create a TCP socket using IPv4
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print("Connected to server.")

    while True:
        message = input("Client: ")
        client.sendall(message.encode("utf-8"))

        if message.lower() == "exit":
            break

        # Receive and display the server's reply
        reply = client.recv(1024).decode("utf-8")
        if not reply:
            print("Server disconnected.")
            break

        print("Server:", reply)

        if reply.lower() == "exit":
            break

print("Client closed.")
