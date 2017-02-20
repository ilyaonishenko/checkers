import ast
from client.src.Board import Board
from client.src.Piece import Piece
from client.src.Checkers import Checkers


class Decoder:
    # {"deepcopy": {"game_over": false, "jump_again": [false, null, null], "turn": 2,
    #               "board": "{\"aiPieces\": 12, \"size\": 8, \"array\": \"[[null, {\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}], [{\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, null, null, null, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}, null], [null, {\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, null, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}], [{\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}, null], [null, {\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, null, null, null, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}], [{\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, null, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}, null], [null, {\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, null, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}], [{\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, {\\\"owner\\\": \\\"AI\\\", \\\"type\\\": 0}, null, null, null, {\\\"owner\\\": \\\"Player\\\", \\\"type\\\": 0}, null]]\","
    #                        " \"playerPieces\": 12}",
    #               "p": "{\"owner\": \"AI\", \"type\": 0}", "size": 8, "best_move": [1, 2, 0, 3]}, "ai": [1, 2, 0, 3]}

    @staticmethod
    def get_ai_move(d):
        return d['ai']

    @staticmethod
    def update_pieces(pieces):
        return [[Piece.Factory.create(x['type'], x['owner']) if x is not None else None for x in arr] for arr in
                pieces]

    @staticmethod
    def get_game(d):
        dump = d['deepcopy']
        board_list = ast.literal_eval(dump['board'])
        pieces = ast.literal_eval(board_list['array'].replace('null', 'None'))
        pieces = Decoder.update_pieces(pieces)
        # piece = Piece.create_from_dump(int(ast.literal_eval(dump['p'])['type']), ast.literal_eval(dump['p'])['owner'])
        board = Board.Factory.create(pieces, board_list['size'],
                                     board_list['aiPieces'], board_list['playerPieces'])
        return Checkers.Factory.create(board, int(dump['size']), int(dump['turn']),
                                       dump['best_move'], dump['game_over'], dump['jump_again'])
