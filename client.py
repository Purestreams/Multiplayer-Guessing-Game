import socket

# Server settings
HOST = '127.0.0.1'
PORT = 65432

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        while True:
            incoming_message = client.recv(1024).decode()
            print(incoming_message)
            if "1001 Authentication successful" in incoming_message:
                break

            command = input("% ")
            client.sendall(command.encode())

        while True:
            incoming_message = client.recv(1024).decode()
            print(incoming_message)
            if "Please select a room (1-10)" in incoming_message:
                while True:
                    command = input("Enter room number or /list to see all rooms or /exit to leave: ")
                    client.sendall(command.encode())
                    if command == "/exit":
                        print("Goodbye!")
                        return
                    elif command == "/list":
                        room_list = client.recv(1024).decode()
                        print(room_list)
                    else:
                        break

            if "3012" in incoming_message:
                choice = input("Enter your choice (true/false): ")
                client.sendall(choice.encode())
                result = client.recv(1024).decode()
                print(result)
                break

if __name__ == "__main__":
    start_client()