# Chat Application in Python
Here is an example of creating a real time chatting application using **python**, **web sockets** and **tkinter** gui. This basic chat application provides an overview of **socket programming** using to demonstrate a **client server architecture** where multiple clients connect to the server and chat with random persons online

## Features
* Allows one-to-one communication with the clients online
* Allows broadcasting messages to all the clients online

## Python and Modules
This application is compatible with python version 3 and above

**Below are the modules used**
1. threading --> It enables the client to constantly receive the messages from server and server to keep accepting new connections and redirecting the messages from existing messages
1. socket --> Allows the client and server to communicate with each other
1. tkinter --> GUI for python, its already included in the python 
1. time --> Mainly it enables to maintain the speed of sending and receiving the data between the server and client

>[!Note]:  
>There is no requirement to download any additional modules

## Functioning and Gui
**Below is the GUI of server side application**

<img src = "Server_GUI.png" alt = Server style = "width:800px;"/>

1. Firstly, the server admin needs to enter the IP address to which server will bind and run on that IP and port number is by default 9000
1. Hit **Run Server** button to run the server
1. The white blank space is the place where server displays the client who has connected and disconnected to the server
1. The **Stop Server** button stops the server


**Below is the GUI of the client side application**

<!-- ![GUI](C:\Users\abc\Desktop\Chat_App\Client_GUI.png) -->
<img src = "Client_GUI.png" alt = Client style = "width:800px;"/>

1. The client first need to enter the IP address of the server and enter their username which must unique among all the currently connected clients otherwise a warning pop up is displayed saying **Username Exists**
1. The **Online clients** workspace is the place where name of the currently online clients to server are displayed, and client can select the particular client useing **select** button with whome they want to chat
1. **Chat with your friends** is the workspace where private chat between two clients are shown
1. **Send** button sends the message privately to the user with whom the client is chatting
1. **Broadcast** workspace allows to display the broadcasted messages
1. **Broadcast** button sends messages to all the clients currently online

## Working  
Basically, each of the client gets connected to the server with their **socket**, each clients socket is associated with their unique **username** and stored at run time to identify whose message is to be redirected to which user/client. Each message from the client is a string where in the starting of the actual message **receiver's username** and **sender's username** is added and decoded at the server. This collection of a string having **receiver + sender + message** is then divided in two parts **receiver & server + message** to identify the reciever where this remaining message is to be redirected. If the receiver is online the message is redirected to the respective client otherwise nothing happens. If a client broadcasts a message, the server redirects the message to all the clients online.

## Further features
1. Group chatting can be established
1. Sharing of mutlimedia files can be added

## References
>[Tkinter](https://www.javatpoint.com/python-tkinter)

>[Websockets](https://www.javatpoint.com/socket-programming-using-python)

>[Desgin a chat system](https://bytebytego.com/courses/system-design-interview/design-a-chat-system)

>[Building a chat room](https://www.scaler.com/topics/build-a-chatroom-in-python/)
<!-- <img src = C:/Users/abc/Desktop/Chat_App/Chat_App_GUI.png alt text = "GUI"> -->