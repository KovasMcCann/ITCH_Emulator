import socket
import struct
import threading


class SoupBinTCPServer:
    def __init__(self, host='127.0.0.1', port=34566):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, address):
        print(f"Connection established with {address}")
        try:
            while True:
                header = client_socket.recv(2)
                if len(header) < 2:
                    print("Client disconnected")
                    break

                packet_length = struct.unpack('!H', header)[0]
                payload = client_socket.recv(packet_length)

                if not payload:
                    break

                message_type = chr(payload[0])
                message_data = payload[1:].decode(errors='replace')

                print(f"Received message: Type='{message_type}', Data='{message_data}'")

                if message_type == 'L':
                    self.send_packet(client_socket, 'A', "Login Successful")
                    self.stream_file_data(client_socket)
                elif message_type == 'O':
                    self.send_packet(client_socket, 'O', "Logout Successful")
                    break
                else:
                    self.send_packet(client_socket, 'U', "Unknown Request")
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection closed with {address}")

    def send_packet(self, client_socket, message_type, payload):
        # If payload is a string, encode it; if it's bytes, use it directly
        if isinstance(payload, str):
            payload_data = message_type.encode() + payload.encode()
        elif isinstance(payload, bytes):
            payload_data = message_type.encode() + payload
        else:
            raise ValueError("Payload must be either a string or bytes")

        # Pack the length and send the packet
        packet_length = len(payload_data)
        packet = struct.pack(f'!H{packet_length}s', packet_length, payload_data)
        client_socket.sendall(packet)


    def stream_file_data(self, client_socket):
        try:
            with open('Gigabit.NASDAQ_ITCH50', 'rb') as f:
                while True:
                    size_data = f.read(2)
                    if not size_data or len(size_data) != 2:
                        break

                    message_size = int.from_bytes(size_data, byteorder='big')
                    message_type_data = f.read(1)
                    if not message_type_data:
                        break

                    message_type = message_type_data.decode('ascii', errors='replace')
                    record_data = f.read(message_size - 1)

                    if len(record_data) != (message_size - 1):
                        break

                    self.send_packet(client_socket, 'S', message_type_data + record_data)
        except FileNotFoundError:
            print("File not found: Gigabit.NASDAQ_ITCH50")
        except Exception as e:
            print(f"Error streaming file data: {e}")

    def start(self):
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, address)).start()
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    server = SoupBinTCPServer()
    server.start()
