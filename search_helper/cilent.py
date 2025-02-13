# client.py
import socket
import os


class ImageClient:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port

    def send_image(self, image_path):
        """Send an image to the server and get response"""
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # Create socket and connect to server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))

            # Read the image file
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # Send image size first
            size_msg = f"{len(image_data):08d}"
            client_socket.send(size_msg.encode())

            # Send image data
            client_socket.sendall(image_data)

            # Get response from server
            response = client_socket.recv(1024).decode()
            print("Server response:", response)

            return response

        except Exception as e:
            print(f"Error: {str(e)}")
            return str(e)

        finally:
            client_socket.close()


def main():
    client = ImageClient()

    # Example usage
    image_path = input("Enter the path to the image file: ")
    client.send_image(image_path)


if __name__ == "__main__":
    main()