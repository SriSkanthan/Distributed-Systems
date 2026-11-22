# peer_client.py
import json
import socket

SERVER_HOST = "127.0.0.1"  # Use the server computer's IP on a different computer
SERVER_PORT = 5001

def request_file_list():
    """Connect to the peer server and request its current file listing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, SERVER_PORT))
        client.sendall(b"LIST")

        # Read until the server closes its connection.
        chunks = []
        while True:
            data = client.recv(4096)
            if not data:
                break
            chunks.append(data)

    response_text = b"".join(chunks).decode("utf-8")
    return json.loads(response_text)

def main():
    print("Connecting to peer file-listing server...")
    try:
        response = request_file_list()

        if response.get("status") != "success":
            print("Error:", response.get("message", "Unknown error"))
            return

        print("\nFiles available on the peer:")
        print("Shared folder:", response["folder"])
        files = response["files"]

        if not files:
            print("No files found in the shared folder.")
        else:
            print(f"{'File name':<35} {'Size (bytes)':>12}")
            print("-" * 49)
            for item in files:
                print(f"{item['name']:<35} {item['size_bytes']:>12}")

            print(f"\nTotal files: {len(files)}")

    except ConnectionRefusedError:
        print("Could not connect. Make sure peer_server.py is running.")
    except json.JSONDecodeError:
        print("The server returned an invalid response.")
    except OSError as error:
        print("Network error:", error)

if __name__ == "__main__":
    main()
