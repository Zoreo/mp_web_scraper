
import socket

def start_client(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print("Connected to server.")

            while True:
                # Receive prompt from server
                server_message = client_socket.recv(1024).decode()
                if not server_message:
                    print("Server closed the connection.")
                    break

                print(server_message, end="")

                # Send user input to server
                user_input = input()
                client_socket.sendall(user_input.encode())

                if user_input.strip().lower() == "exit":
                    print("Exiting client.")
                    break

    except ConnectionRefusedError:
        print(f"Failed to connect to the server at {host}:{port}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    server_host = "localhost"  # Change if the server runs on a different host
    server_port = 65432       # Change if the server uses a different port
    start_client(server_host, server_port)
