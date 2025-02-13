# server.py
import socket
import threading
import os
from datetime import datetime


class ImageServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.save_dir = 'received_images'

        # Create save directory if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        # Initialize server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, address):
        """Handle individual client connections"""
        print(f"Connected to client: {address}")

        try:
            # Receive image size first
            size_data = client_socket.recv(8)
            if not size_data:
                return

            image_size = int(size_data.decode().strip())
            print(f"Expecting image of size: {image_size} bytes")

            # Receive the image data
            received_data = b""
            while len(received_data) < image_size:
                chunk = client_socket.recv(min(4096, image_size - len(received_data)))
                if not chunk:
                    break
                received_data += chunk

            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.jpg"
            filepath = os.path.join(self.save_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(received_data)

            # Send response back to client
            response = f"Image received and saved as {filename}. Size: {len(received_data)} bytes"
            client_socket.send(response.encode())

            print(f"Saved image from {address} as {filename}")

        except Exception as e:
            error_msg = f"Error handling client {address}: {str(e)}"
            print(error_msg)
            try:
                client_socket.send(error_msg.encode())
            except:
                pass

        finally:
            client_socket.close()
            print(f"Connection closed with {address}")

    def start(self):
        """Start the server and listen for connections"""
        print("Server started. Waiting for connections...")
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                # Handle each client in a separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()

        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            self.server_socket.close()


def main():
    server = ImageServer()
    server.start()


if __name__ == "__main__":
    main()