# NASDAQ ITCH 5.0 Parser

import struct
import datetime

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

MarketCategory = { # For Stock Directory Messages
    "Q": "NASDAQ Global Select Market",
    "G": "NASDAQ Global Market",
    "S": "NASDAQ Capital Market",
    "N": "New York Stock Exchange",
    "A": "NYSE MKT",
    "P": "NYSE Arca",
    "Z": "BATS Global Markets",
    "V": "Investors Exchange",
    " ": "Not Available"
}

Action = {
    "H": "Trading Halted",
    "P": "Trading Paused",
    "Q": "Quotation Only Period",
    "T": "Trading Resumed"
}

def decodeTimestamp(timestamp):
    # Given a 6 byte integer, returns an 8 bit unsigned long long
    new_bytes = struct.pack('>2s6s', b'\x00\x00', timestamp)  # Add padding bytes
    new_timestamp = struct.unpack('>Q', new_bytes)
    return new_timestamp[0]

def nanosecondsToTime(nanoseconds):
    return datetime.datetime.utcfromtimestamp(nanoseconds/1e9).strftime('%H:%M:%S')


#file = '../Data/01302019.NASDAQ_ITCH50'

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file", help="The file to process")
args = parser.parse_args()
file = args.file

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
        #print(message_size, message_type, record)

        if message_type == "S": # System Event Messages
            unpacked_data = struct.unpack('>HH6sc', record)
            #print(unpacked_data)
            if unpacked_data[3].decode() == "Q":  # Start of Market hours
                openTime = decodeTimestamp(unpacked_data[2])
                print(f"{nanosecondsToTime(openTime)}: Market Opened")

            elif unpacked_data[3].decode() == "M":  # End of Market hours
                endTime = decodeTimestamp(unpacked_data[2])
                print(f"{nanosecondsToTime(endTime)}: Market closed")

            elif unpacked_data[3].decode() == "S": # Start of System Hours 
                openTime = decodeTimestamp(unpacked_data[2])
                print(f"{nanosecondsToTime(openTime)}: System Started")

            elif unpacked_data[3].decode() == "E": # End of System Hours
                endTime = decodeTimestamp(unpacked_data[2])
                print(f"{nanosecondsToTime(endTime)}: System Stopped")

            elif unpacked_data[3].decode() == "O": # Start of Messages
                openTime = decodeTimestamp(unpacked_data[2])
                print(f"{nanosecondsToTime(openTime)}: Start of Messages")

            elif unpacked_data[3].decode() == "C": # End of Messages
                endTime = decodeTimestamp(unpacked_data[2])
                print(f"{nanosecondsToTime(endTime)}: End of Messages")

        elif message_type == "R": # Stock Directory Messages
            data = struct.unpack('>HH6s8sccIcc2scccccIc', record)
            #print(data)

            locate = data[0]
            tracker = data[1] #Always 0
            timestamp = decodeTimestamp(data[2])
            ticker = data[3].decode().strip()
            market = MarketCategory[data[4].decode()]
            status = data[5].decode()
            lotSize = data[6]
            restrictions = data[7].decode()
            issueclass = data[8].decode()
            issueSubType = data[9].decode()
            authenticity = data[10].decode()
            shortSaleThreshold = data[11].decode()
            IPOflag = data[12].decode()
            LULDRefPriceTier = data[13].decode()
            ETPTier = data[14].decode()
            ETPleverageFactor = data[15]
            inverseIndicator = data[16].decode()

            #print(f"{locate} {tracker} {nanosecondsToTime(timestamp)} {ticker} {market} {status} {lotSize} {restrictions} {issueclass} {issueSubType} {authenticity} {shortSaleThreshold} {IPOflag} {LULDRefPriceTier} {ETPTier} {ETPleverageFactor} {inverseIndicator}")

            print(f"{nanosecondsToTime(timestamp)}: Stock {ticker} on {market} assigned {locate}")
            #stock_map[stockID] = ticker

        if message_type == "H": # Stock Trading Action Messages
            data = struct.unpack('>HH6s8scIc', record)
            locate = data[0]
            tracker = data[1]
            timestamp = decodeTimestamp(data[2])
            ticker = data[3].decode().strip()
            #ticker = data[3]
            tradingState = data[4].decode()
            StateValuesSimple = Action[data[4].decode()]
            reserved = data[5]
            reason = data[6]
            print(f"{nanosecondsToTime(timestamp)}: Stock {ticker} {StateValuesSimple}")

        if message_type == "A": # Add Orders
            data = struct.unpack('>HH6sQcI8sI', record)
            locate = data[0]
            tracker = data[1]
            timestamp = decodeTimestamp(data[2])
            orderRefNum = data[3]
            buySell = data[4].decode()
            shares = data[5]
            stock = data[6].decode().strip()
            price = data[7]

            print(f"{nanosecondsToTime(timestamp)}: Order {orderRefNum} for {shares} shares of {stock} at {price} {buySell}")

        import time
        #time.sleep(0.01)