import os
import sys
import json
import time
import socket
import select
import struct
import threading
import file_lock

SITE_LOCK_FILE = "/tmp/Site_lock"
# Data header length, 4 bytes
DATA_HEADER_LEN = 4
# Socket path
SITE_SOCKET_PATH = "/tmp/Site_socket"
# Max connection
BACKLOG = 5
# Message length
BUFFER_SIZE = 4096

def create_server_socket(path: str):
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
    if os.path.exists(SITE_SOCKET_PATH):
        os.unlink(path)
    server.bind(path)
    server.listen(BACKLOG)
    return server

def handle_request(client: socket.socket):
    print("handle request")
    response = '{"GENERAL-INFO": {"operate": "request", "timestam": "2024-11-01T00:00:00.000"}, "TELESCOPE-INFO": {"tel_id": xxx, "mode": "image","filter": "g","exptime":60,"nframe": 1}, "TARGET -INFO": {"targ_id": xxx, "ra_targ": xxx, "ra_dec": xxx }}'
    pass
def handle_push(client: socket.socket):
    print("handle push")
    pass
def handle_client(client: socket.socket):
    while True:
        message_len = client.recv(DATA_HEADER_LEN)
        if not message_len:
            print("Failed to receive data")
            file_lock.re_lock(SITE_LOCK_FILE)
            break
        message_len = struct.unpack('I',message_len)[0]
        message = client.recv(message_len).decode('utf-8')
        message_json = json.loads(message)
        print(f"site server rec: {message_json}")
        if message_json.get('GENERAL-INFO', {}).get('operate') == 'request':
            threading.Thread(target=handle_request, args=(client,), daemon=True).start()
        elif message_json.get('GENERAL-INFO', {}).get('operate') == 'push':
            threading.Thread(target=handle_push, args=(client,), daemon=True).start()
        
        
def connect_and_handle_client(server: socket.socket):
    while True:
        client,client_addr = server.accept()
        print(f"site connected")
        threading.Thread(target=handle_client,args=(client,), daemon=True).start()
def start_site_server():
    site_lock = file_lock.ac_lock(lock_file=SITE_LOCK_FILE)
    if not site_lock:
        print("Site lock has been used")
        sys.exit(1)
    site_server = create_server_socket(path=SITE_SOCKET_PATH)
    connect_and_handle_client(server=site_server)
    site_server.close()
    
start_site_server()