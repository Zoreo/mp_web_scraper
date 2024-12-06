
# mpr2025_KN_82119_Python_Windows Documentation

## Overview

This project demonstrates a **client-server system** that performs web scraping of cryptocurrency news headlines. The system is designed to:

1. Use a **web scraper** to fetch the latest cryptocurrency news headlines from the [Cointelegraph website](https://cointelegraph.com/).
2. Handle multiple clients simultaneously using an efficient **Selector paradigm** for connection management.
3. Allow clients to interact dynamically with the server by requesting headlines and responding to server prompts.

---

## Key Features

1. **Web Scraper**:
   - Dynamically fetches headlines and links from Cointelegraph's homepage.
   - Extracts useful data and formats it in a readable JSON format.

2. **Selector-Based Server**:
   - Efficiently manages multiple client connections without creating a separate thread for each client.
   - Processes requests dynamically based on client input.

3. **Interactive Client**:
   - Clients can specify the number of headlines they want in response to server prompts.
   - Clients can request more headlines or exit the interaction.

---

## TAM Diagram: System Flow

```text
+--------------------------+
|     Client (User)        |
|  - Interacts Dynamically |
|  - Responds to Prompts   |
|  - Requests Headlines    |
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

## Action Diagram: Interaction Flow

```text
Server sends prompt to client: "How many headlines would you like?"
                |
                v
Client responds with number (e.g., 3)
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
Server sends headlines to client
                |
                v
Server prompts: "Would you like to see more? (Enter number or 'exit')"
                |
                v
Client responds with number or "exit"
                |
                v
Process repeats or connection ends.
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
1. `mpr2025_KN_82119_Python_Windows_Server.py` (Server Code)
2. `mpr2025_KN_82119_Python_Windows_Client.py` (Client Code)
3. `requirements.txt` (Dependencies)
4. `mpr2025_KN_82119_Python_Windows_documentation.md` (This Documentation)

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

1. Start the server by running the server script:
   ```bash
   python mpr2025_KN_82119_Python_Windows_Server.py
   ```
2. The server will start and listen for connections on `localhost:65432`.
3. You should see output like this:
   ```
   Listening on ('localhost', 65432)
   ```

### Step 6: Run the Client

1. Open a new terminal or command prompt.
2. Run the client script:
   ```bash
   python mpr2025_KN_82119_Python_Windows_Client.py
   ```
3. Follow the on-screen instructions:
   - Enter the number of headlines you want when prompted.
   - Decide whether to request more or exit the interaction.

---

## Notes

1. **Internet Connection**:
   - The server requires an active internet connection to fetch data from Cointelegraph.

2. **Customization**:
   - You can modify the scraper to target other sections of Cointelegraph or different websites altogether.

3. **Scalability**:
   - The selector-based server design allows efficient handling of multiple client requests.

---

