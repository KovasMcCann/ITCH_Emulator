## project:
# Create a converter to convert itch data to SoupBinTCP format
# Create a parser to read the SoupBinTCP format
## References
# https://www.nyse.com/publicdocs/nyse/data/Daily_TAQ_Client_Spec_v3.0.pdf
# https://www.nyse.com/publicdocs/nyse/data/Daily_TAQ_ArcaBook_Client_Spec_v2.0.pdf
# https://www.nyse.com/publicdocs/nyse/data/Daily_TAQ_NASDAQ_Client_Spec_v2.2.pdf
# https://www.nyse.com/publicdocs/nyse/data/Daily_TAQ_NASDAQ_OMX_Client_Spec_v1.2.pdf
# https://www.nyse.com/publicdocs/nyse/data/Daily_TAQ_NYSE_Client_Spec_v2.0.pdf
# https://www.nyse.com/publicdocs/nyse/data/Daily_TAQ_NYSE_Arca_Client_Spec_v2.0.pdf

# https://wiki.wireshark.org/SoupBinTCP
# also setup wireshark to monitor the packets

"""
import scapy

##SoupBinTCP
class Disney(Packet):
    name = "DisneyPacket "
    fields_desc=[ ShortField("mickey",5),
                 XByteField("minnie",3) ,
                 IntEnumField("donald" , 1 ,
                      { 1: "happy", 2: "cool" , 3: "angry" } ) ]
    
#prase the packet
"""

import os

# This defines the message types and their lengths
m_map = {
    "S": 11,  # System messages, important to set start/stop timestamps
    "R": 38,  # Stock Directory, use to set keys in map of stocks map
    "H": 24,  # Stock Trading Action
    "Y": 19,  # Reg SHO Restriction
    "L": 25,  # Market Participant Position
    "V": 34,  # MWCB Decline Level Message
    "W": 11,  # MWCB Status Message
    "K": 27,  # IPO Quoting Period Update
    "J": 34,  # LULD Auction Collar
    "h": 20,  # Operational Halt
    "A": 35,  # Added orders
    "F": 39,  # Added orders with MPID Attribution
    "E": 30,  # Executed orders, linked to the previously added orders
    "C": 35,  # Executed orders without linked added orders
    "X": 22,  # Order Cancel
    "D": 18,  # Order Delete
    "U": 34,  # Modifications to added orders
    "P": 43,  # Undisplayable non-cross orders executed
    "Q": 39,  # Cross Trade
    "B": 18,  # Broken Trade
    "I": 49,  # NOII message
    "N": 19   # RPII message
}

# Define the path to the binary file
file_name = "../Data/01302019.NASDAQ_ITCH50"

data = open(os.path.join(file_name), 'rb') #sets to ready binary

# Read the message header
msg_header = data.read(1) #Does this need to be 0?  # Reads one byte
print(msg_header)

if msg_header == b"S":
    print("System Event Message")
    msg_type = "S"
    msg_len = m_map[msg_type]
    msg_data = data.read(msg_len - 1)
    print(msg_data)

# Close the binary file after reading
data.close()
