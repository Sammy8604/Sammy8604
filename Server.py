import socket
import threading

HEADER = 64
ip = socket.gethostbyname(socket.gethostname())
port = 5050
ADDR = (ip, port)
FORMAT = "utf-8"
Disconnect_msg = "LEAVING"
connections = set()
conn_lock = threading.Lock()
stack =[]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    global list
    print(list)
    print(type(list[0]))
    new = True
    print(f"[CONNECTION] New connection - {addr}")
    name = addr
    welcome_message = ("Welcome, \nPlease note the first message you send will be considered asyour name\nMessage end to leave").encode(FORMAT)
    length_msg = len(welcome_message)
    length_msg = str(length_msg).encode(FORMAT)
    length_msg += b" " * (HEADER-len(length_msg))
    conn.send(length_msg)
    conn.send(welcome_message)

    connected = True
    while connected:
        temp = ""
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == Disconnect_msg:
                connected = False
            if new == True:
                new = False
                name = msg
                stack.append(name)
                stack.append("NEW")
                with conn_lock:
                    for i in connections:
                        if i!=conn:
                            #first sends the length of the message padded to length 64
                            length_msg = len("NEW")
                            length_msg = str(length_msg).encode(FORMAT)
                            length_msg += b" " * (HEADER-len("NEW"))
                            i.send(length_msg)
                            i.send("NEW".encode(FORMAT))
                            length_msg = len(name)
                            length_msg = str(length_msg).encode(FORMAT)
                            length_msg += b" " * (HEADER-len(length_msg))
                            i.send(length_msg)
                            #sends the name
                            i.send(name.encode(FORMAT))

            if msg != name:
                if msg != "LEAVING":
                    msg = f"{name}: {msg}"
                else:
                    if name != "LEAVING":
                        msg = f"{name} has left the chat"
                    else:
                        msg = "Unknown has left the chat"
                print(msg)
                with conn_lock:
                    for i in connections:
                        if i!=conn:
                            length_msg = len(msg)
                            length_msg = str(length_msg).encode(FORMAT)
                            length_msg += b" " * (HEADER-len(length_msg))
                            i.send(length_msg)
                            i.send(msg.encode(FORMAT))

    print(f"[LEAVING] {addr} has left the chat")
    connections.remove(conn)
    conn.close()


def start():
    global connections
    server.listen()
    print(f"Listening at {ip}")
    while True:
        conn, addr = server.accept()
        print(conn,addr)
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        connections.add(conn)
        thread.start()
        print(f"[CONNECTIONS] There are {threading.active_count()-1} connections.")

print("[START] Server is starting...")
start()