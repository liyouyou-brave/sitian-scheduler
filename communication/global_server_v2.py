import os
import sys
import time
import json
import fcntl
import struct
import socket
import logging
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from communication import file_lock
from communication import debug
from gschedule import Global

# global server lock
GLOBAL_LOCK_FILE = "/tmp/Global_lock"
# Data header length, 4 bytes
DATA_HEADER_LEN = 4
# Socket path
SOCKET_PATH = '/tmp/Global_socket'
# Max connection
BACKLOG = 5
# Message length
BUFFER_SIZE = 4096

# def handle_header(client: socket.socket):
#     request_len = client.recv(DATA_HEADER_LEN)
#     return request_len
def create_server_socket(path):
    # print("Server socket is creating, please wait a minute...")
    time.sleep(1)
    try:
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        # print(f"Global server socket has been created, server's family is {server.family}, server's protocol is {server.proto}")
        if os.path.exists(path):
            os.unlink(path)
        server.bind(path)
        # print(f"Global server binded successfully, addr is {path}")
        server.listen(BACKLOG)
        return server
    except socket.error as e:
        filename, lineno = debug.get_current_location()
        print(f"Socket error: {e}\tfilename: {filename}\tlineno: {lineno}")
    except OSError as e:
        filename, lineno = debug.get_current_location()
        print(f"Operating system error: {e}\tfilename: {filename}\tlineno: {lineno}")
    except PermissionError:
        filename, lineno = debug.get_current_location()
        print(f"Permission error: Unable to access or modify the socket file {path}")
    except Exception as e:
        filename, lineno = debug.get_current_location()
        print(f"An unexpected error occurred: {e}\tfilename: {filename}\tlineno: {lineno}")
        
def handle_client(client:socket.socket):
    try:
        while True:
            # handle header
            print("Waiting request...")
            request_len = client.recv(DATA_HEADER_LEN)
            if not request_len:
                print("Failed to receive data")
                break
            # decode
            request_len = struct.unpack('I', request_len)[0]
            # receive request
            request_data = client.recv(request_len).decode('utf-8')
            # print(repr(request_data))
            # request_data = request_data.strip('\x00')

            request_json = json.loads(request_data)
            print(f"Global received request: {request_json}")
            # if request_json.get('GENERAL-INFO',{}).get('operate') == 'request':
            if True:
                # print('Calculating, please wait a minute')
                # print(123)
                start_cal_time = Global.GBlock(5, 100, 5, '2022-05-01T00:00:00', '2022-05-03T00:00:00')
                # print(2334)
                # start_cal_time = "2024-11-19_15-25-16"
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                schedule_block_path = f"{base_dir}/output/{start_cal_time}/global/"
                print(schedule_block_path)
                json_outputs = [schedule_block_path+f for f in os.listdir(schedule_block_path) if f.endswith('.json')]
                json_outputs.sort()
                for json_output in json_outputs:
                    print(json_output)
                    with open(json_output, 'r') as j:
                        schedule_block = json.load(j)
                    # convert to json from python object
                    schedule_block = json.dumps(schedule_block)
                    schedule_block_len = struct.pack('I', len(schedule_block))
                    client.send(schedule_block_len)
                    # print(f"Server sended SB length:{len(schedule_block_len)}")
                    client.sendall(schedule_block.encode('utf-8'))
                    # print("Server has sended SB")
                    ACK_len = client.recv(DATA_HEADER_LEN)
                    ACK_len = struct.unpack('I', ACK_len)[0]
                    ACK_data = client.recv(ACK_len).decode('utf-8')
                    # ACK_data = ACK_data.rstrip('\x00')
                    ACK_data = json.loads(ACK_data)
                    if ACK_data.get('GENERAL-INFO', {}).get('operate') == 'acknowledge':
                        continue
                    else:
                        print(f"Receive message is not ack, it is {ACK_data}")
                        break
            time.sleep(1)
            print("Request over")
    except (EOFError, BrokenPipeError):
        print("Client broken unexpectly")
    finally:
        client.close()
                                  
def connect_and_handle_client(server: socket.socket):
    try:
        # start_cal_time = Global.GBlock(5, 100, 5, '2022-05-01T00:00:00', '2022-05-03T00:00:00')
        
        while True:
            client, client_addr = server.accept()
            print(f"Connected with {client}")
            handle_client(client)
    # except Exception as e:
    #     print(f"23Exception occur: {e}")
    finally:
        file_lock.re_lock(lock_file=GLOBAL_LOCK_FILE)
        
        server.close()    
        
def start_global_server():
    # file_lock.re_lock(lock_file=GLOBAL_LOCK_FILE)
    global_lock = file_lock.ac_lock(lock_file=GLOBAL_LOCK_FILE)
    if not global_lock:
        print("Global lock has been used")
        sys.exit(1)
    # start_cal_time = Global.GBlock(5, 100, 5, '2022-05-01T00:00:00', '2022-05-03T00:00:00')
    
    global_server = create_server_socket(path=SOCKET_PATH)
    connect_and_handle_client(server=global_server)
