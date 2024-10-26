import socket
import threading
import random
import time

# Server settings
HOST = '127.0.0.1'
PORT = 65432

clients = {i: [] for i in range(1, 11)}
choices = {i: {} for i in range(1, 11)}

users = {"user1": "password1", "user2": "password2"}

# Create a lock object
lock = threading.Lock()

def handle_client(conn, addr):
    # Send welcome message
    while True:
        conn.send(b"Please input your user name")
        username = conn.recv(1024).decode()
        conn.send(b"Please input your password")
        password = conn.recv(1024).decode()
        if users.get(username) == password:
            conn.send(b"1001 Authentication successful")
            break
        else:
            conn.send(b"1002 Authentication failed")

    # Wait for 50ms to prevent message from being sent too fast and leading to an error
    time.sleep(0.05)

    send_ready = True

    while True:
        #Please select a room (1-10) or type /list to see all rooms or /exit to leave"
        if send_ready:
            conn.send(b"ready")
            time.sleep(0.05)
            send_ready = False

        
        message = conn.recv(1024).decode().strip()

        if message == "/exit":
            conn.send(b"Goodbye!\n")
            conn.close()
            return
        elif message == "/list":
            with lock:
                no_of_players_in_room = [len(clients[i]) for i in range(1, 11)]
                room_list = "3001 " + " ".join(map(str, no_of_players_in_room))
            conn.send(room_list.encode())
            time.sleep(0.05)
            continue
        elif "/enter" in message:
            try:
                #/enter n
                room = int(message.split(" ")[1])
                if room not in range(1, 11):
                    conn.send(b"Invalid room number\n")
                    continue
            except ValueError:
                conn.send(b"Invalid input\n")
                continue

            if len(clients[room]) == 2:
                conn.send(b"3013 Room is full\n")
                continue

            with lock:
                clients[room].append(conn)

            with lock:
                if len(clients[room]) == 2:
                    clients[room][0].send(b"3012 Game started. Please guess true or false")
                    clients[room][1].send(b"3012 Game started. Please guess true or false")
                else:
                    conn.send(b"3011 Wait")

            # Expect client to send "true" or "false"
            input = conn.recv(1024).decode()
            choice = input.split(" ")[1].lower()
            with lock:
                if choice == "true":
                    choices[room][addr] = 1
                elif choice == "false":
                    choices[room][addr] = 0
                else:
                    conn.send(b"Invalid choice\n")
                    return

            # If there are 2 choices, send random choice one client to be the winner
            with lock:
                if len(choices[room]) == 2:
                    client_addrs = list(choices[room].keys())
                    if choices[room][client_addrs[0]] == choices[room][client_addrs[1]]:
                        clients[room][0].send("3023 The result is a tie\n".encode())
                        clients[room][1].send("3023 The result is a tie\n".encode())
                    else:
                        winner = random.randint(0, 1)
                        if winner == 1:
                            clients[room][0].send(f"3021 You are the winner".encode())
                            clients[room][1].send(f"3022 You lost this game".encode())
                        else:
                            clients[room][1].send(f"3021 You are the winner".encode())
                            clients[room][0].send(f"3022 You lost this game".encode())
                    choices[room].clear()
                    clients[room].clear()
            break
        else:
            #4002 Unrecognized message
            conn.send(b"4002 Unrecognized message")

    while True:
        message = conn.recv(1024).decode().strip()
        if message == "/exit":
            conn.send(b"4001 Bye Bye")
            conn.close()
            return
        else:
            conn.send(b"4002 Unrecognized message")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started on {HOST}:{PORT}")
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()