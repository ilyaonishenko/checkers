""" Piece Class"""

class Piece:
    # default constructor
    def __init__(self, *args, **kwargs):
        if len(kwargs) is 0:
            self.type = 0
            self.owner = ""
        else:
            self.type = kwargs['type']
            self.owner = kwargs['owner']

    @staticmethod
    def create_from_dump(type, owner):
        return Piece(type = type, owner = owner)

    def __json__(self):
        return {"type": self.type, "owner": self.owner}

    #setup assigns owner and type to itself
    def setup(self,owner,type):
        self.type = type
        self.owner = owner
    
    #returns type
    def getType(self):
        return self.type
    
    #returns owner
    def getOwner(self):
        return self.owner

    #prints owner and type    
    def printPieceInfo(self):
        print("Owner =" , self.owner)
        print("Type =" , self.type)