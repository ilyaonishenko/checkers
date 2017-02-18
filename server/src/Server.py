import socket
import pika
import json
import ast

from server.src import Encoder
from server.src.Board import Board
from server.src.Checkers import Checkers
from server.src.Piece import Piece
from server.src.Transformer import Transformer

if False:
    sock = socket.socket()
    sock.bind(('', 8080))

    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)

        if not data:
            continue
        print("Server received: " + str(data))

        conn.send(("MR GRACHEV IS A DEFINETELY HUY").encode())

    print('closed')
    conn.close()

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def evaluate_move(game):
    return game.AI()

def update_pieces(pieces):
    for i in range(8):
        for j in range(8):
            if isinstance(pieces[i][j],dict):
                pieces[i][j] = Piece.create_from_dump(pieces[i][j]['type'],pieces[i][j]['owner'])
    return pieces

def parse_dump(bytes):
    dump = json.loads(bytes.decode("utf-8"))
    print(dump)
    board_list = ast.literal_eval(dump['board'])
    print(board_list)
    pieces = ast.literal_eval(board_list['array'].replace('null', 'None'))
    pieces = update_pieces(pieces)
    piece = Piece.create_from_dump(int(ast.literal_eval(dump['p'])['type']), ast.literal_eval(dump['p'])['owner'])
    board = Board.create_from_dump(pieces, board_list['size'],
                                   board_list['aiPieces'], board_list['playerPieces'])
    return Checkers.create_from_dump(board, int(dump['size']), int(dump['turn']),
                                         dump['best_move'], dump['game_over'], dump['jump_again'])
#     {'board': '{"aiPieces": 12, "playerPieces": 12,
# "array": "[[null, {\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, null, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}], [{\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, {\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, null, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}, null], [null, {\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, null, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}], [{\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, {\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}, null], [null, {\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, null, null, null, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}], [{\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, {\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, null, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}, null], [null, {\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, null, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}], [{\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, {\\"type\\": 0, \\"owner\\": \\"AI\\"}, null, null, null, {\\"type\\": 0, \\"owner\\": \\"Player\\"}, null]]", "size": 8}',
#  'p': '{"type": 0, "owner": "Player"}',
# 'game_over': False, 'turn': 1, 'best_move': None, 'jump_again': [False, None, None], 'size': 8}

# 'array': '[[null, {"type": 0, "owner": "AI"}, null, null, null, {"type": 0, "owner": "Player"}, null, {"type": 0, "owner": "Player"}], [{"type": 0, "owner": "AI"}, null, {"type": 0, "owner": "AI"}, null, null, null, {"type": 0, "owner": "Player"}, null], [null, {"type": 0, "owner": "AI"}, null, null, null, {"type": 0, "owner": "Player"}, null, {"type": 0, "owner": "Player"}], [{"type": 0, "owner": "AI"}, null, {"type": 0, "owner": "AI"}, null, {"type": 0, "owner": "Player"}, null, {"type": 0, "owner": "Player"}, null], [null, {"type": 0, "owner": "AI"}, null, null, null, null, null, {"type": 0, "owner": "Player"}], [{"type": 0, "owner": "AI"}, null, {"type": 0, "owner": "AI"}, null, null, null, {"type": 0, "owner": "Player"}, null], [null, {"type": 0, "owner": "AI"}, null, null, null, {"type": 0, "owner": "Player"}, null, {"type": 0, "owner": "Player"}], [{"type": 0, "owner": "AI"}, null, {"type": 0, "owner": "AI"}, null, null, null, {"type": 0, "owner": "Player"}, null]]'

def on_request(ch, method, props, body):
    status = parse_dump(body)
    game = evaluate_move(status)
    print("get game body")
    # response = "MR GRACHEV IS A DEFINETELY HUY"

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id),
                     body=json.dumps(game, cls=Encoder))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
