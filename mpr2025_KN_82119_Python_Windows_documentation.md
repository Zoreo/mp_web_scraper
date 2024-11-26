
# mpr2025_KN_82119_Python_Windows Documentation

## Overview

This project is a demonstration of a **client-server system** that performs web scraping of cryptocurrency news headlines. The system is designed to:

1. Use a **web scraper** to fetch the latest cryptocurrency news headlines from the [Cointelegraph website](https://cointelegraph.com/).
2. Handle multiple clients simultaneously using an efficient **Selector paradigm** for connection management.
3. Allow clients to request a specific number of news headlines via a simple JSON request.

---

## Key Features

1. **Web Scraper**:
   - Dynamically fetches headlines and links from Cointelegraph's homepage.
   - Extracts useful data and formats it in a readable JSON format.

2. **Selector-Based Server**:
   - Efficiently manages multiple client connections without creating a separate thread for each client.
   - Processes requests and returns results dynamically.

3. **Ease of Use**:
   - Clients can specify the number of headlines they want, making it customizable.

---

## TAM Diagram: System Flow

```text
+--------------------------+
|     Client (User)        |
|  - Sends JSON Request    |
|  - Specifies # Headlines |
+--------------------------+
            |
            v
+--------------------------+
|       Server (API)       |
|  - Handles Multiple      |
|    Connections           |
|  - Parses Requests       |
|  - Returns JSON Response |
+--------------------------+
            |
            v
+--------------------------+
|      Web Scraper         |
|  - Fetches Headlines     |
|  - Parses HTML Content   |
|  - Formats as JSON       |
+--------------------------+
            |
            v
+--------------------------+
| Cointelegraph Website    |
|  - Source of News Data   |
+--------------------------+
```

---

## Action Diagram: Step-by-Step Process

```text
Client sends JSON request (e.g., {"num_headlines": 3})
                |
                v
+----------------------------+
| Server receives the request|
|  - Parses JSON             |
|  - Extracts # headlines    |
+----------------------------+
                |
                v
+----------------------------+
| Server calls scraper       |
|  - Sends GET request to    |
|    Cointelegraph           |
|  - Parses response HTML    |
|  - Extracts headlines      |
|  - Formats JSON response   |
+----------------------------+
                |
                v
+----------------------------+
| Server sends JSON response |
|  - Contains requested      |
|    headlines               |
+----------------------------+
                |
                v
Client receives and processes response
(e.g., Displays headlines)
```

---

## Setup

### Step 1: Install Python

1. Ensure Python 3.8 or newer is installed on your computer.
   - Download Python from [python.org](https://www.python.org/).
2. Verify the installation:
   - Open a terminal or command prompt and run:
     ```bash
     python --version
     ```

### Step 2: Download Project Files

Download the following files and place them in the same folder:
1. `mpr2025_KN_82119_Python_Windows.py` (Server Code)
2. `requirements.txt` (Dependencies)
3. `mpr2025_KN_82119_Python_Windows_documentation.md` (This Documentation)

### Step 3: Set Up a Virtual Environment

A virtual environment ensures that the project dependencies are isolated from the rest of your system.

1. Open a terminal or command prompt.
2. Navigate to the folder where the project files are located:
   ```bash
   cd path/to/project
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

### Step 4: Install Dependencies

1. Use the `requirements.txt` file to install the necessary Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Step 5: Run the Server

1. Start the server by running the Python script:
   ```bash
   python mpr2025_KN_82119_Python_Windows.py
   ```
2. The server will start and listen for connections on `localhost:65432`.
3. You should see output like this:
   ```
   Listening on ('localhost', 65432)
   ```

### Step 6: Test the Client

You can test the server using a custom client script or a tool like `curl`. Below is an example Python client script:

```python
import socket
import json

def request_crypto_headlines(num_headlines):
    host = 'localhost'
    port = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        request = json.dumps({'num_headlines': num_headlines}).encode()
        s.sendall(request)
        data = s.recv(4096)
    headlines = json.loads(data.decode())
    return headlines

if __name__ == "__main__":
    num_headlines = 5  # Request 5 headlines
    results = request_crypto_headlines(num_headlines)
    for item in results:
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print("-" * 40)
```

---

## Notes

1. **Internet Connection**:
   - The server requires an active internet connection to fetch data from Cointelegraph.

2. **Customization**:
   - You can modify the scraper to target other sections of Cointelegraph or different websites altogether.

3. **Scalability**:
   - The selector-based server design allows efficient handling of multiple client requests.

---

