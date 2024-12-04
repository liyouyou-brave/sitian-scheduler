import socket
import os
import time
import select
import json
import struct
import mysql.connector
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gschedule import Global

import pdb

# Length size
LEN_SIZE = 4
# Create socket path
SOCKET_PATH = "/tmp/Global_socket"
# Max connection
BACKLOG = 5
# Message length
BUFFER_SIZE = 4096
# Time-out
TIME_OUT = 100

def Rec(client: socket.socket):
    request_len = client.recv(LEN_SIZE)
    if not request_len:
        print(f"Fail to receive data!")
        return 0,""
    # Convert to uint
    request_len = struct.unpack('I', request_len)[0]
    recv_data = client.recv(request_len+10).decode("utf-8")
    recv_data = recv_data.rstrip('\x00')
    return request_len, recv_data
    
def handle_ACK(ACK_rec):
    if ACK_rec.get('GENERAL-INFO',{}).get('operation') == "acknowledge":
        return
    else:
        return

# bind socket
def bind_socket(server:socket.socket, path):
    server.bind(path)
    print(f"Socket binded to {path}")
    # max connection number
    server.listen(BACKLOG)

def create_server_socket(path):
    print(f"Server socket is creating socket, please wait a minute...")
    time.sleep(1)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
    print(f"Socket has been created, server.family is {server.family}, server.proto is {server.proto}")
    # delete the previous connection  
    if os.path.exists(path):
        os.unlink(path)
    # bind the path
    print(f"Server socket is binding the path, please wait a minute...")
    time.sleep(1)
    bind_socket(server, path)
    # Set non-blocking mode
    server.setblocking(False)
    print(f"Server is listenning client's connect...")
    return server

def handle_client(client: socket.socket):
    # Listen for messages from connected clients
    while True:
        # pdb.set_trace()
        # Length of the received message
        request_len, recv_data = Rec(client)
        if request_len == 0:
            print("closed connection")
            break
        # recv_data = client.recv(BUFFER_SIZE).decode("utf-8")
        # if not recv_data:
        #     print(f"Connection closed!")
        #     break
        # 转为json格式
        # print(f"\n\n{recv_data}\n\n")
        # print(repr(recv_data))
        recv_data = json.loads(recv_data)
        print(f"Rec from client:\n{recv_data}")
        if recv_data.get('GENERAL-INFO',{}).get('operate') == "request":
            print("Calculating, please waiting")
            # start_cal_time = Global.GBlock(5, 100, 5, '2022-05-01T00:00:00', '2022-05-03T00:00:00')
            start_cal_time = "2024-11-19_15-25-16"
            global_output_path = f"/home/lxs_cloud/time_domain_survey/sitian_scheduler/output/{start_cal_time}/global/"
            json_outputs = [global_output_path+f for f in os.listdir(global_output_path) if f.endswith('.json')]
            json_outputs.sort()
            # print(f"json_outputs: {json_outputs}")
            for json_output in json_outputs:
                # print(f"json_output: {json_output}")
                with open(json_output, 'r', encoding='utf-8') as j:
                    response = json.load(j)
                response = json.dumps(response)
                response_len = len(response)
                # 有点问题
                print(f"response_len: {response_len}")
                
                response_len = struct.pack('I', response_len)
                client.send(response_len)
                client.sendall(response.encode("utf-8"))
                ACK_len, ACK_rec = Rec(client)
                # print(f"line 99: {ACK_len}\n{ACK_rec}")
                ACK_rec = json.loads(ACK_rec)
                if ACK_rec.get('GENERAL-INFO',{}).get('operate') == "acknowledge":
                    continue
                else:
                    print("break")
                    break
                # handle_ACK(ACK_rec)
                
    client.close()

def wait_and_connection(server:socket.socket):
    
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
    server = create_server_socket(SOCKET_PATH)
    wait_and_connection(server)
    server.close()