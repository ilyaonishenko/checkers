
import datetime
import requests
import time
import socket


class Sender:

    global last
    global ai_num
    global player_num


    '''
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
    '''

    def __init__(self):

        last = datetime.datetime.now()


    @staticmethod
    def reformat(x, y):
        return 1+(7-y)*8+x

    @staticmethod
    def move(placeFrom, placeTo):
        return "CHECK,6\r\nM,M,M,M,M,M\r\n" + str(1) + "," + str(placeFrom) + "," + str(1) + "," + str(placeTo) + "," + str(0) + "," + str(0)

    @staticmethod
    def remove(placeFrom):
        return "CHECK,6\r\nM,M,M,M,M,M\r\n" + str(1) + "," + str(placeFrom) + "," + str(4) + "," + str(1) + "," + str(0) + "," + str(3)
    '''
    def remove_player(self, placeFrom):
        if self.A[self.player_i] > self.height:
            self.player_i += 2

        self.A[self.player_i] += 1
        return  Sender.send(self, "CHECK,6\r\nM,M,M,M,M,M\r\n" + str(1) + "," + str(placeFrom) + "," + str(4) + "," + str(self.player_i) + "," + str(0) + "," + str(self.A[self.player_i]))


    def takeback_player(self, placeForm):
        return

    def takeback_AI(self, placeForm):
        return

    def static_init(self):
        self.height = 3
        self.A = [0, 0, 0, 0, 0, 0]
        self.player_i = 0
        self.AI_i = 1

    '''





