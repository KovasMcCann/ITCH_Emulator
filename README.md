[Screen recording 2024-11-11 2.51.36 PM.webm](https://github.com/user-attachments/assets/a612829e-a5e0-4ce7-af3d-cf7475a3ac4f)

# How to work with NASDAQ ITCH protocol

## Reciving Sample Data

To receive **Free** sample data from NASDAQ use this [link](https://emi.nasdaq.com/ITCH/Nasdaq%20ITCH/).

## Accessing Sample Data

The ITCH tick data comes in binary format. For a basic Python implementation use [`struct`](https://docs.python.org/3/library/struct.html)
> This module converts Python values to and from C structs represented as Python bytes objects, enabling the handling of binary data from files or network connections. It uses Format Strings to describe the layout of C structs and facilitate conversions with Python values.

**For high-performance applications it's best to use C as binary data manipulation is built in.**

### Message Types

The ITCH protocol has 11 main message types. The first byte of each message indicates the message type. The message types are as follows:

- `A` - Add Order
- `F` - Add Order with [MPID Attribution](https://www.finra.org/filing-reporting/trace/depository-institutions-mpids)
- `E` - Order Executed
- `C` - Order Executed with Price
- `X` - Order Cancel
- `D` - Order Delete
- `U` - Order Replace
- `P` - Trade
- `Q` - Cross Trade
- `B` - Broken Trade
- `I` - [NOII](https://www.investopedia.com/terms/n/net-order-imbalance-indicator-noii.asp)

## How the code works

### Key Features
1. **Message Mapping (`m_map`)**
   - Maps ITCH message types (e.g., `s`, `r`, `a`) to their respective lengths.
2. **Utility Functions**
   - `decodeTimestamp`: Converts a 6-byte timestamp into an 8-byte unsigned integer.
   - `nanosecondsToTime`: Converts nanoseconds to a human-readable time format (UTC).
3. **Dictionaries**
   - `MarketCategory`: Maps market identifiers (e.g., `Q`) to their full names (e.g., NASDAQ Global Select Market).
   - `Action`: Maps trading action codes (e.g., `H`, `P`) to their corresponding states.
   - `StockDirectory`: Tracks stock locates (IDs) and their associated tickers.

---

### **File Reading**
- Each message consists of:
  1. A 2-byte message size.
  2. A 1-byte message type.
  3. Message-specific data.
- The script processes the binary file iteratively, ensuring proper alignment.

### **Message Decoding**
- The `struct` module unpacks binary data based on the message type.
- Examples:
  - **System Event Messages (`S`)**:
    ```python
    unpacked_data = struct.unpack('>HH6sc', record)
    ```
    Fields include timestamps and event codes. Event types are mapped to actions like "Market Opened" or "System Stopped."
  - **Stock Directory Messages (`R`)**:
    ```python
    data = struct.unpack('>HH6s8sccIcc2scccccIc', record)
    ```
    Provides metadata such as ticker, market category, lot size, and restrictions.
  - **Add Orders (`A`)**:
    ```python
    data = struct.unpack('>HH6sQcI8sI', record)
    ```
    Includes order reference number, stock, price, and whether it's a buy (`B`) or sell (`S`).

### **Output**
- Decoded data is printed in a human-readable format, including timestamps, stock tickers, order details, and market actions.

---

## Important Details

1. **Endian-ness**
   - Binary data uses **big-endian** encoding (`>` in `struct.unpack`).

2. **Timestamp Decoding**
   - ITCH timestamps are in **nanoseconds since midnight UTC**.

3. **Data Length Validation**
   - The length of each message is validated to avoid misaligned parsing.

4. **Duplicate Message Type**
   - `m_map` contains two entries for `h` with different lengths (`24` and `20`). This redundancy may indicate an oversight or protocol update.

5. **Stock Mapping**
   - The `StockDirectory` ensures stock locates are resolved to tickers for later messages.

6. **Price Precision** 
   - Prices are stored in **1/10,000 units** and converted to floating-point values. See [investopedia.com](https://www.investopedia.com/terms/d/decimalization.asp) for interesting information.

7. **Scalability**
   - The `while` loop processes messages until EOF, making it suitable for large data streams.

---

## Example Output

For a message with type `A` (Add Order):

```
14:23:45: Order 123456 for 100 shares of AAPL at 150.25 B
```
