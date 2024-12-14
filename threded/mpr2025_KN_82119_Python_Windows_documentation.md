
# Project Documentation: Multithreaded Web Scraper and Server

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

### **Server Architecture**
1. **Connection Management**:
   - The `selectors` module monitors multiple sockets for readiness (read/write).
   - The `accept_wrapper` function accepts new connections and registers them.

2. **Client Handling**:
   - Each client connection spawns a new thread for processing its requests.
   - The `handle_client` function handles communication with individual clients.

3. **Non-Blocking Design**:
   - The main server loop uses `selectors` to monitor sockets and delegate work efficiently.

## Diagrams

### **Architecture Diagram**
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
+------+       +------+
| Thread|       | Thread|
|  1    |       |  2    |
+------+       +------+
   |                |
+------+        +------+
|Scraping|      |Scraping|
| Logic  |      | Logic  |
+------+        +------+
```

### **Action Flow**
1. The client connects to the server.
2. The server sends an initial prompt: "How many products would you like to see?"
3. The client responds with a number.
4. The server spawns a thread to scrape the requested product data.
5. The thread performs the scraping task and sends the response back to the client.
6. The client can request more products or exit the session.

## How to Run
1. Start the server:
   ```bash
   python server_script.py
   ```
2. Connect a client using a simple socket-based client script or a tool like `telnet`:
   ```bash
   telnet localhost 65432
   ```

## Requirements
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### `requirements.txt` Content
```plaintext
selenium
webdriver-manager
```

## Future Improvements
1. **Error Handling**:
   - Enhance error reporting for client misbehavior and scraping failures.
2. **Pagination**:
   - Extend the scraper to handle paginated results automatically.
3. **Scalability**:
   - Upgrade to a process-based architecture for higher throughput.

---