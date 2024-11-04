#Shorten a sample ITCH file to 1GB to allow storage on GitHub

#mega_byte = 1024 * 1024
#giga_byte = 1024 * mega_byte
giga_byte = 1000000000

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file", help="The file to process")
args = parser.parse_args()
file = args.file

total_bytes = 0

new = open('Gigabit.NASDAQ_ITCH50', 'wb')

with open(file, 'rb') as f:
    while total_bytes < giga_byte:
        # Read the message size (2 bytes)
        size_data = f.read(2)
        if not size_data:
            break

        # Convert the size to an integer
        message_size = int.from_bytes(size_data, byteorder='big', signed=False)

        # Read the message type (1 byte)
        message_type = f.read(1).decode('ascii')

        # Read the rest of the message based on the size
        record = f.read(message_size - 1)
        #print(message_size, message_type, record)

        new.write(size_data + message_type.encode('ascii') + record)

        total_bytes += 2 + 1 + len(record)
        print(f'\r{total_bytes}/{giga_byte}: {total_bytes/giga_byte*100:.2f}%', end='')
