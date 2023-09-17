import socket
import threading
import customtkinter
from tkinter import Tk, Frame, Entry, Button, Scrollbar, Text, LEFT, RIGHT, Y

HEADER = 64
port = 5050
FORMAT = "utf-8"
Disconnect_msg = "LEAVING"
ip = "192.168.10.162"
ADDR = (ip, port)
run = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive_messages():
    global name
    while run:
        length_received = client.recv(HEADER).decode(FORMAT)
        received = client.recv(int(length_received)).decode(FORMAT)
        if received=="NEW":
            length_received = int(client.recv(HEADER).decode(FORMAT))
            new_join = client.recv(length_received).decode(FORMAT)
            chat_box.insert("end",f"{new_join} has just joined the chat\n")
        else:
            chat_box.insert("end",f"{received}\n")

def send_message():
    msg = message_box.get()
    if msg == "end":
        msg = "LEAVING"
    message_box.delete(0, len(msg))
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    chat_box.insert("end",f"You: {msg} \n")
    if msg == "LEAVING":
        quit()

customtkinter.set_appearance_mode("dark")

window = customtkinter.CTk()
window.geometry("500x400")
window.title("Messenger")

chat_frame = Frame(window, width=480, height=360)
chat_frame.pack(padx=10, pady=10)

chat_box = Text(chat_frame, width=60, height=23)
chat_box.pack(side=LEFT, fill=Y)

scrollbar = Scrollbar(chat_frame)
scrollbar.pack(side=RIGHT, fill=Y)

scrollbar.config(command=chat_box.yview)
chat_box.config(yscrollcommand=scrollbar.set)

input_frame = customtkinter.CTkFrame(window, width=480, height=50)
input_frame.pack(padx=10, pady=(0, 10))  # Add extra padding to the bottom

message_box = customtkinter.CTkEntry(input_frame, width=340, height=50, placeholder_text="Enter Message")
message_box.pack(side=LEFT)

send_button = customtkinter.CTkButton(input_frame, text=">", width=50, height=50)
send_button.pack(side=LEFT, padx=10)

send_button.configure(command=send_message)

thread = threading.Thread(target = receive_messages)
thread.start()

window.mainloop()

send_message("LEAVING")