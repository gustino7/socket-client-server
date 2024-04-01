import os
import socket
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Client:
    # TODO:
    def __init__(self, host, port):
        # 1. Define host and port
        # 2. Create a socket
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        # 3. Connect to the server
        self.socket.connect((self.host, self.port))

    def send_message(self, message):
        # 4. Send a message to the server
        message = message.encode('utf-8')
        self.socket.send(message)
        
        # 5. Receive a response from the server and return it
        response = self.socket.recv(1024)
        response = response.decode('utf-8')

        return response

    def recv(self, size):
        # 6. Receive data from the server and return it
        return self.socket.recv(size)

    def disconnect(self):
        # 7. Close the connection
        self.socket.close()

    def parse_header(self, header):
        # 8. Parse the header and return the file name and size
        filename, size = header.split(',')
        filename = filename.split(":")[1].strip()
        size = size.split(":")[1].strip
        return filename, int(size)


if __name__ == "__main__":
    # TODO:
    # 1. Create a Client object
    client = Client('127.0.0.1', 65432)
    # 2. Connect to the server
    client.connect()

    # 3. Send a message to the server and receive a response
    message = input("Enter a message: ")
    status = client.send_message(message)

    # 4. Check if the response isn't a header
    # 4.1 If it is, print the response and exit
    if "file-name" not in status and "file-size:" not in status:
        print(status)
        exit()

    # 5. Parse the header
    file_name, file_size = client.parse_header(status)
    file_path = os.path.join(BASE_DIR, "files", file_name)

    # 6. Receive the file from the server and save it
    with open(file_path, "wb") as f:
        while True:
            data = client.recv(min(1024, file_size))
            if not data:
                break
            f.write(data)
            file_size -= len(data)

    # 7. Close the connection
    client.disconnect()
