
# mpr2025_KN_82119_Python_Windows Documentation

## Overview

This project demonstrates a **client-server system** that scrapes product data from [DM Drogerie Markt Bulgaria](https://www.dm-drogeriemarkt.bg) for "шампоани за коса" (hair shampoos), sorts the products by price from lowest to highest, and allows clients to request a specified number of products.

The scraping functionality is implemented using **Selenium**, enabling dynamic loading of content to ensure accurate data retrieval.

---

## Key Features

1. **Web Scraper**:
   - Fetches product names and prices from the specified URL using `Selenium`.
   - Handles dynamic JavaScript content.
   - Sorts products in ascending order by price.

2. **Selector-Based Server**:
   - Manages multiple client connections efficiently.
   - Responds dynamically to client input, providing sorted product data.

3. **Interactive Client**:
   - Clients can specify the number of products to display and decide whether to request more.

---

## System Flow Diagram

```plaintext
+--------------------------+
|     Client (User)        |
|  - Interacts Dynamically |
|  - Responds to Prompts   |
|  - Requests Product Data |
+--------------------------+
            |
            v
+--------------------------+
|       Server (API)       |
|  - Handles Multiple      |
|    Connections           |
|  - Parses Requests       |
|  - Calls Scraper         |
|  - Prompts Client        |
+--------------------------+
            |
            v
+--------------------------+
|      Web Scraper         |
|  - Fetches Product Data  |
|  - Parses Dynamic Content|
|  - Formats and Sorts Data|
+--------------------------+
            |
            v
+--------------------------+
| DM Drogerie Markt Website|
|  - Source of Product Data|
+--------------------------+
```

---

## Setup

### Step 1: Install Python

Ensure Python 3.8 or newer is installed on your computer.

### Step 2: Download Project Files

1. `mpr2025_KN_82119_Python_Windows_Server_Selenium_DM.py`
2. `requirements.txt`
3. Client script (optional).

### Step 3: Set Up a Virtual Environment

1. Navigate to the project folder:
   ```bash
   cd path/to/project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

### Step 4: Install Dependencies

Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### Step 5: Run the Server

1. Start the server:
   ```bash
   python mpr2025_KN_82119_Python_Windows_Server_Selenium_DM.py
   ```

2. The server will listen for connections on `localhost:65432`.

### Step 6: Run the Client

1. Open a new terminal or command prompt.
2. Run the client script:
   ```bash
   python mpr2025_KN_82119_Python_Windows_Client.py
   ```

3. Follow the prompts to retrieve sorted product data.

---

## Notes

1. **Dependencies**:
   - Ensure all dependencies are installed using `requirements.txt`.

2. **Error Handling**:
   - The server handles missing or invalid data gracefully and logs errors.

3. **Dynamic Content**:
   - Selenium ensures all dynamic content is properly loaded before scraping.

---
