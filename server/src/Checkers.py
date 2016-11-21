""" Checkers Logic"""

# Import Qt module
from copy import deepcopy

from PyQt5.QtCore import QCoreApplication
from server.src.Board import *
from server.src.Piece import *
from server.src.TypeMove import *

from server.src.Sender import *


class Checkers:
    """
        default constructor creates the board and populates
        the board with pieces
    """
    def __init__(self):
        self.board = Board(8)
        self.size = self.board.getSize()
        self.turn = 0
        self.best_move = None
        self.game_over = False
        self.jumpAgain = (False,None,None)

    """
         gets if any of the players pieces can jump and adds it to
         the array, and returns it
    """
    def forceJump(self,player):
        moves = []
        for i in range (self.size):
            for j in range (self.size):
                tmp = self.board.getPieceAt(i, j)
                # checks if tmp is not none and player == the piece
                if tmp and player == tmp.getOwner() :
                    jumpF = self.canJump(i, j)
                    # if jumpF array is not empty append i , j and each value in the array
                    # for that piece
                    if jumpF :
                        for n in jumpF:
                            moves.append(n)
        return moves

    # returns if the game is over
    def isOver(self):
        return self.game_over

    # checks to see if the game has ended and sets game_over to true
    def checkWin(self, typeMove):
        if self.board.countPlayerPieces ==0 or len(self.getMoves("Player")) == 0:
            self.game_over = True
            return "AI"
        elif self.board.countAiPieces ==0 or len(self.getMoves("AI")) == 0:
            self.game_over = True
            return "Player"

    """
        validates if piece at X,Y can move to x1 , y1
        checks if x1 and y1 is inside the board and x1 and y1 is a empty space
        returns true or false
    """
    def validMove(self,x1,y1):
        if self.board.getSize() > x1 >= 0 and 0 <= y1 < self.board.getSize():
            if not self.board.pieceAt(x1, y1):
                return True
        else:
            return False

    # moves a piece players piece from X Y to x1 y1
    def movePiece(self,player,x,y,x1,y1,typeMove):

        #self.sender = Sender#

        moved = False
        #gets an array of movable positions x y given by user
        moves = self.getMoves(player)
        # move is the string of x y, x1 y1 for comparing to the array of movable positions
        move = str(x)+","+str(y)+","+str(x1)+","+str(y1)
        if not self.isOver() :
            if self.forceJump(player):
                #Second jump
                if self.jumpAgain[0]:
                    # if jumpagain is true get the jumpable moves for jumpAgain[1], jumpAgain[2]
                    moves = self.canJump(self.jumpAgain[1], self.jumpAgain[2])

                    #compares moves to move if equal move the piece and remove the piece being jumped
                    for i in moves:
                        if i == move:
                            self.board.movePiece(x, y, x1, y1)
                            # checks if a jump is true then remove the piece being jumped

                            removePieceX = (x + (x1))/2
                            removePieceY = (y + (y1))/2

                            self.board.removePiece(removePieceX, removePieceY)

                            #checks if it is king
                            if self.isKing(x1,y1):
                                self.board.updatePieceType(1,x1,y1)

                            #checks if it can jump again sets jumpAgain to true if true else set to False
                            if self.canJump(x1, y1):
                                moved = False
                                self.jumpAgain=(True,x1,y1)
                                break
                            else:
                                self.jumpAgain=(False,None,None)
                                moved = True
                                break

                else:
                    # This is the first jump
                    for i in moves:
                        if i == move :
                            self.board.movePiece(x, y, x1, y1)
                            # checks if a jump is true then remove the piece being jumped
                            removePieceX = (x + (x1))/2
                            removePieceY = (y + (y1))/2

                            self.board.removePiece(removePieceX, removePieceY)
                            #after jumping check if it can be Kinged and can it jump again
                            if self.isKing(x1,y1):
                                self.board.updatePieceType(1,x1,y1)

                            if self.canJump(x1, y1):
                                moved = False
                                self.jumpAgain= (True,x1,y1)
                                break
                            else:
                                self.jumpAgain= (False,None,None)
                                moved = True
                                break
            else:
            # checks if the input equals any possible moves
                if moves:
                    for i in moves:
                        if(i == move):
                            self.board.movePiece(x, y, x1, y1)
                            self.jumpAgain=(False,None,None)
                            moved = True
                            break
                    # if it can be kinged and updates the piece to a king
                    if self.isKing(x1,y1):
                        self.board.updatePieceType(1,x1,y1)

            #check is the game is over
            self.checkWin(typeMove=TypeMove.real)

        return moved

    #ends the players turn
    def turnEnd(self):
        self.turn+=1

    # returns if its players turn or AI's turn
    def getTurn(self):
        if(self.turn % 2 == 0):
            return "Player"
        else:
            return "AI"
    """
        checks if a piece can be Kinged when AI piece hits bottom of board
         or Player piece hits the top of the board
    """
    def isKing(self,x,y):
        self.p = Piece()
        self.p = self.board.getPieceAt(x, y)
        if(self.board.pieceAt(x, y)):
            if self.p.getOwner() == "AI" and y == self.board.getSize()-1:
                return True
            elif self.p.getOwner() == "Player" and y == 0 :
                return True
            else:
                return False
        else:
            return False
    """
        returns the moves for the piece at x y if it can jump
    """
    def canJump(self,x,y):
        moves = []
        tmp = self.board.getPieceAt(x, y)
        if tmp:
            start = 0
            finish = 0
            if tmp.getType() == 0:
                if tmp.getOwner() == "Player":
                    start = -1
                    finish = 0

                if tmp.getOwner() == "AI":
                    start = 1
                    finish = 2
                # Ai  # +1,-1 #-1 -1  player # +1 +1#-1 +1
                for i in range(-1,2):
                    for j in range (start,finish):
                        if (x +i < self.board.getSize() and x+i >=0) and (y+j <self.board.getSize() and y+j >=0):
                            tmp1 = self.board.getPieceAt(x+i, y+j)
                            if tmp1:
                                if tmp.getOwner() != tmp1.getOwner() :
                                    if self.validMove(x+i+i, y+j+j):
                                        moves.append(str(x)+","+str(y) +","+str(x+i+i)+","+str(y+j+j))

            #if piece is king then will try get all directions
            if tmp.getType() == 1:
                for i in range(-1,2):
                    for j in range (-1,2):
                        if (x +i < self.board.getSize() and x+i >=0) and (y+j <self.board.getSize() and y+j >=0):
                            tmp1 = self.board.getPieceAt(x+i, y+j)
                            if tmp1:
                                if tmp.getOwner() != tmp1.getOwner() :
                                    if self.validMove(x+i+i, y+j+j):
                                        moves.append(str(x)+","+str(y) +","+str(x+i+i)+","+str(y+j+j))

        return moves
    """
        returns the moves for the piece at x y if it can move
    """
    def pieceMovable(self,x,y):
        moves = []
        tmp = self.board.getPieceAt(x,y)
        if tmp :
            # if tmp is a king then check up left, up right, down left , down right
            if tmp.getType() == 1:
                if self.validMove(x-1, y-1):
                    moves.append(str(x-1)+","+str(y-1))

                if self.validMove(x+1, y-1):
                    moves.append(str(x+1)+","+str(y-1))

                if self.validMove(x-1, y+1):
                    moves.append(str(x-1)+","+str(y+1))

                if self.validMove(x+1, y+1):
                    moves.append(str(x+1)+","+str(y+1))
            # Players pieces which will always be at the bottom
            elif tmp.getOwner() == "Player" and tmp.getType() == 0:

                # UP and left
                if self.validMove(x-1, y-1):
                    moves.append(str(x-1)+","+str(y-1))
                # Up and right
                if self.validMove(x+1, y-1):
                    moves.append(str(x+1)+","+str(y-1))

            # AI pieces which will always be at the Top
            elif tmp.getOwner() == "AI" and tmp.getType() == 0:

                #down and right
                if self.validMove(x+1, y+1):
                        moves.append(str(x+1)+","+str(y+1))
                #down and left
                if self.validMove(x-1, y+1):
                    moves.append(str(x-1)+","+str(y+1))

        return moves

    # gets all the moves available to the player
    def getMoves(self,player):

        movableP = []
        # if it can jump again just get the moves that piece can jump again.
        if self.jumpAgain[0]:
            movableP = self.canJump(self.jumpAgain[1], self.jumpAgain[2])
        #check if any pieces can jump and just return the list of jumpable pieces and nothing else.
        else:
            movableP = self.forceJump(player)

        # if there is no pieces that can jump for the player return the movable pieces
        if not movableP:

            for i in range (self.board.getSize()):
                for j in range (self.board.getSize()):
                    tmp = self.board.getPieceAt(i,j)
                    if tmp and tmp.getOwner() == player:
                            tmpMoves =self.pieceMovable(i, j)
                            if tmpMoves:
                                for p in range (len(tmpMoves)):
                                    movableP.append(str(i)+","+str(j)+","+str(tmpMoves[p]))
        return movableP

    # evaluates the player for minimax with alpha beta pruning
    """
        minimax with alpha beta pruning
    """
    def alpha_beta(self, board,player, ply, alpha, beta):
        sock = socket.socket()
        sock.bind(('', 8080))

        sock.listen(1)
        conn, addr = sock.accept()

        data = conn.recv(1024)

        print("Server received: " + data)

        conn.send(("MR GRACHEV IS A DEFINETELY HUY").encode())

        conn.close()


        QCoreApplication.processEvents()
        # amount of moves to look ahead currently 3 moves ahead
        return beta
