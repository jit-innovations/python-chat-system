import socket, threading, time
from tkinter import *
from tkinter import messagebox

server_ip = '127.0.0.1'
port = 9000

root = Tk()
root.geometry("1000x550")
root.title("Server")
root.configure(bg="sky blue")

x = 100
y = 100

background_canvas = Canvas(root,bg="white",scrollregion=(0,0,1000,1000),height=400,width=800)
background_canvas.place(x=100,y=50)

chat_scroller = Scrollbar(root,command=background_canvas.yview)
chat_scroller.pack(side=RIGHT,fill=Y)
background_canvas.configure(yscrollcommand=chat_scroller.set)

background_canvas.configure(scrollregion=background_canvas.bbox("all"))

online_clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def show_clients(client_socket): # Sends the list of online clients to the newly joined client
    if(len(online_clients) == 0):
        client_socket.send("All users are offline\n".encode())
    else:
        for client in online_clients.keys():
            online_client = str("CONTACT - " + online_clients.get(client)).encode()
            client_socket.send(online_client)
            time.sleep(2)
        client_socket.send("END".encode())

def redirect_messages(username, message): # Redirects the message between clients
        try: 
            if(message.startswith("GLOBAL")):
                for socket in online_clients.keys():
                    if(online_clients.get(socket) == username):
                        pass
                    else:
                        socket.send(message.encode())

            else:
                message = message.split('-')
                print(message)
                receiver = message[0]
                print("receiver :",receiver)             
                message = str(message[1])
                print(message)

                if(receiver in online_clients.values()):
                    for socket in online_clients.keys():
                        if(online_clients.get(socket) == receiver):
                            socket.send(message.encode())
                            break
                else:
                    global x,y
                    y += 25
                    background_canvas.create_text((x,y), text="receiver of this message is offline",font=(12))
                    background_canvas.configure(scrollregion=background_canvas.bbox("all"))
               
        except Exception as e:
            print(e)

def accepted_clients(client_socket): # Working onto connected clients
    while(True):
        try:
            username = online_clients.get(client_socket)
            messages = client_socket.recv(1024).decode()
            print(messages)

            thread = threading.Thread(target=redirect_messages, args=(username, messages))
            thread.start()

            time.sleep(0.1)            

        except:
            global x,y
            y+=25
            background_canvas.create_text((x,y), text=online_clients.get(client_socket) + ' has disconnected',font=(12))
            y += 25
            background_canvas.create_text((x,y), text='Removed the client from being online\n')
            y += 25
            online_clients.pop(client_socket)
            background_canvas.configure(scrollregion=background_canvas.bbox("all"))            
            
            break

def connections(): # Connecting the clients  
    server.listen()
       
    try:
        while(True):  
            client_socket, client_address = server.accept()

            while(True):
                name = client_socket.recv(1024).decode()

                if(name not in online_clients.values()):
                        global x, y   

                        online_clients.update({client_socket : name})
                        print(online_clients.values())

                        client_socket.send("Connected successfully !\n\n".encode())
                            
                        background_canvas.create_text((x,y), text="Client has connected: " + name,font=(12))
                        background_canvas.configure(scrollregion=background_canvas.bbox("all"))
                        y += 25
                        
                        # Informing existing clients about the new client

                        if(len(online_clients) > 1):
                            for client in online_clients.keys():
                                if(online_clients.get(client) != name):
                                    client.send(str("CONTACT-"+name).encode())
                                    client_socket.send(str('CONTACT-'+online_clients.get(client)).encode())
                                
                        else:
                            client_socket.send("CONTACT-NO CLIENTS".encode())

                        break                

                else:
                            client_socket.send("USERNAME EXISTS".encode())

            thread = threading.Thread(target=accepted_clients,args=(client_socket,client_address))
            thread.start()

    except ConnectionAbortedError as c:
        print("in connections() -",c)
        online_clients.pop(client_socket)
        print(online_clients)
        return

    except Exception as e:
        print(e)

def stop(): # Stopping the server
    messagebox.showinfo("Notification","Server has been shutdown")
    
    try:
        server.close()
    except Exception as e:
        server.close()

def run(): # Runs the server
    try:
        server.bind((server_ip, port))
        messagebox.showinfo("Notification","Server is running")
        global x,y
        background_canvas.create_text((x,y), text="Server started",font=(12))        
        background_canvas.configure(scrollregion=background_canvas.bbox("all"))
        y += 25

        while(True):
            connections()
        
    except WindowsError as w:
        print(w)
    except Exception as e:
        print(e)
        messagebox.showerror("Error","Server is unable to run")

def runThread(): # Starts the thread to run the server
    Button(root, text="Stop Server", command=stop).place(x=500,y=475)

    threading.Thread(target=run).start()

# server_ip_label = Label(root,text='Server IP : ',bg="sky blue").place(x=300,y=10)
# server_ip_entry = Entry(root,textvariable=server_ip).place(x=400,y=10)

Button(root, text="Run Server", command=runThread).place(x=400,y=475)


root.mainloop()