from tkinter import *
from tkinter import messagebox
import threading,socket,time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = Tk()
root.title("Client")
root.geometry("1000x600")
root.configure(bg="sky blue")

server_port = 9000
online_clients = []
sender = ''
receiver = ''
server_ip = StringVar()
username = StringVar()
message_box = StringVar()
x_sender = 800
y_sender = 400

back_frame = Frame(root)
broadcast_canvas = Canvas(back_frame,width=200,height=400,bg="white")
broadcast_scroller = Scrollbar(back_frame,orient=VERTICAL,command=broadcast_canvas.yview)

broadcast_frame = Frame(broadcast_canvas)

broadcast_canvas.create_window((0,0), window=broadcast_frame)
broadcast_canvas.configure(yscrollcommand=broadcast_scroller.set)
broadcast_canvas.pack(side=LEFT,fill=BOTH,expand=True)

broadcast_scroller.pack(side=RIGHT, fill=Y)

back_frame.place(x=740,y=120)

background_canvas = Canvas(root,bg="white",height=400,width=570)
background_canvas.place(x=150,y=120,anchor=NW)

chat_scroller = Scrollbar(root,command=background_canvas.yview)
chat_scroller.pack(side=RIGHT,fill=Y)

background_canvas.configure(yscrollcommand=chat_scroller.set)

background_canvas.configure(scrollregion=background_canvas.bbox("all"))

broadcast_x = 0
broadcast_y = 350


def broadcastMessages(): #Broadcasts the message
    message = message_box.get()


    if(message != ''):
        try:
            global broadcast_x, broadcast_y
            final_message =  'GLOBAL-' + sender + '~' + message
            client.send(final_message.encode())
                  
            broadcast_canvas.create_text((120, broadcast_y), text=message, width=100)
            broadcast_y += 30
                
            broadcast_canvas.configure(scrollregion=broadcast_canvas.bbox("all"))
                     
        except Exception as e:
            print("in broadcastMessages() :",e)
            messagebox.showerror("Error","Message was not sent!")

        back_frame.bind("<Configure>",lambda e: broadcast_canvas.configure(scrollregion=broadcast_canvas.bbox("all")))
    else:
        messagebox.showwarning("Warning","Message cannot be empty")

def selectedReceiver(): # Selecting the receiver
    global receiver
    for i in online_contacts_listbox.curselection():
        receiver = online_contacts_listbox.get(i)
    messagebox.showinfo("Notification","Sending messages to {receiver}".format(receiver=receiver))

def contact_list(contact): # Getting the online clients into a list
    if(contact == "NO CLIENTS"):
        messagebox.showinfo("Notification","Everyone is offline")
    elif(contact != ''):
        print(contact)
        online_clients.append(contact)
        online_contacts_listbox.insert(END, contact)

def sendMessages(): # Sending private messages
    message = message_box.get()
    print("receiver :",receiver)

    if(receiver != '' or receiver == 'GLOBAL'):
        if(message != ''):
            try:
                global x_sender,y_sender
                
                final_message =  receiver+'-' + sender + '~' + message
                client.send(final_message.encode())
                
                background_canvas.create_text((500,y_sender), text=message)
                background_canvas.configure(scrollregion=background_canvas.bbox("all"))
                
                y_sender += 30
            except Exception as e:
                print(e)
                messagebox.showerror("Error !","Message was not sent")
        else:
            messagebox.showwarning("Warning","Message cannot be empty")
    else:
        messagebox.showwarning("Warning","Select a receiver")

def communicate(): # Sets up labels and message entry 
    print("send_message()")
    
    Label(root, text="Enter message",bg="white").place(x=200, y = 550,anchor = S)
    Entry(root,textvariable=message_box,width=75).place(x=475, y = 550, anchor=S)
    Button(root,text="Send",activebackground="white",command=sendMessages).place(x=710,y=527)
    Button(root,text="Broadcast",activebackground="white",command=broadcastMessages).place(x=825,y=527)

    threading.Thread(target=receiveMessages).start()
    
def receiveMessages(): # Constatnly receives the message via threading
    global y_sender
    global broadcast_y
    global receiver
    while(True):
        try:
            message = client.recv(1024).decode()
            
            print("message :",message)

            if(message == ''):
                break

            elif(message.startswith("CONTACT")):
                contact = message.split("-")
                contact = str(contact[1])
                print(contact)
                contact_list(contact)

            elif(message.startswith("GLOBAL")):
                message = message.split('-')
                message = str(message[1])
                broadcast_canvas.create_text((10,broadcast_y), text=message)
                broadcast_y += 30
                broadcast_canvas.configure(scrollregion=broadcast_canvas.bbox("all"))     
            
            elif(receiver == ''):                
                message = message.split('~')
                print("message:",message)
                receiver = message[0]
                print("receiver :",receiver)
                
                if(receiver in online_clients):
                    messagebox.showinfo("Notification","Sending messages to {receiver}".format(receiver=receiver))

                    background_canvas.create_text((10,y_sender),text=message,fill="gray")
                    background_canvas.configure(scrollregion=background_canvas.bbox("all"))                

                    y_sender += 30

            else:
                message = message.split('~')
                print("message:",message)
                receiver = message[0]
                print("receiver :",receiver)
                    
                if(receiver in online_clients):
                    background_canvas.create_text((10,y_sender),text=message,fill="gray")
                    background_canvas.configure(scrollregion=background_canvas.bbox("all"))                

                    y_sender += 30
                                                    
        except:
            print('\n')
            break

def disconnect(): # Disconnects client from server
    messagebox.showinfo("Notification","Disconnected from server")
    client.close()

def connect(): # Establishes connection between client and server
    global client
    server_host = server_ip.get()

    try:
        global sender
        client.connect((server_host, 9000))
        print("\nConnecting to the server\n\n")
        
        sender = username.get()

        while(True):
            sender = username.get()
            print("sender :",sender)

            if(sender == ''):
                messagebox.showinfo("Username cannot be empty")
                print("Username cannot be empty\n")
                            
            else:
                client.send(sender.encode())
                server_message = client.recv(1024).decode()
                
                if(server_message == "USERNAME EXISTS"):
                    messagebox.showinfo("Notification from Server",server_message)
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    time.sleep(2)
                    break
                    

                else:
                    thread = threading.Thread(target=receiveMessages)
                    thread.start()

                    Button(root,text="Disconnect",activebackground="white",command=disconnect).place(x=500, y= 80)

                    communicate()

                    break
        
    except Exception as e:
        print("An error occurred! while connection",e)
        messagebox.showerror("Cannot connect to the server ! Server might be shut down")

Label(root,text="Chat with your Friends",font=("Comic Sans MS",16,"bold"),bg="white").place(x=330,y=120)
Label(root,text = "Online Friends",font=("Comic Sans MS",10),bg="white").place(x=27,y=123)
Label(root,text="Broadcasts",font=("Comic Sans MS",16,"bold"),bg="white").place(x=800,y=120)

Label(root,text='Server IP : ',bg="sky blue",font=("Comic Sans MS",10)).place(x=400,y=10)
Entry(root,textvariable=server_ip).place(x=500,y=10)

Label(root,text="Username : ",bg="sky blue",font=("Comic Sans MS",10)).place(x=400,y=40)
Entry(root,textvariable=username).place(x=500,y=40)

Button(root, text='Connect',activebackground='white',command=connect).place(x=405,y=80)
Button(root, text="Select",command=selectedReceiver).place(x=50,y=530)

online_contacts_listbox = Listbox(root,height=23,width=20)
online_contacts_listbox.place(x=10,y=150)

root.mainloop()