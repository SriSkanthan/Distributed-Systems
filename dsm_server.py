
# dsm_server.py
import json
import socket
import threading

HOST = "0.0.0.0"
PORT = 6000

shared_value = None
value_lock = threading.Lock()


def handle_client(conn, addr):
    global shared_value

    print("Connected:", addr)

    with conn:
        data = b""

        while not data.endswith(b"\n"):
            chunk = conn.recv(1024)

            if not chunk:
                return

            data += chunk

        try:
            request = json.loads(data.decode("utf-8"))
            action = request.get("action")

            with value_lock:

                if action == "write":
                    shared_value = int(request["value"])

                    response = {
                        "status": "success",
                        "message": "Shared value written",
                        "value": shared_value
                    }

                elif action == "read":

                    if shared_value is None:
                        response = {
                            "status": "error",
                            "message": "Variable not initialized"
                        }
                    else:
                        response = {
                            "status": "success",
                            "value": shared_value
                        }

                elif action == "increment":

                    if shared_value is None:
                        response = {
                            "status": "error",
                            "message": "Variable not initialized"
                        }
                    else:
                        amount = int(request.get("amount", 1))
                        shared_value += amount

                        response = {
                            "status": "success",
                            "message": "Shared value incremented",
                            "value": shared_value
                        }

                else:
                    response = {
                        "status": "error",
                        "message": "Unknown action"
                    }

            conn.sendall(
                (json.dumps(response) + "\n").encode("utf-8")
            )

            print("Request:", action, "| Response:", response)

        except (ValueError, KeyError, json.JSONDecodeError) as error:

            response = {
                "status": "error",
                "message": str(error)
            }

            conn.sendall(
                (json.dumps(response) + "\n").encode("utf-8")
            )


def main():

    print("Distributed Shared Memory (DSM) Server")
    print(f"Listening on {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        while True:

            conn, addr = server.accept()

            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()


if __name__ == "__main__":
    main()
