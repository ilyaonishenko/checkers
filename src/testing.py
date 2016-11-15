from Checkers import *
from Piece import *
from Board import *
import unittest
def checkersTest():
	game = Checkers()
	print(game.evaluate("Player"))
	print(game.evaluate("AI"))
	print(game.getTurn())
	game.turnEnd()
	print(game.getTurn())
	game.printGame()
	
	board = Board(8)
	board.addPiece("Player",0,1,1)
	game.loadBoard(board)
	game.printGame()
	print(game.checkWin(), game.isOver())
	board = Board(8)
	board.addPiece("AI",0,1,1)
	game.loadBoard(board)
	game.printGame()
	print(game.checkWin(), game.isOver())
	"""
	board = Board(8)
	board.addPiece("Player",0,1,0)
	board.addPiece("Player",0,4,4)
	board.addPiece("AI",0,5,3)
	board.addPiece("Player",0,2,2)
	board.addPiece("AI",0,0,7)
	board.addPiece("AI",0,3,3)
	board.addPiece("AI",0,1,6)
	game.loadBoard(board)
	print("validMove  from 2,2 to 1,1",game.validMove(1,1))
	print("Movable","2,2",game.pieceMovable(2, 2) )
	print("Movable","0,7",game.pieceMovable(1, 6) )
	
	
	print("King", game.isKing(3,3))
	print("King", game.isKing(1,6))
	print("King", game.isKing(1,0))
	print("King", game.isKing(0,7))
	print("CAN 4,4 Jump?", game.canJump(4, 4))
	print("ForceJump Player", game.forceJump("Player"))
	print("CAN 5,3 Jump?", game.canJump(5, 3))
	print("ForceJump AI", game.forceJump("AI"))
	
	
	board = Board(8)
	
	board.addPiece("Player",0,1,0)
	board.addPiece("Player",0,5,4)
	board.addPiece("AI",0,0,7)
	board.addPiece("AI",0,4,3)
	board.addPiece("AI",0,7,0)
	board.addPiece("Player",0,1,6)
	board.addPiece("Player",0,6,7)
	board.updatePiece(1, 0, 7)
	board.updatePiece(1, 1, 0)

	game.loadBoard(board)

	print(game.movePiece("Player",1, 0, 0, 1))
	print(game.movePiece("AI",7, 0, 6, 1))
	print(game.movePiece("AI",0, 7, 2, 5))
	print(game.movePiece("Player",5, 4, 3, 2))
	
	board2 = Board(8)
	
	board2.addPiece("Player",0,1,0)
	board2.addPiece("Player",0,5,4)
	board2.addPiece("AI",0,0,7)
	board2.addPiece("AI",0,4,3)
	board2.addPiece("AI",0,7,0)
	board2.addPiece("Player",0,1,6)
	board2.addPiece("Player",0,6,7)
	board2.updatePiece(1, 0, 7)
	board2.updatePiece(1, 1, 0)

	game2 = Checkers()
	game2.printGame()
	game2.loadBoard(board2)
	game2.printGame()
	print(game.movePiece("AI",0, 7, 2, 5))
	print(game.movePiece("Player",5, 4, 3, 2))
	print(game.movePiece("AI",7, 0, 6, 1))
	print(game.movePiece("Player",1, 0, 0, 1))
	"""
	"""while not game.isOver():
		print(game.getTurn())
		game.turnEnd()
		game.AI()
		game.printGame()"""

class BoardTest(unittest.TestCase):
	def setUp(self):
		self.board = Board(8)
		self.board2 = Board(3)
		self.board3 = Board(4)
		
	def testBoardSize(self):
		self.assertEqual(8,self.board.getSize())
		self.assertEqual(3,self.board2.getSize())
		self.assertEqual(4,self.board3.getSize())
		
	def test_Remove_From_Board(self):
		self.board.removePiece(2,1)
		self.assertEqual(0,self.board.countAiPieces())
		self.board.removePiece(6,6)
		self.assertEqual(0,self.board.countPlayerPieces())
		
	def test_Add_To_Board(self):
		# board 1
		self.board.addPiece("AI",0,1,1)
		self.board.addPiece("Player",0,6,6)
		self.assertEqual(1,self.board.countPlayerPieces())
		self.assertEqual(1,self.board.countAiPieces())
		self.assertTrue(self.board.pieceAt(1, 1))
		self.assertTrue(self.board.pieceAt(6, 6))
		
		# board 2		
		self.board2.addPiece("test",0,1,1)
		self.board2.addPiece("AI",3,1,2)
		self.assertEqual(0,self.board2.countPlayerPieces())
		self.assertEqual(0,self.board2.countAiPieces())
		self.assertFalse(self.board2.pieceAt(1, 1))
		self.assertFalse(self.board2.pieceAt(1, 2))
		
		self.board2.addPiece("AI",1,2,1)
		self.assertEqual(0,self.board2.countPlayerPieces())
		self.assertEqual(1,self.board2.countAiPieces())
		self.assertTrue(self.board2.pieceAt(2, 1))
		
		# board 3
		self.board3.addPiece("AI",0,1,1)
		self.assertEqual(0,self.board3.countPlayerPieces())
		self.assertEqual(1,self.board3.countAiPieces())
		self.assertTrue(self.board3.pieceAt(1, 1))
	
	def test_Get_Piece_Info(self):
		# board 1
		self.piece = self.board.getPieceAt(6, 6)
		self.assertEqual("Player", self.piece.getOwner())
		self.assertEqual(1, self.piece.getType())
		
		# board 2
		self.piece = self.board2.getPieceAt(2, 1)
		self.assertEqual("AI", self.piece.getOwner())
		self.assertEqual(1, self.piece.getType())
		
		self.piece = self.board2.getPieceAt(1, 2)
		self.assertIsNone(self.piece)
		
		self.piece = self.board2.getPieceAt(1, 1)
		self.assertIsNone(self.piece)

		# board 3
		self.piece = self.board3.getPieceAt(1, 1)
		self.assertEqual("AI", self.piece.getOwner())
		self.assertEqual(0, self.piece.getType())
		
	def test_Move_Piece(self):
		self.assertTrue(self.board.pieceAt(1, 1))
		self.board.movePiece(1, 1, 2, 1)
		self.assertFalse(self.board.pieceAt(1, 1))
		self.assertTrue(self.board.pieceAt(2, 1))

		self.assertTrue(self.board2.pieceAt(2, 1))
		self.board2.movePiece(2, 1, 2, 2)
		self.assertFalse(self.board2.pieceAt(2, 1))
		self.assertTrue(self.board2.pieceAt(2, 2))

		self.assertTrue(self.board3.pieceAt(1, 1))
		self.board3.movePiece(1, 1, 2, 1)
		self.assertFalse(self.board3.pieceAt(1, 1))
		self.assertTrue(self.board3.pieceAt(2, 1))
	
	def test_Update_Piece(self):
		self.board.updatePieceType(1,6,6)
		self.piece = self.board.getPieceAt(6, 6)
		self.assertEqual("Player", self.piece.getOwner())
		self.assertEqual(1, self.piece.getType())
		
	def tearDown(self):
		self.board = None
		self.board2 = None
		self.board3 = None
	
	def main(self):
		self.setUp()
		self.testBoardSize()
		self.test_Add_To_Board()
		self.test_Update_Piece()
		self.test_Get_Piece_Info()
		self.test_Move_Piece()
		self.test_Remove_From_Board()
		self.tearDown()

	# move piece and resign to do left.
class PieceTest(unittest.TestCase):

	def setUp(self):
		self.piece = Piece()
	# test piece setup 
	def pieceTest(self):
		self.piece.setup("Player", 0)
		self.assertEqual("Player", self.piece.getOwner())
		self.assertEqual(0, self.piece.getType())
		
		self.piece.setup("AI", 0)
		self.assertEqual("AI", self.piece.getOwner())
		self.assertEqual(0, self.piece.getType())
		
		self.piece.setup("Player",1)
		self.assertEqual("Player", self.piece.getOwner())
		self.assertEqual(1, self.piece.getType())
		
		self.piece.setup("AI",1)
		self.assertEqual("AI", self.piece.getOwner())
		self.assertEqual(1, self.piece.getType())
		
		self.piece.setup(293,"hello")
		self.assertEqual(293, self.piece.getOwner())
		self.assertEqual("hello", self.piece.getType())
		
		self.piece.setup(1,3)
		self.assertEqual(1, self.piece.getOwner())
		self.assertEqual(3, self.piece.getType())

	def tearDown(self):
		self.piece = None
		
	def main(self):
		self.setUp()
		self.pieceTest()
		self.tearDown()
		
		
test = BoardTest()
test.main()
#pieceTest()
#boardTest()
#checkersTest()