#!/usr/bin/python
import socket

s = socket.socket()
host = socket.gethostname()
port = 12221
s.bind((host, port))

s.listen(5)
c = None

while True:
   if c is None:
       c, addr = s.accept()
       print('Got connection from', addr)
   else:
       print(c.recv(1024).decode("utf-8"))


