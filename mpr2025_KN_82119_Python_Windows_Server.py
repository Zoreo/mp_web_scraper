
import socket
import selectors
import types
import json
import requests
from bs4 import BeautifulSoup

# Web Scraper Function for Crypto News
def fetch_crypto_headlines(num_headlines):
    url = 'https://cointelegraph.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return [{'error': f'Failed to retrieve content: {response.status_code}'}]

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    # Locate the section containing news headlines
    articles = soup.find_all('article', limit=num_headlines)
    for article in articles:
        title_tag = article.find('h2')
        link_tag = article.find('a', href=True)

        title = title_tag.get_text(strip=True) if title_tag else 'No title'
        link = link_tag['href'] if link_tag else 'No link'

        headlines.append({
            'title': title,
            'link': f"https://cointelegraph.com{link}"
        })

    return headlines

# Selector Server
sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'how many headlines would you like?')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            client_request = recv_data.decode().strip().lower()
            if client_request == "exit":
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
            else:
                try:
                    num_headlines = int(client_request)
                    headlines = fetch_crypto_headlines(num_headlines)
                    response = "\n".join(
                        [f"Title: {item['title']}, Link: {item['link']}" for item in headlines]
                    )
                    data.outb = response.encode() + b"\nWould you like to see more? (Enter a number or 'exit'): "
                except ValueError:
                    data.outb = b"Invalid input. Please enter a number or 'exit': "
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE and data.outb:
        sent = sock.send(data.outb)
        data.outb = data.outb[sent:]

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