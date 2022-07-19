import pickle
import socket
import sys
from _thread import start_new_thread
from game import Game, Color, Move, Pawn, Queen, Rook, King
from settings import SERVER_IP, SERVER_PORT

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((SERVER_IP, SERVER_PORT))
        self.socket.listen(2)
        print("Server started, waiting for a connection...")
        self.game = Game()
        self.players_connected = [False, False]
        self.run()
    
    def run(self):
        while True:
            conn, addr = self.socket.accept()
            print("Connected to:", addr)
            player = self.players_connected.index(False)
            self.players_connected[player] = True
            if all(self.players_connected):
                self.game.started = True
            start_new_thread(self.threaded_client, (conn, addr, player))

    def threaded_client(self, conn, addr, player):
        conn.send(str.encode(str(player)))
        reply = ""
        while True:
            try:
                data = pickle.loads(conn.recv(2048*8))
                if not data:
                    break
                if isinstance(data, Move):
                    for piece in self.game.pieces:
                        if piece.id == data.piece:
                            break
                    else:
                        piece = None
                    if piece and piece.move(data.x, data.y):
                        self.game.en_passantable_pawns[piece.color] = []
                        for p in self.game.pieces:
                            if p.x == data.x and p.y == data.y:
                                if isinstance(p, King):
                                    self.game.winner = Color(not p.color)
                                self.game.pieces.remove(p)
                                break
                        if isinstance(piece, King):
                            self.game.can_castle_short[player] = False
                            self.game.can_castle_long[player] = False
                            if piece.x - data.x == -2:
                                for p in self.game.pieces:
                                    if p.x == 8 and p.y == piece.y and p.color == piece.color:
                                        p.x = 5
                                        p.cooldown = 120
                                        break
                            elif piece.x - data.x == 2:
                                for p in self.game.pieces:
                                    if p.x == 1 and p.y == piece.y and p.color == piece.color:
                                        p.x = 3
                                        p.cooldown = 120
                                        break
                        if isinstance(piece, Rook):
                            if (piece.y == 1 and player == Color.WHITE) or (piece.y == 8 and player == Color.BLACK):
                                if piece.x == 1:
                                    self.game.can_castle_long[player] = False
                                elif piece.x == 8:
                                    self.game.can_castle_short[player] = False
                        if data.y in (1, 8) and isinstance(piece, Pawn):
                            new_piece = Queen(self.game, piece.color, data.x, data.y)
                            self.game.pieces.remove(piece)
                            self.game.pieces.append(new_piece)
                            piece = new_piece
                        else:
                            piece.x = data.x
                            piece.y = data.y
                        piece.cooldown = 120
                else:
                    for piece in self.game.pieces:
                        if piece.color == player:
                            piece.cooldown = max(piece.cooldown - 1, 0)
                conn.sendall(pickle.dumps(self.game))
            except Exception as e:
                print(e)
                break
        print("Lost connection to:", addr)
        self.players_connected[player] = False
        conn.close()

Server()
