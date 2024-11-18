'''
    Site scheduler server
    Recieve request from main program
    and calculate Target, then transfer
    schedule block to main program through socket
'''

import socket
import os
import time
import select
import threading
import json
# import "" 
# Create socket path
SOCKET_PATH = "/tmp/Site_socket"
# Max connection
BACKLOG = 5
# Message length
BUFFER_SIZE = 1024
# Time-out
TIME_OUT = 1000
result_lock = threading.Lock()

def bind_socket(server):
    server.bind(SOCKET_PATH)
    print(f"Socket binded to {SOCKET_PATH}")
    server.listen(BACKLOG)

def create_server_socket():
    # Create socket
    print(f"Site server socket is creating socket, please wait a minute...")
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

def wait_and_connection(server):
    start_time = time.time()

    ## socket创建完成，开始监听连接。

    while True:
        readable,_,_ = select.select([server], [], [], TIME_OUT)
        if readable:
            client, client_addr = server.accept()
            print(f"Connected with {client}, addr is {client_addr}")
            start_time = time.time()
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
            
        else:
            if time.time() - start_time >= TIME_OUT:
                print(f"Time out! Server closed!")
                break

def handle_push(client):
    print(f"handling push")
    # time.sleep(5)
    '''
        TODO: result = global_scheduler()
    '''
    send_message = "new result has been updated\n"
    client.sendall(send_message.encode("utf-8"))
    print("Updated request has been sended\n")
    
def handle_request(client):
    '''
        TODO: 从计算结果文件中读取第一个数据并返回
    '''
    send_message = "result"
    client.sendall(send_message.encode("utf-8"))
    print("Request has been sended\n")

def handle_client(client):
    while True:
        recv_data = client.recv(BUFFER_SIZE).decode("utf-8")
        if not recv_data:
            print(f"Client socket closed! Connection break down!")
            break
        else:
            recv_data = json.loads(recv_data)
            if recv_data.get('GENERAL-INFO',{}).get('operate') == "request":
                threading.Thread(target=handle_request, args=(client,), daemon=True).start()
                
            elif recv_data.get('GENERAL-INFO',{}).get('operate') == "push":
                threading.Thread(target=handle_push, args=(client,), daemon=True).start()

            else:
                send_message = "Please check out the message!\n"
                client.sendall(send_message.encode("utf-8"))
                
def start_site_server():
    
    server = create_server_socket()
    wait_and_connection(server)
    server.close()