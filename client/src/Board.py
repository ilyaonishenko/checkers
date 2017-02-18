""" Board Class"""

#import the Piece Class
from client.src.Piece import *
from client.src.Encoder import *
import json


# asdjhaskdhaskdas

class Board:
    """ 
        default constructor given by a argument
        creates a empty 2D array with size given by the argument
    """
    def __init__(self,size):
        self.array = []
        self.size = int(size)
        self.aiPieces = 0
        self.playerPieces = 0
        for i in range (self.size):
            self.array.append([])
            for j in range (self.size):
                self.array[i].append(None)

    def __json__(self):
        return {'array': json.dumps(self.array, cls=Encoder), 'size': self.size, 'aiPieces': self.aiPieces, 'playerPieces': self.playerPieces}
                
    """ 
        Adds a piece to the array given by owner, type , at position x and y
        number of pieces + 1
    """
    def addPiece(self,owner,type,x,y):
        piece = Piece()
        piece.setup(owner,type)
        if self.array[int(x)][int(y)] == None:
            if piece.getOwner()== "AI" and (piece.getType() == 1 or piece.getType() == 0):
                self.array[int(x)][int(y)] = piece
                self.aiPieces+=1
                return True
            elif piece.getOwner()== "Player" and (piece.getType() == 1 or piece.getType() == 0):
                self.array[int(x)][int(y)] = piece   
                self.playerPieces+=1
                return True
        else:
            return False
        
    def printBoard(self):
        for i in range (self.size):
            print(self.array[i])
        print("\n")
        
    # Returns the number of ai pieces
    def countAiPieces(self):
        return self.aiPieces
    
    # Returns the number of player pieces
    def countPlayerPieces(self):
        return self.playerPieces
    
    """
        returns the piece from the array given at position x and y 
        and sets that array position to none
        number of pieces - 1 
    """    
    def removePiece(self,x,y): 
        if self.pieceAt(x,y) :
            tmp = self.getPieceAt(x,y)
            self.array[int(x)][int(y)] = None
            if tmp.getOwner() == "AI":
                self.aiPieces-=1
            elif tmp.getOwner() == "Player":
                self.playerPieces-=1
            return tmp
    """  
        updatePiece takes a type to be updated to
        at position x and y, removes that piece
        and re-adds it back at the same position with the new type
    """
    def updatePieceType(self,type,x,y):
        tmp = self.removePiece(x, y)
        if tmp:
            self.addPiece(tmp.getOwner(), type, x, y)
            return True
        else:
            return False
    
    # checks if there is a piece at X , Y 
    def pieceAt(self,x,y):
        
        tmp = self.array[int(x)][int(y)]
        if tmp != None:
            return True
        else:
            return False
        
    # returns the piece at array X,Y if the piece exits there.     
    def getPieceAt(self,x,y):
        if self.pieceAt(x, y):
            return self.array[int(x)][int(y)]
        
    # returns size
    def getSize(self):
        return self.size
    
    """ 
        move piece takes current piece position at X, Y and moves it to X1, Y1
        removes Piece at X and Y in the array and adds it back at position X1, Y1
    """
    def movePiece(self,x,y,x1,y1):
        tmp = self.removePiece(x, y)
        if tmp:
            self.addPiece(tmp.getOwner(), tmp.getType(), x1, y1)
            return True
        else:
            return False