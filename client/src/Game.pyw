"""The user interface"""

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from client.src.Checkers import *
from client.src.Lock import *

from client.src.TypeMove import *
from client.src.Decoder import Decoder

"""
    image paths
"""
red = "../images/red.jpg"
redKing = "../images/redKing.jpg"
blackKing = "../images/blackKing.jpg"
highlightKingRed = "../images/highlightKingRed.jpg"
highlightKingBlack = "../images/highlightKingBlack.jpg"
empty = "../images/empty.jpg"
white = "../images/white.jpg"
black = "../images/black.jpg"
highlight = "../images/highlight.jpg"
highlightRed = "../images/highlightRed.jpg"
highlightBlack = "../images/highlightBlack.jpg"

"""
    ImgWidget class to draw images onto the GUI window
"""


class ImgWidget(QWidget):
    # default constructor takes image path and the parent of widget
    def __init__(self, imagePath, parent):
        super(ImgWidget, self).__init__(parent)
        self.picture = QPixmap(imagePath)

    # paints the image
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)


"""
    GUI Class main interface for the user.
"""


def main():
    app = QApplication(sys.argv)
    interface = GUI()
    sys.exit(app.exec_())


class GUI(QWidget):
    # default constructor calls initUI
    def __init__(self):
        super(GUI, self).__init__()
        self.initUI()

    # sets up the main window with buttons and tables
    def initUI(self):

        self.gameHistory = []
        # sets the window title
        self.setWindowTitle("DRAUGHTS")
        # draws a black piece
        blackImg = ImgWidget(black, self)
        blackImg.setGeometry(560, self.height() / 1.2, 60, 60)

        # draws a red piece
        redImg = ImgWidget(red, self)
        redImg.setGeometry(560, 50, 60, 60)

        self.score = []
        self.playing = False
        # sets the window to a fixed size
        self.setFixedSize(700, 690)

        """
            BUTTONS For New Game. Quit, Resign, Undo
        """
        quitButton = QPushButton("Quit", self)
        quitButton.resize(80, 50)
        quitButton.move(self.width() - 90, self.height() - 80)

        undoButton = QPushButton("Clean", self)
        undoButton.resize(80, 50)
        undoButton.move(self.width() - 90, self.height() - 160)

        newButton = QPushButton("New Game", self)
        newButton.resize(80, 50)
        newButton.move(self.width() - (180), self.height() - (160))

        resignButton = QPushButton("Resign", self)
        resignButton.move(self.width() - 180, self.height() - 80)
        resignButton.resize(80, 50)

        """
           Labels
        """
        # players turn
        self.turn = QLabel('', self)
        self.turn.setFont(QFont('TimesNewRomans', 18))
        self.turn.move(self.width() - 180, self.height() / 3)
        self.turn.setMinimumWidth(200)

        aiLabel = QLabel("Computer", self)
        aiLabel.setFont(QFont('TimesNewRomans', 17))
        aiLabel.move(self.width() - 160, 10)

        playerLabel = QLabel("Player", self)
        playerLabel.setFont(QFont('TimesNewRomans', 17))
        playerLabel.move(self.width() - 145, self.height() / 1.90)

        # Number of pieces computer has
        self.aiPiece = QLabel(" 0 ", self)
        self.aiPiece.setFont(QFont('TimesNewRomans', 28))
        self.aiPiece.move(self.width() - 75, 60)

        # Number of pieces player has
        self.playerPiece = QLabel(' 0 ', self)
        self.playerPiece.setFont(QFont('TimesNewRomans', 28))
        self.playerPiece.move(self.width() - 75, self.height() / 1.7)

        """
            Table aka the board representation
        """
        # creates a qtable 8 by 8
        self.table = QTableWidget(8, 8, self)

        # default vertical and horizontal header size is 60 images are 60pixels x 60 pixels
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.horizontalHeader().setDefaultSectionSize(60)

        # turning scroll bars off
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # move the table 10 right and 10 down
        self.table.move(10, 10)
        # fix table size of 500 x 510
        self.table.setFixedSize(500, 510)
        # fixed view for vertical and horizontal headers
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        """
             Showing all elements of the widget
        """
        blackImg.show()
        redImg.show()

        playerLabel.show()
        aiLabel.show()
        self.turn.show()

        # resignButton.show()
        # undoButton.show()
        newButton.show()
        quitButton.show()
        self.show()

        self.table.show()

        """
             initials Signals when buttons are pressed which function to call
        """
        newButton.clicked.connect(self.newGame)
        quitButton.clicked.connect(self.close)
        undoButton.clicked.connect(self.undo)
        resignButton.clicked.connect(self.resign)

        # sets the horizontal header labels to be A-H
        a = ord('A')
        index = 0
        for i in range(a, a * 8):
            item = QTableWidgetItem(str(chr(i)))
            self.table.setHorizontalHeaderItem(index, item)
            index += 1

        # displays a empty board in the table
        self.setEmptyBoard()

        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    # undo function is called when undo button is clicked
    def undo(self):
        """if self.gameHistory and self.playing:
            # deepcopy of the what's being pop'd
            pop = deepcopy(self.gameHistory.pop())
            self.game = pop
            # updates the game
            self.updateGame()
            # sets gameHistory to none as undo function only works for one undo
            self.gameHistory = []
        """
        uname = 'admin'
        pas = 'password'
        info = pika.PlainCredentials(uname, pas)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            '10.18.128.14', credentials=info, heartbeat_interval= 0))
        channel = connection.channel()

        channel.queue_declare(queue='turn_queue')
        channel.basic_publish(exchange='',
                              routing_key='turn_queue',
                              body="CLEAN")
        connection.close()

    # resign function  is called when resign button is clicked
    def resign(self):
        # if playing then have a pop up box asking does the player want to resign
        # can't resign if game is not playing.
        if self.playing:
            resignBox = QMessageBox.question(self, 'Resigning', 'Are you sure you want resign and forfeit?',
                                             QMessageBox.Yes, QMessageBox.No)
            if resignBox == QMessageBox.Yes:
                self.game.resign()
                self.updateGame()
                self.playing = False

    # new game function called when new game button is clicked
    def newGame(self):

        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        # if a game is in session a pop up box will appear asking does the player want to start a new game
        uname = 'admin'
        pas = 'password'
        info = pika.PlainCredentials(uname, pas)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            '10.18.128.14', credentials=info, heartbeat_interval=0))
        channel = connection.channel()

        channel.queue_declare(queue='turn_queue')
        channel.basic_publish(exchange='',
                              routing_key='turn_queue',
                              body="START_GAME")
        connection.close()
        if self.playing:

            resignBox = QMessageBox.question(self, 'New Game',
                                             'Are you sure you want start a new game while a game is one?',
                                             QMessageBox.Yes, QMessageBox.No)
            # if yes end game else do nothing
            if resignBox == QMessageBox.Yes:
                self.game.resign()
            else:
                return

        self.playing = True
        # create a new game
        self.game = Checkers()
        self.gameHistory = []
        # append the a deep copy of the new game to the game history
        tmpGame = deepcopy(self.game)
        self.gameHistory.append(tmpGame)

        self.updateGame()

        # self.connect(self.table, SIGNAL("cellClicked(int,int)"),self.clickBoard)
        self.table.cellClicked.connect(self.clickBoard)

    # if the table(board) is clicked
    def clickBoard(self, y, x):
        # takes a deep copy of the game before a move is performed

        if (Lock.isLocked(self)):
            return

        tmpGame = deepcopy(self.game)

        if not self.game.isOver():
            # if x1 is none then its the first click
            if self.x1 == None:
                self.click(x, y)
            else:
                # second click
                self.x2 = x
                self.y2 = y
                moved = False
                # checks if the turn is the players before taking a move
                if (self.game.getTurn() == "Player"):
                    moved = self.game.movePiece("Player", self.x1, self.y1, self.x2, self.y2, TypeMove.real)

                # updates the board
                self.updateGame()
                if moved and self.game.getTurn() == "Player" and not self.game.isOver():
                    print("PLAYER" + self.game.data_to_send)

                    # appends the deepcopy state of the board that was copied before a move
                    self.gameHistory.append(tmpGame)
                    # ends
                    self.game.turnEnd()
                    self.x1 = None
                    self.y1 = None
                    x = None
                    y = None
                    # updates piece positions
                    self.updateGame()

                    if self.game.getTurn() == "AI" and not self.game.isOver():
                        # call the AI to make a move and update the move it has taken.
                        # returns a string and highlights the move its taken
                        info_to_send = deepcopy(self.game)

                        try:
                            rabbit = RabbitClient()
                        except:
                            print("DRUGOY HUY")
                            try:
                                rabbit = RabbitClient()
                            except:
                                print("ESHE ODIN HUY AHAHA")
                                rabbit = RabbitClient()
                        response = rabbit.call(info_to_send)
                        ai_moved = Decoder.get_ai_move(response)
                        self.game = Decoder.get_game(response)
                        self.updateGame()
                        if len(ai_moved) > 0:
                            self.highlightPiece(ai_moved[0], ai_moved[1])
                            self.highlightPiece(ai_moved[2], ai_moved[3])
                            self.x1 = None
                            self.y1 = None
                            x = None
                            y = None
                else:
                    # if not moved try highlight. and set x and y to being the first click
                    self.click(x, y)

            self.x2 = None
            self.y2 = None

    # click function is called when a user clicks on the table(board)
    def click(self, x, y):
        # checks if there is a piece and assigns the x and y coordinates to x1 and y1
        if self.game.getPiece(x, y):
            self.x1 = x
            self.y1 = y
            # highlight the moves for the piece selected can take
            self.highlightMovable(self.x1, self.y1, self.game.getMoves("Player"))
        else:
            self.x1 = None
            self.y1 = None

    # highlights a piece
    def highlightPiece(self, x1, y1):
        tmpP = self.game.getPiece(x1, y1)
        if tmpP:
            # checks the pieces owner and sets the cell image based on the pieces owner and type
            if (tmpP.getOwner() == "AI"):
                if (tmpP.getType() == 1):
                    self.table.setCellWidget(y1, x1, ImgWidget(highlightKingRed, self))
                else:
                    self.table.setCellWidget(y1, x1, ImgWidget(highlightRed, self))
            else:
                if (tmpP.getType() == 1):
                    self.table.setCellWidget(y1, x1, ImgWidget(highlightKingBlack, self))
                else:
                    self.table.setCellWidget(y1, x1, ImgWidget(highlightBlack, self))
        # if tmpP isn't a piece then set it as empty
        else:
            self.table.setCellWidget(y1, x1, ImgWidget(highlight, self))

    def highlightMovable(self, x1, y1, moves):
        # highlights the piece being clicked
        self.highlightPiece(x1, y1)
        # parses i of all the moves, checks if x1 equals index 0 and y1 equals index 2
        for i in moves:
            # if they equal cast i[4] and i[6] to ints and highlight the empty squares the piece can move to
            if x1 == int(i[0]) and y1 == int(i[2]):
                tmpx = int(i[4])
                tmpy = int(i[6])
                self.highlightPiece(tmpx, tmpy)

    # sets the empty table with black and white squares as the board
    def setEmptyBoard(self):
        for y in range(8):
            for x in range(8):
                if (y % 2 == 0 and x % 2 == 1):
                    self.table.setCellWidget(y, x, ImgWidget(empty, self))
                if (y % 2 == 1 and x % 2 == 0):
                    self.table.setCellWidget(y, x, ImgWidget(empty, self))
                if (y % 2 == 0 and x % 2 == 0):
                    self.table.setCellWidget(y, x, ImgWidget(white, self))
                if (y % 2 == 1 and x % 2 == 1):
                    self.table.setCellWidget(y, x, ImgWidget(white, self))

    def updateGame(self):
        # adds the images for a empty board
        self.setEmptyBoard()
        for y in range(8):
            for x in range(8):
                # populate the board if position x and y has a piece
                pi = self.game.getPiece(x, y)
                if pi:
                    if pi.getOwner() == "AI":
                        if pi.getType() == 1:
                            self.table.setCellWidget(y, x, ImgWidget(redKing, self))
                        else:
                            self.table.setCellWidget(y, x, ImgWidget(red, self))

                    elif pi.getOwner() == "Player":
                        if pi.getType() == 1:
                            self.table.setCellWidget(y, x, ImgWidget(blackKing, self))
                        else:
                            self.table.setCellWidget(y, x, ImgWidget(black, self))

        # gets the amount of ai pieces and displays it
        self.aiPiece.setText(str(self.game.getAI()))
        # gets the amount of player pieces and displays it
        self.playerPiece.setText(str(self.game.getPlayer()))

        self.aiPiece.show()
        self.playerPiece.show()
        # Gets the players turn and indicates it.
        if (self.game.getTurn() == "AI"):
            self.turn.setText("A.I is Thinking")
        else:
            self.turn.setText("Its Your Turn")
        # if over set the players turn to game over.
        if self.game.isOver():
            self.turn.setText("GameOver")
            self.game.cleanField()
            self.playing = False

        self.turn.show()

    # Close event when you try to close the window a popup box will ask do you want to close the program
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to close the program?', QMessageBox.No,
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.playing = False
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    main()
