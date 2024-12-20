# Project Documentation: Multithreaded Web Scraper

## Table of Contents
- [Overview](#overview)
- [Implementation Details](#implementation-details)
  - [Web Scraping](#web-scraping)
  - [Multithreading](#multithreading)
  - [Selectors](#selectors)
  - [Server Functions](#server-functions)
  - [Client Functions](#client-functions)
  - [Diagram](#diagram)
- [How to Run](#how-to-run)
- [Future Improvements](#future-improvements)

## Overview
This project is a multithreaded web scraping server implemented in Python. It allows clients to request product information from the DM Drogerie Markt Bulgaria website, specifically targeting natural hair care products. The server processes multiple client requests concurrently using multithreading and an event-driven architecture with the `selectors` module. We use Selenium over BeautifulSoup and similar libraries because Selenium can handle dynamic, JavaScript-rendered content, which is essential for scraping most modern websites that rely on JavaScript to load product data.

## Implementation Details

### **Web Scraping**
The `fetch_dm_products` function uses Selenium to automate the scraping process that:
1. Navigates to the target URL.
2. Waits for the product list to load using `WebDriverWait`.
3. Extracts product names and prices using CSS selectors.
4. Cleans and processes the extracted data.
5. Sorts the products by price.

### **Multithreading**
- The server uses the `selectors` module for event-driven, non-blocking I/O.
- When a blocking task like web scraping is needed, it is offloaded to a separate thread using `threading.Thread`.
- **Why Multithreading?**
  - Selenium operations are inherently blocking. Without multithreading, the server would handle only one client at a time.
  - By delegating blocking tasks to threads, the server loop remains free to handle other client connections, improving responsiveness and scalability.

### **Selectors**
- CSS selectors are used to locate HTML elements for product names and prices.
- **Name Selector**: `#product-tiles div.pdd_14u321i8 div:nth-child(3) > a`
  - Locates the anchor tags containing product names within the product tiles.
- **Price Selector**: `div.pdd_14u321i8 > div:nth-child(2) > div > div > span > span`
  - Extracts the price details from the corresponding product tile.

## Server Functions
### **`main()`**
initializes the application and starts the server on localhost at port 65432 (runs start_server('localhost', 65432)).

### **`start_server(host, port)`**
Starts the server on the specified host and port, registering it with selectors.

### **`accept_wrapper(sock)`**
Accepts client connections and registers them for communication.

### **`service_connection(key, mask)`**
Handles client connections and spawns threads for requests.

### **`clean_up_socket(sock, data)`**
Unregisters and closes the client socket to release resources after the connection ends.

### **`handle_client(sock, data)`**
Processes client requests and sends responses.

### **`fetch_dm_products()`**
Scrapes the DM Drogerie Markt website and returns sorted product data.

## Client Functions

### **`main()`**
Connects to the server and manages user interactions (runs start_client(host, port)).

### **`start_client(host, port)`**
Facilitates communication with the server, processes server responses    

## Diagram

The diagram provide an architectural overview of the server and its multithreaded capabilities, as well as the client-server interaction flow.

### Architecture Diagram
```plaintext
+------------+ +-------------------+
|  Client 1  | |  Client 2, 3,...  |
+------------+ +-------------------+
      |            |
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
|  1    |       | 2,3,..|
+-------+       +-------+
   |                |
+--------+      +--------+
|Scraping|      |Scraping|
| Logic  |      | Logic  |
+--------+      +--------+
```

## How to Run

### Using Python
1. Activate the virtual environment, assuming you have Python and pip installed:
   ```bash
   python -m venv venv       # Create the virtual enviornment
   source venv/bin/activate  # Activate on macOS/Linux
   venv\Scripts\Activate     # Activate on Windows
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ``` 
3. Start the server:
   ```bash
   python server.py
   ```
4. Connect clients using the client script:
   ```bash
   python client.py
   ```

## Future Improvements
4. **Caching**:
   - Implement caching to reduce redundant requests and improve response times for frequently accessed data.
2. **Pagination**:
   - Extend the scraper to handle paginated results automatically.
3. **Scalability**:
   - Upgrade to a process-based architecture for higher throughput.
1. **Error Handling**:
   - Enhance error reporting for client misbehavior and scraping failures.
---
