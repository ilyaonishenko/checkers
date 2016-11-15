class Lock():
    wait = False
    def startTurn(self):
        Lock.wait = True
    def endTurn(self):
        Lock.wait = False
    def isLocked(self):
        return Lock.wait