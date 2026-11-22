# peer_server.py
import json
import os
import socket
import sys

HOST = "0.0.0.0"
PORT = 5001

def get_file_listing(folder_path):
    """Return actual files in the requested folder (not dummy/sample data)."""
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"Folder does not exist: {folder_path}")

    files = []
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file():
                info = entry.stat()
                files.append({
                    "name": entry.name,
                    "size_bytes": info.st_size
                })

    return sorted(files, key=lambda item: item["name"].lower())

def main():
    # Folder to share can be supplied as a command-line argument.
    # If omitted, the server shares the "shared_files" folder beside this script.
    default_folder = os.path.join(os.path.dirname(__file__), "shared_files")
    folder_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else default_folder

    if not os.path.isdir(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created folder: {folder_path}")

    print(f"Sharing files from: {folder_path}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Peer file-listing server is listening on port {PORT}...")

        while True:
            conn, address = server.accept()
            with conn:
                print(f"Client connected: {address}")
                request = conn.recv(1024).decode("utf-8").strip()

                if request.upper() == "LIST":
                    try:
                        file_list = get_file_listing(folder_path)
                        response = {
                            "status": "success",
                            "folder": folder_path,
                            "files": file_list
                        }
                    except (OSError, NotADirectoryError) as error:
                        response = {"status": "error", "message": str(error)}

                    conn.sendall((json.dumps(response) + "\n").encode("utf-8"))
                    print(f"Sent {len(response.get('files', []))} file(s) to {address}.")
                else:
                    response = {"status": "error", "message": "Unknown request. Send LIST."}
                    conn.sendall((json.dumps(response) + "\n").encode("utf-8"))

if __name__ == "__main__":
    main()
