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

    def authenticate_user(username, password):
        if username and users[username]["password"]==password:
            return True
        return False
      
    def client_requests(self,control_connection,data_connection):
        #welcoming message
        control_connection.send(b"** Welcome to FTP Server **\r\n")
        username = None

        #receiving client's requests until client quits
        while True:
            command = control_connection.recv(1024).decode().strip()
            if not command:
                break

            #split request and argument
            request, *args = command.split()
            arg = " ".join(args)
            username=None
            password=None
          
            #user wants to enter the system
            if request.upper()=="USER":
                if arg in users:
                    username = arg
                    control_connection.send(b"    *331* Username accepted enter password.\r\n")
                else:
                    control_connection.send(b"    *530* Invalid username.\r\n")
                  
            #user's password
            elif request.upper()=="PASS":
                password=arg
                if(self.authenticate_user(username,password)):
                    self.authenticate_user=True
                    control_connection.send(b"    *230* Login successful.\r\n")
                else:
                    control_connection.send(b"    *530* Invalid password.\r\n")
                  
            #Sending a list of files and directories in the current directory from the server to the client
            elif request.upper()=="LIST":
                if not self.user_authenticated:
                    control_connection.send(b"    *530* Please login first.\r\n")
                elif not users[username]["read_access"]:
                    control_connection.send(b"    *530* You do not have read access.\r\n")
                else:
                    #path can be the current path or a certain path
                    path = arg if arg else self.current_dir
                    try:
                        control_connection.send(b"    *125* Opening data connection.\r\n")
                        files = os.listdir(path)#list of files in the path
                        file_info_list = []#empty list to save info
                        for file in files:
                          file_path = os.path.join(path, file)#creat file path
                          size = os.path.getsize(file_path)#size of file
                          time = time.ctime(os.path.getmtime(file_path))#creating file'time  
                          file_info_list.append(f"{time} | {file} | {size} bytes ")

                        file_list = "\n".join(file_info_list)
                        control_connection.sendall(file_list.encode())
                        control_connection.send(b"\n    *226* Transfer complete.\r\n")
                    except FileNotFoundError:
                        control_connection.send(b"    *550* Path not found.\r\n")
                      
            #download a file from the server
            elif request.upper()=="RETR":
                if not self.user_authenticated:
                    control_connection.send(b"    *530* Please login first.\r\n")
                elif not users[username]["read_access"]:
                    control_connection.send(b"    *530* You do not have read access.\r\n")    
                else:
                    try:
                        #open the certain file(arg) in reading binary mode
                        with open(arg, "rb") as file:
                            control_connection.send(b"    *150* Opening data connection.\r\n")
                            data_connection.send(file.read())#read all file and send to client via data_connection
                            control_connection.send(b"    *226* Transfer complete.\r\n")
                    except FileNotFoundError:
                        control_connection.send(b"    *550* File not found.\r\n")
                      
            #upload a file to the server
            elif request.upper()=="STOR":
                if not self.user_authenticated:
                    control_connection.send(b"    *530* Please login first.\r\n")
                elif not users[username]["write_access"]:
                    control_connection.send(b"    *530* You do not have write access.\r\n")    
                else:
                    try:
                        control_connection.send(b"    *150* Ready to receive file.\r\n")
                        with open(arg, "wb") as file:#open a file with arg name in writing binary mode
                                data = data_connection.recv(1024*1024*10)#receive file info in binary
                                file.write(data)#write the received data from a client in the file
                        control_connection.send(b"    *226* Transfer complete.\r\n")
                    except Exception:
                        control_connection.send(b"    *550* Error saving file.\r\n")
                      
            #delete a file from the server
            elif request.upper()=="DELE":
              if not self.user_authenticated:
                    control_connection.send(b"    *530* Please login first.\r\n")
                elif not users[username]["delete_access"]:
                    control_connection.send(b"    *530* You do not have delete access.\r\n")    
                else:
                    try:
                        os.remove(arg)#remove the file
                        control_connection.send(b"    *250* File deleted successfully.\r\n")
                    except FileNotFoundError:
                        control_connection.send(b"    *550* File not found.\r\n")
              
            # make a new directory in the server
            elif request.upper()=="MKD":
                if not self.user_authenticated:
                    control_connection.send(b"    *530* Please login first.\r\n")
                elif not users[username]["create_access"]:
                    control_connection.send(b"    *530* You do not have create access.\r\n")    
                else:
                    try:
                        os.makedirs(arg)
                        #if makedirs(org) was successful, send data by converting them to byte with .encode()
                        control_connection.send(f"    *257* \"{arg}\" directory created.\r\n".encode())
                    except Exception as e:
                        #if makedirs(arg) wasn't successful, send the e exception to the client
                        control_connection.send(f"    *550* Failed to create directory: {e}\r\n".encode())
                      
            #delete a directory from the server
            elif request.upper()=="RMD":
                if not self.user_authenticated:
                    control_connection.send(b"    *530* Please login first.\r\n")
                elif not users[username]["delete_access"]:
                    control_connection.send(b"    *530* You do not have delete access.\r\n")    
                else:
                    try:
                        os.rmdir(arg)
                        control_connection.send(f"    *250* Directory \"{arg}\" removed successfully.\r\n".encode())
                    except Exception as e:
                        control_connection.send(f"    *550* Failed to remove directory: {e}\r\n".encode())
              
            #get the current server directory path
            elif request.upper()=="PWD":
                if not self.user_authenticated:
                    control_connection.send(b"    *530* Please login first.\r\n")
                elif not users[username]["read_access"]:
                    control_connection.send(b"    *530* You do not have read access.\r\n")    
                else:
                    control_connection.send(f"    *257* \"{self.current_dir}\"\r\n".encode())
                  
            #change the current directory to a certain directory
            elif request.upper()=="CWD":
                if not self.user_authenticated:
                    control_connection.send(b"    *530* Please login first.\r\n")
                elif not users[username]["write_access"]:
                    control_connection.send(b"    *530* You do not have write access.\r\n")        
                else:
                    try:
                        os.chdir(arg)#change the current directory to arg directory
                        self.current_dir = os.getcwd()#update the current directory
                        control_connection.send(b"    *250* Directory changed.\r\n")
                    except FileNotFoundError:
                        control_connection.send(b"    *550* Directory not found.\r\n")
              
            #change the directory to the parent directory
            elif request.upper()=="CDUP":
                break
            #disconnecting the client from the server
            elif request.upper()=="QUIT":
                break
            #no requests found
            else:
                break
        
        #close the connections
        control_connection.close()
        data_connection.close()


