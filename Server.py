import socket
import os
import time

host = '127.0.0.1'     #local host
control_port = 21      #standard control port
data_port = 2021       #can be 2021, 2121, 3000, etc for transferring data
BASE_DIR = os.getcwd() #current directory

users ={
  "user1":  {"password":"00000001","read_access":False, "write_access":False, "delete_access":False, "create_access":False },
  "user2":  {"password":"00000002","read_access":False, "write_access":False, "delete_access":False, "create_access":True  },
  "user3":  {"password":"00000003","read_access":False, "write_access":False, "delete_access":True,  "create_access":False },
  "user4":  {"password":"00000004","read_access":False, "write_access":False, "delete_access":True,  "create_access":True  },
  "user5":  {"password":"00000005","read_access":False, "write_access":True,  "delete_access":False, "create_access":False },
  "user6":  {"password":"00000006","read_access":False, "write_access":True,  "delete_access":False, "create_access":True  },
  "user7":  {"password":"00000007","read_access":False, "write_access":True,  "delete_access":True,  "create_access":False },
  "user8":  {"password":"00000008","read_access":False, "write_access":True,  "delete_access":True,  "create_access":True  },
  "user9":  {"password":"00000009","read_access":False, "write_access":False, "delete_access":False, "create_access":False },
  "user10": {"password":"00000010","read_access":False, "write_access":False, "delete_access":False, "create_access":True  },
  "use11":  {"password":"00000011","read_access":True,  "write_access":False, "delete_access":True,  "create_access":False },
  "user12": {"password":"00000012","read_access":True,  "write_access":False, "delete_access":True,  "create_access":True  },
  "user13": {"password":"00000013","read_access":True,  "write_access":True,  "delete_access":False, "create_access":False },
  "user14": {"password":"00000014","read_access":True,  "write_access":True,  "delete_access":False, "create_access":True  },
  "user15": {"password":"00000015","read_access":True,  "write_access":True,  "delete_access":True,  "create_access":False },
  "user16": {"password":"00000016","read_access":True,  "write_access":True,  "delete_access":True,  "create_access":True  },
}

class Server:
    #initial value of constructor
    def __init__(self, host, control_port, data_port):
        self.host = host
        self.control_port = control_port
        self.data_port = data_port
        self.current_dir = BASE_DIR
        self.user_authenticated = False

    #begining the FTP server
    def start(self):
        #creating the control socket with IPv4 and TCP protocol
        control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to the host='127.0.01' with control_port=21
        control_socket.bind((self.host, self.control_port))
        #control socket is listening limited to one user(changeable)
        control_socket.listen(1)
        #printing that server is listening on control port
        print(f"Server started on {self.host} Port:{self.control_port}")
        
        #creating a data socket
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect the socket to the host with data port
        data_socket.bind((self.host, self.data_port))
        #data socket is listening limited to one user(changeable)
        data_socket.listen(1)
        #printing that server is listening on data port
        print(f"Data connection on {self.host} Port:{self.data_port}")
        
        #always accepting new connections
        while True:
            #accepting the incoming connection from the control socket
            control_connection, addr = control_socket.accept()
            print(f"Control connection established with {addr}")
            #accepting the incoming connection from the data socket
            data_connection, _ = data_socket.accept()
            print("Data connection established.")
            #processing client's requests
            self.client_requests(control_connection, data_connection)

