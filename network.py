import pickle
import socket
from settings import CLIENT_IP, CLIENT_PORT

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = CLIENT_IP
        self.port = CLIENT_PORT
        self.player = self.connect()
        
    @property
    def addr(self):
        return (self.server, self.port)
    
    def connect(self):
        self.client.connect(self.addr)
        return int(self.client.recv(2048*8).decode())
    
    def send(self, data):
        self.client.send(data)
        return pickle.loads(self.client.recv(2048*8))
