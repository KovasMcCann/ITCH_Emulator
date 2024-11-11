[Screen recording 2024-11-11 2.51.36 PM.webm](https://github.com/user-attachments/assets/a612829e-a5e0-4ce7-af3d-cf7475a3ac4f)

# How to work with NASDAQ ITCH protocol

## Reciving Sample Data

To receive **Free** sample data from NASDAQ use this [link](https://emi.nasdaq.com/ITCH/Nasdaq%20ITCH/).

## Accessing Smaple Data

The ITCH tick data comes in binary format. For a basic python implementation use [`struct`](https://docs.python.org/3/library/struct.html)
> This module converts Python values to and from C structs represented as Python bytes objects, enabling the handling of binary data from files or network connections. It uses Format Strings to describe the layout of C structs and facilitate conversions with Python values.

**For high performance applications its best to use C as binary data manipulation is built in.**

### Message Types

The ITCH protocol has 11 main message types. The first byte of each message indicates the message type. The message types are as follows:

- `A` - Add Order
- `F` - Add Order MPID Attribution
- `E` - Order Executed
- `C` - Order Executed with Price
- `X` - Order Cancel
- `D` - Order Delete
- `U` - Order Replace
- `P` - Trade
- `Q` - Cross Trade
- `B` - Broken Trade
- `I` - NOII
