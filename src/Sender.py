
import datetime
import requests
import time
import socket


class Sender:

    global last
    global ai_num
    global player_num

    def send(self, message):
        last = datetime.datetime.now()
        td = (datetime.datetime.now()-last)
        if(td.seconds*1000000 + td.microseconds*200000):
            time.sleep(0.2)
        host = '10.0.0.2'
        port = 10002
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        s.send((message+"\r\n").encode())
        buffer = 256
        resp = s.recv(buffer)
        s.close()
        print(resp)

        last = datetime.datetime.now()

    def __init__(self):
        last = datetime.datetime.now()

    def reformat(self, x, y):
        return 1+(7-y)*8+x

    def move(self,placeFrom, placeTo):
        return Sender.send(self,"CHECK,6\r\nM,M,M,M,M,M\r\n" + str(1) + "," + str(placeFrom) + "," + str(1) + "," + str(placeTo) + "," + str(0) + "," + str(0))

    def remove_player(self, placeFrom):
        return  Sender.send(self, "CHECK,6\r\nM,M,M,M,M,M\r\n" + str(1) + "," + str(placeFrom) + "," + str(4) + "," + str(9) + "," + str(0) + "," + str(7))

    def remove_AI(self, placeFrom):
        return  Sender.send(self, "CHECK,6\r\nM,M,M,M,M,M\r\n" + str(1) + "," + str(placeFrom) + "," + str(4) + "," + str(7) + "," + str(0) + "," + str(7))

    def takeback_player(self, placeForm):
        return

    def takeback_AI(self, placeForm):
        return
