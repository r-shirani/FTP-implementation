import socket
import os
import time

host = '127.0.0.1' #local host
control_port = 21  #standard control port
data_port = 2021   #can be 2021, 2121, 3000, etc for transferring data

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
