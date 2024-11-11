import socket
import struct


class SoupBinTCPClient:
    def __init__(self, host='127.0.0.1', port=34566):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_packet(self, message_type, payload):
        payload_data = message_type.encode() + payload.encode()
        packet_length = len(payload_data)
        
        # Pack the packet length and payload
        packet = struct.pack(f'!H{packet_length}s', packet_length, payload_data)
        self.sock.sendall(packet)
        print(f"Sent packet: Type='{message_type}', Payload='{payload}'")

    def receive_packet(self):
        try:
            header = self.sock.recv(2)
            if len(header) < 2:
                print("No response or server closed connection")
                return None
            
            packet_length = struct.unpack('!H', header)[0]
            data = self.sock.recv(packet_length)
            
            if not data:
                print("No data received")
                return None

            return data
        except Exception as e:
            print(f"Error receiving packet: {e}")
            return None

    def receive_stream(self):
        print("Receiving streamed data...")
        try:
            while True:
                data = self.receive_packet()
                if not data:
                    break

                message_type = chr(data[0])
                message_content = data[1:]
                
                print(f"Streamed Packet: Type='{message_type}', Content={message_content}")
        except KeyboardInterrupt:
            print("Stream receiving interrupted")
        except Exception as e:
            print(f"Error receiving stream: {e}")

    def close(self):
        self.sock.close()
        print("Connection closed")


if __name__ == "__main__":
    client = SoupBinTCPClient()

    try:
        client.connect()
        client.send_packet('L', "user\0password\0")
        
        response = client.receive_packet()
        if response:
            print(f"Received response: {response.decode(errors='replace')}")

        client.receive_stream()

    finally:
        client.close()
