import socket
import threading
import select
import sys


port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", port))

s.listen()
print("Waiting for a connection, Server Started")




def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])
    

def threaded_client(conn, conn2):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:

            data = (conn.recv(2048))
            reply = data.decode('utf-8')
            print("decoded")
            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)

            conn2.send(str.encode(reply))
        except:
            Break

    print("Lost connection")
    conn.close()



    

conn, addr = s.accept()
conn2, addr2 = s.accept()
thread1 = threading.Thread(target=threaded_client, args=(conn, conn2, ))
thread2 = threading.Thread(target=threaded_client, args=(conn2, conn, ))
thread1.start()
thread2.start()
conn2.send(str.encode("p2,p2"))


