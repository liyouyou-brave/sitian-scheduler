'''
    
'''
import socket
import os
import time
import select
import json
import mysql.connector
# Create socket path
SOCKET_PATH = "/tmp/Global_socket"
# Max connection
BACKLOG = 5
# Message length
BUFFER_SIZE = 1024
# Time-out
TIME_OUT = 10

def bind_socket(server):
    server.bind(SOCKET_PATH)
    print(f"Socket binded to {SOCKET_PATH}")
    server.listen(BACKLOG)

def create_server_socket():
    print(f"Server socket is creating socket, please wait a minute...")
    time.sleep(1)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
    print(f"Socket has been created, server.family is {server.family}, server.proto is {server.proto}")
    # delete the previous connection  
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)
    # bind the path
    print(f"Server socket is binding the path, please wait a minute...")
    time.sleep(1)
    bind_socket(server)
    # Set non-blocking mode
    server.setblocking(False)
    print(f"Server is listenning client's connect...")
    return server

def handle_client(client):
    while True:
        recv_data = client.recv(BUFFER_SIZE).decode("utf-8")
        if not recv_data:
            print(f"Connection closed!")
            break
        # 转为json格式
        recv_data = json.loads(recv_data)
        print(f"rec:\n{recv_data}")
        if recv_data.get('GENERAL-INFO',{}).get('operate') == "request":

            print("Calculating")
            # global_cal()
            # Global.GBlock(5, 100, 5, '2022-05-01T00:00:00', '2022-05-03T00:00:00')

            with open('1.json', 'r') as j:
                response = json.load(j)
            response = json.dumps(response)
            client.sendall(response.encode("utf-8"))
        elif recv_data.get('GENERAL-INFO',{}).get('operate') == "ACK":
            '''
                需要client端的适配
            '''
            res = "122112\n"
            client.sendall(res.encode("utf-8"))
    client.close()

def wait_and_connection(server):
    
    start_time = time.time()
    while True:
        readable,_,_ = select.select([server], [], [], TIME_OUT)
        if readable:
            client, client_addr = server.accept()
            print(f"Connected with {client}, addr is {client_addr}")
            start_time = time.time()
            handle_client(client)
        else:
            if time.time() - start_time >= TIME_OUT:
                print(f"Time out! Server closed!")
                break

def start_server():
    server = create_server_socket()
    wait_and_connection(server)
    server.close()
