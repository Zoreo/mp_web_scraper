import socket
import selectors
import types
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Web Scraper Function for DM Drogerie Markt Bulgaria using Selenium
def fetch_dm_products():
    url = "https://www.dm-drogeriemarkt.bg/search?query=%D1%88%D0%B0%D0%BC%D0%BF%D0%BE%D0%B0%D0%BD%D0%B8%20%D0%B7%D0%B0%20%D0%BA%D0%BE%D1%81%D0%B0&searchProviderType=product&sort=price_asc&popularFacet=%D0%9D%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D0%BD%D0%B0%20%D0%BA%D0%BE%D0%B7%D0%BC%D0%B5%D1%82%D0%B8%D0%BA%D0%B0"

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless browser
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Navigating to the website...")
        driver.get(url)

        # Wait for the product list to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#product-tiles div.pdd_14u321i8 div:nth-child(3) > a')
            )
        )

        products = []
        name_elements = driver.find_elements(
            By.CSS_SELECTOR, '#product-tiles div.pdd_14u321i8 div:nth-child(3) > a'
        )
        price_elements = driver.find_elements(
            By.CSS_SELECTOR, 'div.pdd_14u321i8 > div:nth-child(2) > div > div > span > span',
        )

        for name_element, price_element in zip(name_elements, price_elements):
            try:
                name_text = name_element.get_attribute("innerHTML")
                name = name_text.replace('&nbsp;', '').strip()

                price_text = price_element.get_attribute("innerHTML").strip()
                price = float(price_text.replace('лв.', '').replace(',', '.'))

                products.append({'name': name, 'price': price})
            except Exception:
                continue

        sorted_products = sorted(products, key=lambda x: x['price'])
        return sorted_products

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        driver.quit()

# Selector Server
sel = selectors.DefaultSelector()

def handle_client(sock, data):
    try:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            client_request = recv_data.decode().strip().lower()
            if client_request == "exit":
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
            else:
                try:
                    num_products = int(client_request)
                    print(f"Fetching products for client {data.addr}")
                    products = fetch_dm_products()
                    response = "\n".join(
                        [f"{i+1}. {item['name']}: {item['price']} лв." for i, item in enumerate(products[:num_products])]
                    )
                    response += "\nWould you like to see more? (Enter a number or 'exit'): "
                    sock.sendall(response.encode())
                except ValueError:
                    sock.sendall(b"Invalid input. Please enter a number or 'exit': ")
    except Exception as e:
        print(f"Error handling client {data.addr}: {e}")
        sel.unregister(sock)
        sock.close()

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        threading.Thread(target=handle_client, args=(sock, data), daemon=True).start()
    if mask & selectors.EVENT_WRITE and data.outb:
        sent = sock.send(data.outb)  # Send the initial prompt or response
        data.outb = data.outb[sent:]  # Clear the buffer after sending

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'How many products would you like to see?\n')
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)

def start_server(host, port):
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print(f"Listening on {(host, port)}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        sel.close()

if __name__ == "__main__":
    start_server('localhost', 65432)
