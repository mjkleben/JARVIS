from multiprocessing import Process,Queue,Pipe
from test1 import hello, goodbye

if __name__ == '__main__':
    parent_conn,child_conn = Pipe()
    p = Process(target=hello, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "Hello"