
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
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.inb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE and data.inb:
        request = data.inb.decode()
        try:
            request_data = json.loads(request)
            num_headlines = int(request_data.get('num_headlines', 5))  # Default to 5 if not specified
            headlines = fetch_crypto_headlines(num_headlines)
            response = json.dumps(headlines).encode()
        except Exception as e:
            response = json.dumps({'error': str(e)}).encode()
        data.outb += response
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
            data.inb = b''

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
