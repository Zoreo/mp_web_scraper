
import socket

def interact_with_server():
    host = 'localhost'
    port = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            response = s.recv(4096).decode()
            print(response.strip())
            user_input = input()
            if user_input.lower() == "exit":
                s.sendall(user_input.encode())
                print("Exiting...")
                break
            else:
                s.sendall(user_input.encode())

if __name__ == "__main__":
    interact_with_server()
