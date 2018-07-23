from multiprocessing import Process,Pipe
import time

def hello(child_conn):
    msg = "Hello"
    child_conn.send(msg)
    child_conn.close()

def goodbye(child_conn):
    msg = "goodbye"
    child_conn.send(msg)
    child_conn.close()

