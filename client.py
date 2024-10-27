import socket
import sys

def start_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        while True:
            incoming_message = client.recv(1024).decode()
            print(incoming_message)
            if "1001 Authentication successful" in incoming_message:
                break
            elif "1002" in incoming_message:
                continue
            command = input("")
            client.send(command.encode())

        while True:
            incoming_message = client.recv(1024).decode()
            if incoming_message != "ready":
                print(incoming_message)
            if "ready" in incoming_message:
                while True:
                    command = input("")
                    client.send(command.encode())
                    if command == "/exit":
                        print("Goodbye!")
                        return
                    elif command == "/list":
                        room_list = client.recv(1024).decode()
                        print(room_list)
                    elif "/enter" in command:
                        break
                    else:
                        received_message = client.recv(1024).decode()
                        print(received_message)

            if "3012" in incoming_message:
                choice = input("")
                client.send(choice.encode())
                result = client.recv(1024).decode()
                print(result)
                while True:
                    command = input("")
                    if "/exit" in command:
                        client.send(command.encode())
                        received_message = client.recv(1024).decode()
                        print(received_message)
                        if "4001" in received_message:
                            print("Client ends")
                            return
                    else:
                        client.send(command.encode())
                        received_message = client.recv(1024).decode()
                        print(received_message)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <server address> <server port>")
        sys.exit(1)
    
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Port must be an integer.")
        sys.exit(1)
    
    start_client(host, port)