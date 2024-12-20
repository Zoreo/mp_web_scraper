
# Project Documentation: Multithreaded Web Scraper and Server

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Implementation Details](#implementation-details)
  - [Web Scraping](#web-scraping)
  - [Selectors](#selectors)
  - [Multithreading](#multithreading)
  - [Server Functions](#server-functions)
  - [Client Functions](#client-functions)
- [Diagrams](#diagrams)
- [How to Run](#how-to-run)
- [Future Improvements](#future-improvements)

## Overview
This project is a multithreaded web scraping server implemented in Python. It allows clients to request product information from the DM Drogerie Markt Bulgaria website, specifically targeting hair care products. The server processes multiple client requests concurrently using multithreading and an event-driven architecture with the `selectors` module.

## Features
1. **Web Scraping**:
   - Scrapes product names and prices from the specified URL using Selenium.
   - Extracts and sorts products by price in ascending order.
   
2. **Multithreaded Server**:
   - Handles multiple client requests simultaneously using threads for blocking tasks.
   - Uses the `selectors` module for efficient connection management.

3. **Client Interaction**:
   - Clients can request a specific number of products, and the server responds with the requested information.
   - Clients can continue querying or exit the session.

## Implementation Details

### **Web Scraping**
The `fetch_dm_products` function uses Selenium to automate the scraping process. Key steps include:
1. Navigating to the target URL.
2. Waiting for the product list to load using `WebDriverWait`.
3. Extracting product names and prices using CSS selectors.
4. Cleaning and processing the extracted data.
5. Sorting the products by price.

### **Selectors**
- CSS selectors are used to locate HTML elements for product names and prices.
- **Name Selector**: `#product-tiles div.pdd_14u321i8 div:nth-child(3) > a`
  - Locates the anchor tags containing product names within the product tiles.
- **Price Selector**: `div.pdd_14u321i8 > div:nth-child(2) > div > div > span > span`
  - Extracts the price details from the corresponding product tile.

### **Multithreading**
- The server uses the `selectors` module for event-driven, non-blocking I/O.
- When a blocking task like web scraping is needed, it is offloaded to a separate thread using `threading.Thread`.
- **Why Multithreading?**
  - Selenium operations are inherently blocking. Without multithreading, the server would handle only one client at a time.
  - By delegating blocking tasks to threads, the server loop remains free to handle other client connections, improving responsiveness and scalability.

### Server Functions
- **`main()`**
  - Initializes and starts the server.
- **`start_server(host, port)`**
  - Starts the multithreaded server on the specified host and port.
  - **Inputs**: `host` (string), `port` (integer).
  - **Outputs**: None.
- **`accept_wrapper(sock)`**
  - Accepts new client connections and registers them with the selector.
  - **Inputs**: `sock` (socket object).
  - **Outputs**: None.
- **`service_connection(key, mask)`**
  - Handles active client connections and spawns threads for blocking operations.
  - **Inputs**: `key` (selector key), `mask` (event mask).
  - **Outputs**: None.
- **`handle_client(sock, data)`**
  - Processes client requests, fetches data, and sends responses.
  - **Inputs**: `sock` (client socket), `data` (connection-specific data).
  - **Outputs**: None.
- **`fetch_dm_products()`**
  - Scrapes product names and prices from the specified website and sorts them by price.
  - **Inputs**: None.
  - **Outputs**: List of dictionaries containing product names and prices.

### Client Functions
- **`main()`**
  - Handles client-side operations, including connecting to the server and managing input/output.
- **`clear_terminal()`**
  - Clears the terminal screen for a clean user interface.
- **`client_handler(sock)`**
  - Manages communication with the server, including sending and receiving messages.

## Diagrams
The diagrams provide an architectural overview of the server and its multithreaded capabilities, as well as the client-server interaction flow.

### Architecture Diagram
```plaintext
+----------------------+
|      Client 1        |
+----------------------+
          |
+----------------------+
|      Client 2        |
+----------------------+
          |
+----------------------+
|   Multithreaded      |
|   Server             |
|   (Main Loop +       |
|   Selectors)         |
+----------------------+
       |       |
  +----+       +----+
  |                 |
+-------+       +-------+
| Thread|       | Thread|
|  1    |       |  2    |
+-------+       +-------+
   |                |
+--------+      +--------+
|Scraping|      |Scraping|
| Logic  |      | Logic  |
+--------+      +--------+
```

## How to Run

### Using Python
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   venv\Scriptsctivate     # On Windows
   ```
2. Install the requirements:
   ```bash
    pip install -r requirements.txt
    ```
3. Start the server:
   ```bash
   python mpr2025_KN_82119_Python_Windows_Server_Multithreading.py
   ```
4. Connect a client using the client script:
   ```bash
   python mpr2025_KN_82119_Python_Windows_Client.py
   ```

### Using Telnet (Optional)
Alternatively, connect using `telnet`:
```bash
telnet localhost 65432
```

## Future Improvements
1. **Error Handling**:
   - Enhance error reporting for client misbehavior and scraping failures.
2. **Pagination**:
   - Extend the scraper to handle paginated results automatically.
3. **Scalability**:
   - Upgrade to a process-based architecture for higher throughput.
4. **Caching**:
   - Implement caching to reduce redundant requests and improve response times for frequently accessed data.

---