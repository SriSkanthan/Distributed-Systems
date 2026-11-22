# server.py
import socket

HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 5000

# Create a TCP socket using IPv4
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server is waiting for a client on port {PORT}...")

    conn, addr = server.accept()
    with conn:
        print("Connected to:", addr)

        while True:
            message = conn.recv(1024).decode("utf-8")

            # Stop if the client disconnects or sends "exit"
            if not message or message.lower() == "exit":
                print("Client disconnected.")
                break

            print("Client:", message)

            # Read a reply from the server user and send it to the client
            reply = input("Server: ")
            conn.sendall(reply.encode("utf-8"))

            if reply.lower() == "exit":
                break

print("Server closed.")
