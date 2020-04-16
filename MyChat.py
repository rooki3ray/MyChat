# -*- coding: UTF-8 -*-
# 文件名：MyChat.py

import os
import sys
import time
import base64
import threading
import webbrowser
from PyQt5.QtCore import Qt
from Client import MyChat_Client
from PyQt5 import QtCore, QtGui, QtWidgets

class loginWindow(QtWidgets.QDialog):
    def __init__(self):
        super(loginWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("LoginWindow")
        self.setStyleSheet("#LoginWindow{border-image:url(./images/style/login/login.png);}")
        self.setWindowIcon(QtGui.QIcon("./images/style/icon.png"))
        self.resize(432, 300)

        self.loginButton = QtWidgets.QPushButton(self)      #登录按钮
        self.loginButton.setGeometry(QtCore.QRect(118, 243, 220, 35))
        self.loginButton.setObjectName("login")
        self.loginButton.setStyleSheet("border-image:url(./images/style/login/loginbutton.png);")
        self.loginButton.clicked.connect(self.loginButtonClicked)

        self.registerButton = QtWidgets.QPushButton(self)   #注册按钮
        self.registerButton.setGeometry(QtCore.QRect(12, 250, 65, 25))
        self.registerButton.setObjectName("register")
        self.registerButton.setStyleSheet("border:none;")  #无边框
        self.registerButton.setCursor(Qt.PointingHandCursor)
        self.registerButton.clicked.connect(self.registerButtonClicked)

        self.userName = QtWidgets.QLineEdit(self)       #账号
        self.userName.setGeometry(QtCore.QRect(118, 140, 220, 28))
        self.userName.setObjectName("username")
        self.userName.setPlaceholderText("请输入账号")
        self.userName.setMaxLength(20)

        self.password = QtWidgets.QLineEdit(self)       #密码
        self.password.setGeometry(QtCore.QRect(118, 170, 220, 28))
        self.password.setObjectName("password")
        self.password.setPlaceholderText("请输入密码")
        self.password.setMaxLength(20)
        self.password.setEchoMode(self.password.Password)

        self.constuserName = QtWidgets.QLineEdit(self)      #文本输入框前的提示
        self.constuserName.setGeometry(QtCore.QRect(42, 140, 75, 28))
        self.constuserName.setStyleSheet("border:none;")
        self.constuserName.setReadOnly(True)
        self.constpassword = QtWidgets.QLineEdit(self)
        self.constpassword.setGeometry(QtCore.QRect(42, 170, 75, 28))
        self.constpassword.setStyleSheet("border:none;")
        self.constpassword.setReadOnly(True)

        self.loginError = QtWidgets.QLineEdit(self)         #登录信息提示框
        self.loginError.setGeometry(QtCore.QRect(118, 205, 220, 28))
        self.loginError.setStyleSheet("background-color: rgb(255, 25, 255, 60);border:none;")
        self.loginError.setAlignment(QtCore.Qt.AlignCenter)
        self.loginError.setReadOnly(True)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("LoginWindow", "MyChat"))
        self.loginButton.setText(_translate("LoginWindow", "登录"))
        self.registerButton.setText(_translate("LoginWindow", "注册账号"))
        self.constuserName.setText(_translate("LoginWindow", "MyChat账号："))
        self.constpassword.setText(_translate("LoginWindow", "MyChat密码："))
        self.loginError.setText(_translate("registerWindow", "欢迎使用MyChat!"))

    def loginButtonClicked(self):
        '''
        点击登录按钮触发事件
        '''
        Username = self.userName.text()
        Password = self.password.text()
        if len(Username) == 0 or len(Password) == 0:
            self.loginError.setText("您还没有输入账号或密码！")
        else:
            client.login(Username, Password)
            while client.loginBack == None:
                pass
            flag = False
            if client.loginBack["info"] == "loginSucc":
                self.loginError.setStyleSheet("background-color: rgb(100, 255, 0, 60);border:none;")
                self.loginError.setText("登陆成功")
                self.hide()
                self.chatWindow = chatWindow(Username)      #登录成功，调出聊天界面
                self.chatWindow.show()
                self.chatWindow.main()
            elif client.loginBack["info"] == "loginFail":
                self.loginError.setText("账号或密码错误！请重新输入！")
            else:
                self.loginError.setText("该账号已经登录！")
            client.loginBack = None

    def registerButtonClicked(self):
        '''
        点击注册账号按钮触发事件
        调出注册窗口
        '''
        self.registerWindow = registerWindow()
        self.registerWindow.show()

class registerWindow(QtWidgets.QDialog):
    def __init__(self):
        super(registerWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("registerWindow")
        self.setStyleSheet("#registerWindow{border-image:url(./images/style/register/register.png);}")
        self.setWindowIcon(QtGui.QIcon("./images/style/icon.png"))
        self.resize(360, 330)

        self.userName = QtWidgets.QLineEdit(self)       #用户名
        self.userName.setGeometry(QtCore.QRect(118, 80, 220, 28))
        self.userName.setObjectName("username")
        self.userName.setPlaceholderText("请输入账号")
        self.userName.setMaxLength(20)

        self.password = QtWidgets.QLineEdit(self)       #密码
        self.password.setGeometry(QtCore.QRect(118, 120, 220, 28))
        self.password.setObjectName("password")
        self.password.setPlaceholderText("请输入密码")
        self.password.setMaxLength(20)
        self.password.setEchoMode(self.password.Password)

        self.passwordAgain = QtWidgets.QLineEdit(self)  #密码确认
        self.passwordAgain.setGeometry(QtCore.QRect(118, 160, 220, 28))
        self.passwordAgain.setObjectName("passwordAgain")
        self.passwordAgain.setPlaceholderText("请再次输入密码")
        self.passwordAgain.setMaxLength(20)
        self.passwordAgain.setEchoMode(self.password.Password)

        self.constuserName = QtWidgets.QLineEdit(self)  #文本输入框前的提示
        self.constuserName.setGeometry(QtCore.QRect(30, 80, 87, 28))
        self.constuserName.setStyleSheet("border:none;")
        self.constuserName.setReadOnly(True)
        self.constpassword = QtWidgets.QLineEdit(self)
        self.constpassword.setGeometry(QtCore.QRect(30, 120, 87, 28))
        self.constpassword.setStyleSheet("border:none;")
        self.constpassword.setReadOnly(True)
        self.constpasswordAgain = QtWidgets.QLineEdit(self)
        self.constpasswordAgain.setGeometry(QtCore.QRect(30, 160, 87, 28))
        self.constpasswordAgain.setStyleSheet("border:none;")
        self.constpasswordAgain.setReadOnly(True)

        self.registerButton = QtWidgets.QPushButton(self)   #注册按钮
        self.registerButton.setGeometry(QtCore.QRect(118, 240, 220, 35))
        self.registerButton.setObjectName("register")
        self.registerButton.setStyleSheet("border-image:url(./images/style/register/registerbutton.png);")
        self.registerButton.clicked.connect(self.registerButtonClicked)

        self.registerError = QtWidgets.QLineEdit(self)      #注册信息提示框
        self.registerError.setGeometry(QtCore.QRect(118, 200, 220, 28))
        self.registerError.setStyleSheet("background-color: rgb(255, 25, 255, 60);border:none;")
        self.registerError.setAlignment(QtCore.Qt.AlignCenter)
        self.registerError.setReadOnly(True)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("registerWindow", "注册账号"))
        self.constuserName.setText(_translate("registerWindow", "MyChat账号："))
        self.constpassword.setText(_translate("registerWindow", "MyChat密码："))
        self.constpasswordAgain.setText(_translate("registerWindow", "再次输入密码："))
        self.registerButton.setText(_translate("registerWindow", "注册"))
        self.registerError.setText(_translate("registerWindow", "欢迎使用MyChat!"))

    def registerButtonClicked(self):
        '''
        点击注册账号按钮触发事件
        '''
        Username = self.userName.text()
        password = self.password.text()
        passwordAgain = self.passwordAgain.text()
        if len(Username) == 0 or len(password) == 0 or len(passwordAgain) == 0:
            self.registerError.setText("您还没有输入账号或密码！")
        elif password != passwordAgain:
            self.registerError.setText("您两次输入的密码不同！")
        else:
            client.register(Username, password)
            while client.registerBack == None:
                pass
            if client.registerBack["info"] == "rgtrSucc":
                self.registerError.setStyleSheet("background-color: rgb(100, 255, 0, 60);border:none;")
                self.registerError.setText("注册成功！请返回登录！")
            else:
                self.registerError.setText("该账号已存在！")
            client.registerBack = None

class chatWindow(QtWidgets.QDialog):
    def __init__(self, name):
        self.Username = name
        super(chatWindow, self).__init__()
        self.setupUi()
        try:
            os.mkdir(self.Username)         #创建对应的文件夹
        except FileExistsError:
            pass

    def setupUi(self):

        self.setObjectName("MyChat")
        self.setStyleSheet("#MyChat{border-image:url(./images/style/MyChat/MyChat.png);}")
        self.setWindowIcon(QtGui.QIcon("./images/style/icon.png"))
        self.resize(1005, 463)

        self.grprecvText = QtWidgets.QTextEdit(self)        #群聊消息框
        self.grprecvText.setGeometry(QtCore.QRect(200, 20, 670, 280))
        self.grprecvText.setObjectName("textRecv")
        self.grprecvText.setAlignment(QtCore.Qt.AlignTop)
        self.grprecvText.setStyleSheet("border-image:url(./images/style/MyChat/recvtext.png);")
        self.grprecvText.setReadOnly(True)

        self.prtrecvText1 = QtWidgets.QTextEdit(self)       #私聊消息框1
        self.prtrecvText1.setGeometry(QtCore.QRect(200, 20, 670, 280))
        self.prtrecvText1.setAlignment(QtCore.Qt.AlignTop)
        self.prtrecvText1.setStyleSheet("border-image:url(./images/style/MyChat/recvtext.png);")
        self.prtrecvText1.setReadOnly(True)
        self.prtrecvText1.hide()
        self.prtrecvText2 = QtWidgets.QTextEdit(self)       #私聊消息框2
        self.prtrecvText2.setGeometry(QtCore.QRect(200, 20, 670, 280))
        self.prtrecvText2.setAlignment(QtCore.Qt.AlignTop)
        self.prtrecvText2.setStyleSheet("border-image:url(./images/style/MyChat/recvtext.png);")
        self.prtrecvText2.setReadOnly(True)
        self.prtrecvText2.hide()
        self.prtrecvText3 = QtWidgets.QTextEdit(self)       #私聊消息框3
        self.prtrecvText3.setGeometry(QtCore.QRect(200, 20, 670, 280))
        self.prtrecvText3.setAlignment(QtCore.Qt.AlignTop)
        self.prtrecvText3.setStyleSheet("border-image:url(./images/style/MyChat/recvtext.png);")
        self.prtrecvText3.setReadOnly(True)
        self.prtrecvText3.hide()
        self.prtrecvText = [self.prtrecvText1, self.prtrecvText2, self.prtrecvText3]

        self.sendText = QtWidgets.QTextEdit(self)           #发送消息的编辑框
        self.sendText.setGeometry(QtCore.QRect(200, 335, 670, 85)) #
        self.sendText.setObjectName("textSend")
        self.sendText.setAlignment(QtCore.Qt.AlignTop)
        self.sendText.setStyleSheet("border-image:url(./images/style/MyChat/sendtext.png);")
        # self.sendText.keyPressEvent()
        self.destsend = 'all'

        self.sendtxtButton = QtWidgets.QPushButton(self)    #发送消息的按钮
        self.sendtxtButton.setGeometry(QtCore.QRect(765, 425, 65, 27))
        self.sendtxtButton.setObjectName("txtsendButton")
        self.sendtxtButton.setStyleSheet("border-image:url(./images/style/MyChat/sendtxtbutton.png);")
        self.sendtxtButton.clicked.connect(self.txtsendButtonClicked)

        self.searchButton = QtWidgets.QPushButton(self)  # 发送消息的按钮
        self.searchButton.setGeometry(QtCore.QRect(685, 425, 65, 27))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setStyleSheet("border-image:url(./images/style/MyChat/sendtxtbutton.png);")
        self.searchButton.clicked.connect(self.searchButtonClicked)

        self.friendlistHeader = QtWidgets.QTextEdit(self)   # 在线好友列表头
        self.friendlistHeader.setGeometry(QtCore.QRect(870, 120, 125, 25))
        self.friendlistHeader.setObjectName("friendlistHeader")
        self.friendlistHeader.setAlignment(QtCore.Qt.AlignTop)
        self.friendlistHeader.setStyleSheet("border-image:url(./images/style/MyChat/sendtext.png);")
        self.friendlistHeader.setReadOnly(True)

        self.friendlist = QtWidgets.QListWidget(self)       #在线好友列表
        self.friendlist.setGeometry(QtCore.QRect(870, 140, 125, 280))
        self.friendlist.setObjectName("friendlist")
        self.friendlist.setStyleSheet("border-image:url(./images/style/MyChat/friendlist.png);")
        self.friendlist.doubleClicked.connect(self.friendlistDoubleClicked)
        self.friendlist.addItems(client.userlist)

        self.grpButton = QtWidgets.QPushButton(self)        #将聊天框切换至群聊的按钮
        self.grpButton.setGeometry(QtCore.QRect(0, 0, 200, 62))
        self.grpButton.setObjectName("grpButton")
        self.grpButton.setStyleSheet("border-image:url(./images/style/MyChat/nowfriendbutton.png);")
        self.grpButton.clicked.connect(self.grpbuttonClicked)

        self.destprtbutton = {}
        self.prtbutton1 = QtWidgets.QPushButton(self)       #将聊天框切换至私聊1的按钮
        self.prtbutton1.setGeometry(QtCore.QRect(0, 62, 200, 62))
        self.prtbutton1.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
        self.prtbutton1.clicked.connect(self.prtbutton1Clicked)
        self.prtbutton2 = QtWidgets.QPushButton(self)       #将聊天框切换至私聊2的按钮
        self.prtbutton2.setGeometry(QtCore.QRect(0, 124, 200, 62))
        self.prtbutton2.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
        self.prtbutton2.clicked.connect(self.prtbutton2Clicked)
        self.prtbutton3 = QtWidgets.QPushButton(self)       #将聊天框切换至私聊3的按钮
        self.prtbutton3.setGeometry(QtCore.QRect(0, 186, 200, 62))
        self.prtbutton3.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
        self.prtbutton3.clicked.connect(self.prtbutton3Clicked)
        self.buttontotext = {}                              #按钮和聊天框的字典
        self.buttontotext[self.prtbutton1] = self.prtrecvText1
        self.buttontotext[self.prtbutton2] = self.prtrecvText2
        self.buttontotext[self.prtbutton3] = self.prtrecvText3
        self.prtbutton = [self.prtbutton1, self.prtbutton2, self.prtbutton3]

        self.fileButton = QtWidgets.QPushButton(self)       #发送文件的按钮
        self.fileButton.setGeometry(QtCore.QRect(200, 300, 35, 35))
        self.fileButton.setStyleSheet("border-image:url(./images/style/MyChat/filebutton.png);")
        self.fileButton.clicked.connect(self.fileButtonClicked)

        self.imageButton = QtWidgets.QPushButton(self)      #发送图片的按钮
        self.imageButton.setGeometry(QtCore.QRect(235, 300, 35, 35))
        self.imageButton.setStyleSheet("border-image:url(./images/style/MyChat/imagebutton.png);")
        self.imageButton.clicked.connect(self.imageButtonClicked)

        self.emojiButton = QtWidgets.QPushButton(self)      # 发送表情的按钮
        self.emojiButton.setGeometry(QtCore.QRect(270, 300, 35, 35))
        self.emojiButton.setStyleSheet("border-image:url(./images/style/MyChat/emojibutton.png);")
        self.emojiButton.clicked.connect(self.emojiButtonClicked)

        self.fileselect = QtWidgets.QFileDialog(self)       #文件选择界面
        self.fileselect.setGeometry(QtCore.QRect(248, 341, 500, 62))

        self.emoji = QtWidgets.QTableWidget(self)           #表情列表
        self.emoji.setGeometry(QtCore.QRect(270, 175, 120, 120))
        self.emoji.verticalHeader().setVisible(False)       # 隐藏垂直表头
        self.emoji.horizontalHeader().setVisible(False)     # 隐藏水平表头
        self.emoji.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)   # 隐藏垂直滚动条
        self.emoji.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)     # 隐藏水平滚动条
        self.emoji.setColumnCount(3)
        self.emoji.setRowCount(3)
        label = []
        for i in range(9):
            icon = QtWidgets.QLabel()
            icon.setMargin(4)
            movie = QtGui.QMovie()
            movie.setScaledSize(QtCore.QSize(30, 30))
            movie.setFileName("./images/emoji/"+str(i)+".gif")
            movie.start()
            icon.setMovie(movie)
            self.emoji.setCellWidget(int(i/3), i%3, icon)
            self.emoji.setColumnWidth(i%3, 40)          # 设置列的宽度
            self.emoji.setRowHeight(int(i/3), 40)       # 设置行的高度
        self.emoji.hide()
        self.emoji.cellClicked.connect(self.emojiClicked)

        for i in self.prtbutton:
            self.destprtbutton[i] = None

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MyChat", "MyChat"))
        self.sendtxtButton.setText(_translate("txtsendButton", "发送"))
        self.searchButton.setText(_translate("searchButton", "百度搜索"))
        self.grpButton.setText(_translate("grpButton", "MyChat Group"))
        self.friendlistHeader.setText(_translate("friendlistHeader", "在线好友列表"))

    def txtsendButtonClicked(self):
        '''
        发送按钮响应
        '''
        text = self.sendText.toPlainText()
        if len(text):
            client.send_Msg(text, self.destsend)
            self.sendText.clear()

    def searchButtonClicked(self):
        '''
        搜索按钮响应
        '''
        text = self.sendText.toPlainText()
        if len(text):
            webbrowser.open("https://www.baidu.com/s?ie=UTF-8&wd=" + text, new=0, autoraise=True)
            self.sendText.clear()

    def friendlistDoubleClicked(self):
        '''
        好友列表双击添加私聊窗口
        :return:
        '''
        name = self.friendlist.currentItem().text()      #聊天对象
        if name == self.Username:
            return
        for i in self.prtbutton:
            if self.destprtbutton[i] == None or self.destprtbutton[i] == name:
                self.destprtbutton[i] = name
                i.setText(name)
                break

    def grpbuttonClicked(self):
        for i in self.prtrecvText:
            i.hide()
        self.grpButton.setStyleSheet("border-image:url(./images/style/MyChat/nowfriendbutton.png);")
        self.prtbutton1.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
        self.prtbutton2.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
        self.prtbutton3.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
        self.grprecvText.show()
        self.destsend = "all"
    def prtbutton1Clicked(self):
        if self.destprtbutton[self.prtbutton1] != None:
            for i in self.prtrecvText:
                i.hide()
            self.grpButton.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.prtbutton1.setStyleSheet("border-image:url(./images/style/MyChat/nowfriendbutton.png);")
            self.prtbutton2.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.prtbutton3.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.grprecvText.hide()
            self.buttontotext[self.prtbutton1].show()
            self.destsend = self.destprtbutton[self.prtbutton1]
    def prtbutton2Clicked(self):
        if self.destprtbutton[self.prtbutton2] != None:
            for i in self.prtrecvText:
                i.hide()
            self.grpButton.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.prtbutton1.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.prtbutton2.setStyleSheet("border-image:url(./images/style/MyChat/nowfriendbutton.png);")
            self.prtbutton3.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.grprecvText.hide()
            self.buttontotext[self.prtbutton2].show()
            self.destsend = self.destprtbutton[self.prtbutton2]
    def prtbutton3Clicked(self):
        if self.destprtbutton[self.prtbutton3] != None:
            for i in self.prtrecvText:
                i.hide()
            self.grpButton.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.prtbutton1.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.prtbutton2.setStyleSheet("border-image:url(./images/style/MyChat/friendbutton.png);")
            self.prtbutton3.setStyleSheet("border-image:url(./images/style/MyChat/nowfriendbutton.png);")
            self.grprecvText.hide()
            self.buttontotext[self.prtbutton3].show()
            self.destsend = self.destprtbutton[self.prtbutton3]

    def fileButtonClicked(self):
        # self.fileselect.show()
        fileinfo = self.fileselect.getOpenFileName(self, 'OpenFile', "e:/")
        print(fileinfo)
        filepath, filetype = os.path.splitext(fileinfo[0])
        filename = filepath.split("/")[-1]
        if fileinfo[0] != '':
            with open(fileinfo[0], mode='rb') as f:
                r = f.read()
                f.close()
            file_r = base64.encodebytes(r).decode("utf-8")
            client.send_Msg(file_r, self.destsend, filetype, filename)
        # while self.fileselect.getOpenFileName() == None:

    def imageButtonClicked(self):
        fileinfo = self.fileselect.getOpenFileName(self,'OpenFile',"e:/","Image files (*.jpg *.gif *.png)")
        print(fileinfo)
        filepath, filetype = os.path.splitext(fileinfo[0])
        filename = filepath.split("/")[-1]
        if fileinfo[0] != '':
            with open(fileinfo[0], mode='rb') as f:
                r = f.read()
                f.close()
            file_r = base64.encodebytes(r).decode("utf-8")
            client.send_Msg(file_r, self.destsend, filetype, filename)

    def emojiButtonClicked(self):
        self.emoji.show()

    def emojiClicked(self, row, column):
        client.send_Msg(row*3+column , self.destsend, "emoji")
        self.emoji.hide()

    def recv(self):
        '''
        用于将接收到的消息显示出来
        '''
        while True:
            while len(client.usermsg):
                msg_recv = client.usermsg.pop()
                msgtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(msg_recv["time"]))
                if msg_recv["mtype"] == "msg":
                    msg_recv["msg"] = msg_recv["msg"].replace("\n","\n  ")
                    if msg_recv["name"] == self.Username:       #从本地发送的消息打印
                        if msg_recv["destname"] == "all":
                            self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                            self.grprecvText.setTextColor(Qt.green)
                            self.grprecvText.insertPlainText(
                                " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                            self.grprecvText.setTextColor(Qt.black)
                            self.grprecvText.insertPlainText(msg_recv["msg"] + "\n")
                        else:
                            for i in self.prtbutton:
                                print(msg_recv["destname"])
                                print(self.destprtbutton[i])
                                if msg_recv["destname"] == self.destprtbutton[i]:
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.green)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    self.buttontotext[i].setTextColor(Qt.black)
                                    self.buttontotext[i].insertPlainText(msg_recv["msg"] + "\n")
                    elif msg_recv["destname"] in (self.Username, "all"):        #本地接收到的消息打印
                        if msg_recv["destname"] == "all":
                            self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                            self.grprecvText.setTextColor(Qt.blue)
                            self.grprecvText.insertPlainText(
                                " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                            self.grprecvText.setTextColor(Qt.black)
                            self.grprecvText.insertPlainText(msg_recv["msg"] + "\n")
                        else:
                            for i in self.prtbutton:
                                if self.destprtbutton[i] == msg_recv["name"]:
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.blue)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    self.buttontotext[i].setTextColor(Qt.black)
                                    self.buttontotext[i].insertPlainText(msg_recv["msg"] + "\n")
                                    break
                                elif self.destprtbutton[i] == None:
                                    self.destprtbutton[i] = msg_recv["name"]
                                    i.setText(msg_recv["name"])
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.blue)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    self.buttontotext[i].setTextColor(Qt.black)
                                    self.buttontotext[i].insertPlainText(msg_recv["msg"] + "\n")
                                    break
                elif msg_recv["mtype"] == "emoji":
                    if msg_recv["name"] == self.Username:  # 从本地发送的消息打印
                        if msg_recv["destname"] == "all":
                            self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                            self.grprecvText.setTextColor(Qt.green)
                            self.grprecvText.insertPlainText(
                                " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                            path = "./images/emoji/"+ str(msg_recv["msg"]) +".gif"
                            tcursor = self.grprecvText.textCursor()
                            img = QtGui.QTextImageFormat()
                            img.setName(path)
                            img.setHeight(28)
                            img.setWidth(28)
                            tcursor.insertImage(img)
                            self.grprecvText.insertPlainText("\n")
                        else:
                            for i in self.prtbutton:
                                print(msg_recv["destname"])
                                print(self.destprtbutton[i])
                                if msg_recv["destname"] == self.destprtbutton[i]:
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.green)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    path = "./images/emoji/" + str(msg_recv["msg"]) + ".gif"
                                    tcursor = self.buttontotext[i].textCursor()
                                    img = QtGui.QTextImageFormat()
                                    img.setName(path)
                                    img.setHeight(28)
                                    img.setWidth(28)
                                    tcursor.insertImage(img)
                                    self.buttontotext[i].insertPlainText("\n")
                    elif msg_recv["destname"] in (self.Username, "all"):  # 本地接收到的消息打印
                        if msg_recv["destname"] == "all":
                            self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                            self.grprecvText.setTextColor(Qt.blue)
                            self.grprecvText.insertPlainText(
                                " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                            path = "./images/emoji/"+ str(msg_recv["msg"]) +".gif"
                            tcursor = self.grprecvText.textCursor()
                            img = QtGui.QTextImageFormat()
                            img.setName(path)
                            img.setHeight(28)
                            img.setWidth(28)
                            tcursor.insertImage(img)
                            self.grprecvText.insertPlainText("\n")
                        else:
                            for i in self.prtbutton:
                                if self.destprtbutton[i] == msg_recv["name"]:
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.blue)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    path = "./images/emoji/" + str(msg_recv["msg"]) + ".gif"
                                    tcursor = self.buttontotext[i].textCursor()
                                    img = QtGui.QTextImageFormat()
                                    img.setName(path)
                                    img.setHeight(28)
                                    img.setWidth(28)
                                    tcursor.insertImage(img)
                                    self.buttontotext[i].insertPlainText("\n")
                                    break
                                elif self.destprtbutton[i] == None:
                                    self.destprtbutton[i] = msg_recv["name"]
                                    i.setText(msg_recv["name"])
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.blue)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    path = "./images/emoji/" + str(msg_recv["msg"]) + ".gif"
                                    tcursor = self.buttontotext[i].textCursor()
                                    img = QtGui.QTextImageFormat()
                                    img.setName(path)
                                    img.setHeight(28)
                                    img.setWidth(28)
                                    tcursor.insertImage(img)
                                    self.buttontotext[i].insertPlainText("\n")
                                    break
                else:
                    if msg_recv["name"] == self.Username:  # 从本地发送的消息打印
                        if msg_recv["destname"] == "all":
                            self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                            self.grprecvText.setTextColor(Qt.green)
                            self.grprecvText.insertPlainText(
                                " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                            path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                            with open(path,"wb") as f:
                                f.write(base64.b64decode(msg_recv["msg"]))
                                f.close()
                            tcursor = self.grprecvText.textCursor()
                            img = QtGui.QTextImageFormat()
                            if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                                img.setName(path)
                                img.setHeight(100)
                                img.setWidth(100)
                                tcursor.insertImage(img)
                            else:
                                img.setName("./images/style/MyChat/filebutton.png")
                                img.setHeight(30)
                                img.setWidth(30)
                                tcursor.insertImage(img)
                                self.grprecvText.insertPlainText("文件已保存在：" + path)
                            self.grprecvText.insertPlainText("\n")
                        else:
                            for i in self.prtbutton:
                                print(msg_recv["destname"])
                                print(self.destprtbutton[i])
                                if msg_recv["destname"] == self.destprtbutton[i]:
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.green)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                                    with open(path, "wb") as f:
                                        f.write(base64.b64decode(msg_recv["msg"]))
                                        f.close()
                                    tcursor = self.buttontotext[i].textCursor()
                                    img = QtGui.QTextImageFormat()
                                    if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                                        img.setName(path)
                                        img.setHeight(100)
                                        img.setWidth(100)
                                        tcursor.insertImage(img)
                                    else:
                                        img.setName("./images/style/MyChat/filebutton.png")
                                        img.setHeight(30)
                                        img.setWidth(30)
                                        tcursor.insertImage(img)
                                        self.buttontotext[i].insertPlainText("文件已保存在："+path)
                                    self.buttontotext[i].insertPlainText("\n")
                    elif msg_recv["destname"] in (self.Username, "all"):  # 本地接收到的消息打印
                        if msg_recv["destname"] == "all":
                            self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                            self.grprecvText.setTextColor(Qt.blue)
                            self.grprecvText.insertPlainText(
                                " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                            path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                            with open(path, "wb") as f:
                                f.write(base64.b64decode(msg_recv["msg"]))
                                f.close()
                            tcursor = self.grprecvText.textCursor()
                            img = QtGui.QTextImageFormat()
                            if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                                img.setName(path)
                                img.setHeight(100)
                                img.setWidth(100)
                                tcursor.insertImage(img)
                            else:
                                img.setName("./images/style/MyChat/filebutton.png")
                                img.setHeight(30)
                                img.setWidth(30)
                                tcursor.insertImage(img)
                                self.grprecvText.insertPlainText("文件已保存在：" + path)
                            self.grprecvText.insertPlainText("\n")
                        else:
                            for i in self.prtbutton:
                                if self.destprtbutton[i] == msg_recv["name"]:
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.blue)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                                    with open(path, "wb") as f:
                                        f.write(base64.b64decode(msg_recv["msg"]))
                                        f.close()
                                    tcursor = self.buttontotext[i].textCursor()
                                    img = QtGui.QTextImageFormat()
                                    if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                                        img.setName(path)
                                        img.setHeight(100)
                                        img.setWidth(100)
                                        tcursor.insertImage(img)
                                    else:
                                        img.setName("./images/style/MyChat/filebutton.png")
                                        img.setHeight(30)
                                        img.setWidth(30)
                                        tcursor.insertImage(img)
                                        self.buttontotext[i].insertPlainText("文件已保存在："+path)
                                    self.buttontotext[i].insertPlainText("\n")
                                    break
                                elif self.destprtbutton[i] == None:
                                    self.destprtbutton[i] = msg_recv["name"]
                                    i.setText(msg_recv["name"])
                                    self.buttontotext[i].moveCursor(QtGui.QTextCursor.End)
                                    self.buttontotext[i].setTextColor(Qt.blue)
                                    self.buttontotext[i].insertPlainText(
                                        " " + msg_recv["name"] + "  " + msgtime + "\n  ")
                                    path = "./" + self.Username + "/" + msg_recv["fname"] + msg_recv["mtype"]
                                    with open(path, "wb") as f:
                                        f.write(base64.b64decode(msg_recv["msg"]))
                                        f.close()
                                    tcursor = self.buttontotext[i].textCursor()
                                    img = QtGui.QTextImageFormat()
                                    if msg_recv["mtype"] in (".png", ".gif", ".jpg"):
                                        img.setName(path)
                                        img.setHeight(100)
                                        img.setWidth(100)
                                        tcursor.insertImage(img)
                                    else:
                                        img.setName("./images/style/MyChat/filebutton.png")
                                        img.setHeight(30)
                                        img.setWidth(30)
                                        tcursor.insertImage(img)
                                        self.buttontotext[i].insertPlainText("文件已保存在："+path)
                                    self.buttontotext[i].insertPlainText("\n")
                                    break

            while len(client.sysmsg):
                msg_recv = client.sysmsg.pop()
                # msgtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(msg_recv["time"]))
                if msg_recv["info"] == "userlogin":
                    if msg_recv["name"] not in client.userlist:
                        client.userlist.append(msg_recv["name"])
                        self.friendlist.clear()
                        self.friendlist.addItems(client.userlist)
                elif msg_recv["info"] == "userexit":
                    if msg_recv["name"] in client.userlist:
                        client.userlist.remove(msg_recv["name"])
                        self.friendlist.clear()
                        self.friendlist.addItems(client.userlist)
                self.grprecvText.moveCursor(QtGui.QTextCursor.End)
                self.grprecvText.setTextColor(Qt.gray)
                self.grprecvText.insertPlainText("      "+msg_recv["msg"]+"\n")

    def main(self):
        func1 = threading.Thread(target=self.recv)
        func1.start()

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)  #
    client = MyChat_Client(addr="localhost", port=14396)
    client.main()
    login = loginWindow()
    login.show()
    sys.exit(app.exec_())
