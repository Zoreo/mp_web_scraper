
import socket
import json

def request_crypto_headlines():
    host = 'localhost'
    port = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            try:
                num_headlines = int(input("Enter the number of headlines to fetch (or type 0 to exit): "))
                if num_headlines == 0:
                    print("Exiting...")
                    break
                request = json.dumps({'num_headlines': num_headlines}).encode()
                s.sendall(request)
                data = s.recv(4096)
                headlines = json.loads(data.decode())
                for item in headlines:
                    print(f"Title: {item['title']}")
                    print(f"Link: {item['link']}")
                    print("-" * 40)
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    request_crypto_headlines()
