# FTP-implementation
implementation of the FTP protocol

**Project Objective**  
The main objective of this project in the networking course is to develop a file transfer system that allows users to transfer files between clients and the server. Students will gain familiarity with key concepts such as network communication, socket programming, FTP protocol, file management, network security, authentication, and access control. They will also gain practical experience working with network and security tools. This project not only enhances students' technical skills but also deepens their understanding of file transfer systems' structure, functionality, and related security challenges.  

**FTP Command Descriptions**  

1. **USER**  
   - Used to send the username to the server, allowing the server to identify the user.  
   - Status codes:  
     - **331**: Username accepted; waiting for password.  
     - **530**: Invalid username; please try again.  

2. **PASS**  
   - Sends the password to the server for authentication.  
   - Status codes:  
     - **230**: Successful login.  
     - **530**: Invalid password; please try again.  

3. **LIST**  
   - Sends a list of files and directories in the current server directory to the client, including details like name, size, permissions, and creation date.  
   - Optional: Specify a pathname to retrieve details about a specific path or directory.  
   - Example: `LIST /path/to/directory`  
   - Status codes:  
     - **125**: Preparing to transfer the list.  
     - **226**: List transferred successfully.  

4. **RETR**  
   - Download a file from the server.  
   - Example: `RETR /path/to/file`  
   - Status codes:  
     - **150**: Preparing to transfer file.  
     - **226**: File transfer successful.  

5. **STOR**  
   - Uploads a file to the server. If a file with the same name already exists, the new file replaces the old one.  
   - Example: `STOR /client-path /server-path`  
   - Status codes:  
     - **150**: Preparing to receive file.  
     - **226**: File uploaded successfully.  

6. **DELE**  
   - Deletes a file from the server.  
   - Example: `DELE /path/to/file`  
   - Status codes:  
     - **250**: File deleted successfully.  
     - **550**: File not found or cannot be deleted.  

7. **MKD**  
   - Creates a new directory on the server.  
   - Example: `MKD /path/to/new/dir`  
   - Status codes:  
     - **257**: Directory created successfully.  
     - **550**: Unable to create a directory.  

8. **RMD**  
   - Deletes a directory from the server.  
   - Example: `RMD /path/to/dir`  
   - Status codes:  
     - **250**: Directory deleted successfully.  
     - **550**: Directory not found or cannot be deleted.  

9. **PWD**  
   - Retrieves the current server directory path.  
   - Status codes:  
     - **257**: Current directory path displayed successfully.  

10. **CWD**  
    - Change the current directory to the specified one.  
    - Example: `CWD /dir`  
    - Status codes:  
      - **250**: Directory changed successfully.  
      - **550**: Directory not found.  

11. **CDUP**  
    - Changes the current directory to the parent directory. For example, running `CDUP` in `/home/user/public` will change the path to `/home/user`.  
    - Status codes:  
      - **250**: Successfully moved to the parent directory.  

12. **QUIT**  
    - Disconnects the user from the server. If a file transfer is in progress, it should not be interrupted.  
    - Status codes:  
      - **221**: Disconnection successful.

**Relative and Absolute Paths**  

In FTP commands dealing with paths (such as `CWD`, `MKD`, `RMD`, `RETR`, `STOR`, etc.), paths can be defined in two ways:  

- **Relative Path:** A path defined relative to the current directory. For example, if the user is in `/home/user/` and wants to access the `documents/` subdirectory, they can use the relative path `documents/`.  

- **Absolute Path:** A path that starts from the root directory of the server's file system and fully specifies the location. For example, `/home/user/documents/` is an absolute path.  

---

**Error Management**  

Error management in FTP ensures proper execution of operations. The server returns specific status codes indicating the error type if a command fails.  

- **Example Errors:**  
  - If the user tries to access a nonexistent directory using `CWD`, the server returns code **550**, indicating the directory does not exist.  
  - When deleting or moving a file, if the file is missing or insufficient permissions exist, the server sends an appropriate error message.  

---

**File Transfer Management Using Separate Connections**  

In FTP, data transfers (such as uploading or downloading files) are done using a separate connection called the **data connection**:  

- **Control Connection:** Used for sending commands and responses.  
- **Data Connection:** Opened temporarily for actual file transfers and closed after completion.  

This separation allows the client and server to manage commands and files independently and simultaneously, preventing control-data interferences. It is a key reason for FTP's flexibility and efficiency, especially when transferring large files or using multiple commands concurrently.  

---

**File Transfer System Components**  

1. **Server**  
   The file server manages files and directories and responds to client requests. Its responsibilities include:  

   - Storing and managing files and directories.  
   - Authenticating users through username and password validation.  
   - Controlling access based on defined permissions and access levels.  
   - Creating, deleting, and modifying files and directories upon authorized requests.  
   - Sending or receiving files through data connections.  

2. **Client**  
   The client system allows users to interact with the file server and perform various tasks such as:  

   - Sending requests to the server to access files or directories.  
   - Managing files using FTP commands like `STOR`, `RETR`, `DELE`, or `CWD`.  
   - Managing file transfers, authentication, and executing various operations.  

---

**Access Management**  

Access management is critical in an FTP system to ensure users can only access authorized files and directories. Proper access control includes:  

1. **Authentication:**  
   - When a user connects using `USER` and `PASS`, the server validates login credentials.  
   - If authentication fails, the user cannot access FTP services or resources.  

2. **Access Levels:**  
   - After authentication, access is restricted based on defined permissions, which can include:  
     - **Read Access:** Users can view and download files but cannot modify them.  
     - **Write Access:** Users can upload and edit files.  
     - **Delete Access:** Users can delete files and directories.  
     - **Create Access:** Users can create new directories.

**Security in Network Protocols**  

Data encryption in network protocols is essential to ensure secure communication and prevent unauthorized access. Two primary protocols used for this purpose are **SSL (Secure Sockets Layer)** and **SSH (Secure Shell)**. Although they operate differently, both aim to secure network communications and protect data from eavesdropping and unauthorized access.  

**Threat Example:**  
In FTP, usernames and passwords are sent in plain text, making them vulnerable to **man-in-the-middle attacks**. To mitigate this risk, secure protocols like **FTPS** and **SFTP** were developed.  

---

### **SFTP (SSH File Transfer Protocol)**  
- **Definition:** A secure file transfer protocol that uses **SSH** for encryption.  
- **Key Characteristics:**  
  - Completely different from FTP and FTPS.  
  - Encrypts data, commands, and credentials over a single, secure connection.  
  - More versatile and secure compared to FTPS.  
- **Use Cases:** Widely used for secure file transfers, remote system administration, and backup services.  
