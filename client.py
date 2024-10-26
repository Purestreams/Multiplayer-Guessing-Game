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
            client.send(command.encode())

        while True:
            incoming_message = client.recv(1024).decode()
            if incoming_message != "ready":
                print(incoming_message)
            if "ready" in incoming_message:
                while True:
                    command = input("% ")
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
                choice = input("% ")
                client.send(choice.encode())
                result = client.recv(1024).decode()
                print(result)
                while True:
                    command = input("% ")
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
    start_client()