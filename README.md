# How to work with NASDAQ ITCH protocol

## Reciving Sample Data

To receive **Free** sample data from NASDAQ use this [link](https://emi.nasdaq.com/ITCH/Nasdaq%20ITCH/).

## Accessing Smaple Data

The ITCH tick data comes in binary format. For a basic python implementation use [`struct`](https://docs.python.org/3/library/struct.html)
> This module converts Python values to and from C structs represented as Python bytes objects, enabling the handling of binary data from files or network connections. It uses Format Strings to describe the layout of C structs and facilitate conversions with Python values.

**For high performance applications its best to use C as binary data manipulation is built in.**

### Message Types

The ITCH protocol has 11 message types. The first byte of each message indicates the message type. The message types are as follows:

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

### Message Structure

The ITCH message structure is as follows:

- `Message Type` - 1 byte
- `Stock Locator` - 4 bytes
- `Tracking Number` - 2 bytes
- `Timestamp` - 6 bytes
- `Order Reference Number` - 8 bytes
- `Buy/Sell Indicator` - 1 byte
- `Shares` - 4 bytes
- `Stock` - 8 bytes
- `Price

Once you have the sample data you need to define what strings to format. This is because the parser uses format strings according to the following formats dictionaries.

```python
#import micropip

# Install pandas if necessary
#await micropip.install("pandas")

import pandas as pd

# Read the Excel file without the encoding parameter
message_data = (pd.read_excel('/home/wire/Obsidian/Courses 🧑‍🎓/ML-for-Algo-Trading/Book/Chapter02/01_NASDAQ_TotalView-ITCH_Order_Book/message_types.xlsx',
                              sheet_name='messages')
                .sort_values('id')
                .drop('id', axis=1))

def clean_message_types(df):
    df.columns = [c.lower().strip() for c in df.columns]
    df.value = df.value.str.strip()
    df.name = (df.name
               .str.strip()  # remove whitespace
               .str.lower()
               .str.replace(' ', '_')
               .str.replace('-', '_')
               .str.replace('/', '_'))
    df.notes = df.notes.str.strip()
    df['message_type'] = df.loc[df.name == 'message_type', 'value']
    return df

# Clean the message types
message_types = clean_message_types(message_data)

message_labels = (message_types.loc[:, ['message_type', 'notes']]
                  .dropna()
                  .rename(columns={'notes': 'name'}))
message_labels.name = (message_labels.name
                       .str.lower()
                       .str.replace('message', '')
                       .str.replace('.', '')
                       .str.strip()
                       .str.replace(' ', '_'))

# Optionally save to CSV
# message_labels.to_csv('message_labels.csv', index=False)

# Display the first few rows
print(message_labels.head())

```