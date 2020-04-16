# -*- coding: UTF-8 -*-
# 文件名：Client.py

import time
import queue
import socket
import threading

class MyChat_Client(object):
    def __init__(self, addr="127.0.0.1", port=9999):
        """
        :param addr:客户端地址
        :param port:客户端端口
        """
        self.addr = addr
        self.port = port
        self.username = None
        self.queue = queue.Queue()
        self.status = True
        self.loginStatus = False
        self.loginBack = None
        self.registerBack = None
        self.userlist = []
        self.usermsg = []
        self.sysmsg = []

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #创建TCP Socket

        try:
            self.s.connect((self.addr, self.port))
            self.s.settimeout(0.000001)
        except socket.error as err:
            if err.errno == 10061:
                print("Connection with {addr}:{port} refused".format(addr=self.addr, port=self.port))
                return
            else:
                raise
        else:
            print("initial successfully!")

    def register(self, name, password):
        """
        注册账号
        :param name:要注册的账号
        :param password:密码
        """
        self.s.send(str({"type": "register",
                                "name": name,
                                "password": password,
                                "time": time.time()}).encode())

    def login(self, name, password):
        """
        使用账号密码登录
        :param name: 用户账号
        :param password: 密码
        """
        self.username = name
        self.s.send(str({"type": "login",
                                "name": name,
                                "password": password,
                                "time": time.time()}).encode())

    def send_Msg(self, msg_send, destname, mtype = "msg", fname = ""):
        """
        发送消息
        :param msg_send: 要发送的消息
        :param destname: 发送对象的用户名
        """
        a = str({"type": "usermsg",
                        "mtype": mtype,
                        "destname": destname,
                        "fname": fname,
                        "name": self.username,
                        "time": time.time(),
                        "msg": msg_send}).encode()
        constlen = len(a)

        self.s.send(str({"type": "msglen",
                                "destname": destname,
                                "name": self.username,
                                "len": constlen}).encode())
        print("send     ")
        print(str({"type": "msglen",
                          "destname": destname,
                          "name": self.username,
                          "len": constlen}).encode())
        time.sleep(0.01)
        self.s.send(a)

    def receive_msg(self):
        """
        接收消息
        """
        while self.status:
            try:
                msg_recv = eval(self.s.recv(1024))
            except socket.timeout:
                pass
            except socket.error as err:
                if err.errno == 10053:
                    print("Software caused connection abort ")
                    self.status = False
            else:
                if msg_recv["type"] == "msglen":
                    self.queue.put(msg_recv)
                    print("recv             ")
                    length = msg_recv["len"]
                    mlen = 0
                    while msg_recv["type"] != "usermsg":
                        try:
                            msg_recv = "".encode()

                            while mlen < length:
                                try:
                                    msg_recv_ = self.s.recv(length)
                                    msg_recv = msg_recv + msg_recv_
                                    mlen = mlen + len(msg_recv_)
                                    msg_recv = eval(msg_recv)
                                    time.sleep(length * 0.00000001)
                                except socket.timeout:
                                    continue
                                except SyntaxError:
                                    continue
                                else:
                                    break
                        except socket.timeout:
                            continue
                        except socket.error as err:
                            if err.errno == 10053:
                                print("Software caused connection abort ")
                                self.status = False
                    self.queue.put(msg_recv)
                    print("recv             ")
                else:
                    self.queue.put(msg_recv)
                    print("recv             ")

    def handle_msg(self):
        """
        处理收到的消息
        """
        while True:
            msg = self.queue.get()
            print("handle              ",end='')

            if msg["type"] == "loginBack":
                self.loginBack = msg
                if msg["info"] == "loginSucc":
                    self.userlist = msg["userlist"]
            elif msg["type"] == "rgtrBack":
                self.registerBack = msg
            elif msg["type"] == "usermsg":
                self.usermsg.append(msg)
            elif msg["type"] == "sysmsg":
                self.sysmsg.append(msg)

    def main(self):
        """"""
        func1 = threading.Thread(target=self.receive_msg)
        func2 = threading.Thread(target=self.handle_msg)
        func1.start()
        func2.start()

    def __del__(self):
        self.s.close()

if __name__ == '__main__':
    client = MyChat_Client(addr="127.0.0.1", port=14396)
    client.main()
    client.login("0", "0")
    # with open("./images/style/a.jpg", mode='rb') as f:
    #     r = f.read()
    #     image_str = base64.encodebytes(r).decode("utf-8")
    #     print(image_str)
    # client.send_Msg(image_str,"all","msg")


