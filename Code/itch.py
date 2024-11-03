import struct

# Define the mapping of message types to their lengths
m_map = {
    "s": 11,  # system messages, important to set start/stop timestamps
    "r": 38,  # stock directory
    "h": 24,  # stock trading action
    "y": 19,  # reg sho restriction
    "l": 25,  # market participant position
    "v": 34,  # mwcb decline level message
    "w": 11,  # mwcb status message
    "k": 27,  # ipo quoting period update
    "j": 34,  # luld auction collar
    "h": 20,  # operational halt
    "a": 35,  # added orders
    "f": 39,  # added orders with mpid attribution
    "e": 30,  # executed orders, linked to the previously added orders
    "c": 35,  # executed orders without linked added orders
    "x": 22,  # order cancel
    "d": 18,  # order delete
    "u": 34,  # modifications to added orders
    "p": 43,  # undisplayable non-cross orders executed
    "q": 39,  # cross trade_data
    "b": 18,  # broken trade
    "i": 49,  # noii message
    "n": 19   # rpii message
}

file = '../Data/01302019.NASDAQ_ITCH50'

def decodeTimestamp(timestamp):
    # Given a 6 byte integer, returns an 8 bit unsigned long long
    new_bytes = struct.pack('>2s6s', b'\x00\x00', timestamp)  # Add padding bytes
    new_timestamp = struct.unpack('>Q', new_bytes)
    return new_timestamp[0]

with open(file, 'rb') as f:
    while True:
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
        print(message_size, message_type, record)

        if message_type == "S":
            unpacked_data = struct.unpack('>HH6sc', record)
            if unpacked_data[3].decode() == "Q":  # Start of Market hours
                openTime = decodeTimestamp(unpacked_data[2])
                print("Market opened at %d nanoseconds: " % openTime)
                import time
                time.sleep(5)
            elif unpacked_data[3].decode() == "M":  # End of Market hours
                endTime = decodeTimestamp(unpacked_data[2])
                print("Market closed at %d nanoseconds: " % endTime)
                import time
                time.sleep(5)