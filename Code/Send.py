# NASDAQ SoupBinTCP 3.00 protocol ITCH message sender
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file", help="The file to process")
args = parser.parse_args()
file = args.file

def debug(message):
    length = len(message).to_bytes(2, byteorder='big', signed=False)
    type = '+'.encode('ascii')
    message = message.encode('ascii')
    print(f'{length} {type} {message}')

def send(data):
    pass

def heartbeat():
    send(b'H')

def login_request(username, password, requested_session, requested_sequence_number):
    ## Will not be as secure as the real one
    pass

debug("Fuck YOU bitch ass")

exit()

with open(file, 'rb') as f:
    
    while True:
        # Read the message size (2 bytes)
        size_data = f.read(2)
        if not size_data:
            break

        # Convert the size to an integer
        message_size = int.from_bytes(size_data, byteorder='big', signed=False)

        # Read the message type (1 byte)
        #message_type = f.read(1).decode('ascii')

        # Read the rest of the message based on the size
        record = f.read(message_size)
        print(message_size, record)

        send(record)
