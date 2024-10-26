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
                room = input("Enter room number: ")
                client.sendall(room.encode())

            #if incoming_message == "3012 Game started. Please guess true or false":
            if "3012" in incoming_message:
                choice = input("Enter your choice (true/false): ")
                client.sendall(choice.encode())
                result = client.recv(1024).decode()
                print(result)
                break

if __name__ == "__main__":
    start_client()