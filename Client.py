import socket

def Client():
    host = '127.0.0.1' #local host
    control_port = 21  #standard control port
    data_port = 2021   #can be 2021, 2121, 3000, etc for transferring data

    #TCP socket for connecting to the server(IPv4,TCP)
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #connect the client to the server for transferring the commands
    control_socket.connect((host, control_port))

    #do the same things for transferring data
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((host, data_port))

    #send commands to the server and get the result
    def send_command(command):
        control_socket.send(f"{command}\r\n".encode())# send by converting the string to the bytes
        result = control_socket.recv(1024).decode()#get the result and convert max 1024 byte to string
        print(result)
        return result
    
    #welcoming message with code=220
    print(control_socket.recv(1024).decode())

    while True:
        command = input("FTP> ")#get the command from user
        if command.upper() == "QUIT":
            send_command(command)
            break
        elif command.upper().startswith("RETR"): #for downloading a file
           result = send_command(command)        #get the result
           if result.startswith('    *150*'):    #preparing to transfer the file 
             filename = command.split()[1]       #file name
             with open(filename, "wb") as file:  #open file in writting mode
                  data = data_socket.recv(1024)  #receive the file via data socket
                  file.write(data)  #write the data in the file
             print(control_socket.recv(1024).decode()) #print the result from the server
        elif command.upper().startswith("STOR"): #for uploading a file
           result = send_command(command)        #get the result
           if result.startswith('    *150*'):    #preparing the server to get the file
               filename = command.split()[1]     #file name
               with open(filename, "rb") as file:#open a file in reading mode
                       data_socket.send(file.read())   #send a chunk of data to the server
        else:
            send_command(command)

    #close the connection
    control_socket.close()
    data_socket.close()

if __name__ == "__main__":
    Client()
  
