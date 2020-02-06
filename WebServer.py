#!/usr/bin/python3

#This works running python3.7
# Jack Drury



import sys
from socket import *
import os.path
import re


#grab the command line argument for the port
serverPort = int(sys.argv[1])



#AF_INET implies that we are using IPV4
# SOCK_STREAM implies we are using TCP
serverSocket = socket(AF_INET, SOCK_STREAM)


#taking the command line port argument and
#binding servers socket to that port
# only visible to clients on the same machine
serverSocket.bind(('localhost',serverPort))

serverSocket.listen(1)

while 1:
    connectionSocket, addr = serverSocket.accept()
    req = connectionSocket.recv(1024)
    req = req.decode()
    #grab whatever comes after the GET in the request
    #i.e. first thing surrounded by whitespace
    link = (re.search(' [^ ]+ ', req))[0][1:-1]
    print(link)
    if link =='/':
        link = 'index.html'
    else:
        link = link[1:]

    if os.path.exists(link):
        f=open(link,'rb')
        html_text = f.read()
        response =b'HTTP/1.1 200 OK\r\n\r\n'
        connectionSocket.send(response)
        connectionSocket.send(html_text)
        connectionSocket.close()
        f.close()
        

    else:
#        print('need to return 404')
        response =b'HTTP/1.1 404 Not Found.\r\n\r\n'
        connectionSocket.send(response)
        connectionSocket.send(b'404 nothing found here. If looking for Garfield try /index.html')
        connectionSocket.close()
