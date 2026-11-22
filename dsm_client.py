
# dsm_client.py

import json
import socket
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 6000


def send_request(request):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        client.connect((SERVER_HOST, SERVER_PORT))

        client.sendall(
            (json.dumps(request) + "\n").encode("utf-8")
        )

        data = b""

        while not data.endswith(b"\n"):

            chunk = client.recv(1024)

            if not chunk:
                break

            data += chunk

    return json.loads(data.decode("utf-8"))


def main():

    if len(sys.argv) < 2:

        print("Usage:")
        print("python dsm_client.py write 10")
        print("python dsm_client.py read")
        print("python dsm_client.py increment 5")

        return

    action = sys.argv[1].lower()

    try:

        if action == "write" and len(sys.argv) == 3:

            request = {
                "action": "write",
                "value": int(sys.argv[2])
            }

        elif action == "read":

            request = {
                "action": "read"
            }

        elif action == "increment":

            amount = int(sys.argv[2]) if len(sys.argv) > 2 else 1

            request = {
                "action": "increment",
                "amount": amount
            }

        else:

            print("Invalid command.")
            return

        response = send_request(request)

        if response["status"] == "success":

            print(response.get("message", "Operation successful"))
            print("Shared variable =", response["value"])

        else:

            print("Error:", response["message"])

    except ConnectionRefusedError:

        print("Connection failed. Start dsm_server.py first.")

    except (ValueError, OSError, json.JSONDecodeError) as error:

        print("Request failed:", error)


if __name__ == "__main__":
    main()
