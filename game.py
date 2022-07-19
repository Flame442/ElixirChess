import pygame
import itertools
from enum import IntEnum
from math import copysign


class Color(IntEnum):
    WHITE = 0
    BLACK = 1


class Game:
    def __init__(self):
        self.pieces = [
            Rook  (self, Color.WHITE, 1, 1),
            Knight(self, Color.WHITE, 2, 1),
            Bishop(self, Color.WHITE, 3, 1),
            King  (self, Color.WHITE, 4, 1),
            Queen (self, Color.WHITE, 5, 1),
            Bishop(self, Color.WHITE, 6, 1),
            Knight(self, Color.WHITE, 7, 1),
            Rook  (self, Color.WHITE, 8, 1),
            
            Pawn  (self, Color.WHITE, 1, 2),
            Pawn  (self, Color.WHITE, 2, 2),
            Pawn  (self, Color.WHITE, 3, 2),
            Pawn  (self, Color.WHITE, 4, 2),
            Pawn  (self, Color.WHITE, 5, 2),
            Pawn  (self, Color.WHITE, 6, 2),
            Pawn  (self, Color.WHITE, 7, 2),
            Pawn  (self, Color.WHITE, 8, 2),
            
            Pawn  (self, Color.BLACK, 1, 7),
            Pawn  (self, Color.BLACK, 2, 7),
            Pawn  (self, Color.BLACK, 3, 7),
            Pawn  (self, Color.BLACK, 4, 7),
            Pawn  (self, Color.BLACK, 5, 7),
            Pawn  (self, Color.BLACK, 6, 7),
            Pawn  (self, Color.BLACK, 7, 7),
            Pawn  (self, Color.BLACK, 8, 7),
            
            Rook  (self, Color.BLACK, 1, 8),
            Knight(self, Color.BLACK, 2, 8),
            Bishop(self, Color.BLACK, 3, 8),
            King  (self, Color.BLACK, 4, 8),
            Queen (self, Color.BLACK, 5, 8),
            Bishop(self, Color.BLACK, 6, 8),
            Knight(self, Color.BLACK, 7, 8),
            Rook  (self, Color.BLACK, 8, 8),
        ]
        self.can_castle_short = [True, True]
        self.can_castle_long = [True, True]
        self.en_passantable_pawns = [[], []] # List of pawns that have moved two squares SINCE THIS COLOR MOVED LAST
        self.started = False
        self.winner = None


class Piece:
    IMAGE = [None, None]
    COST = 0
    NEXT_ID = itertools.count()
    
    def __init__(self, game: Game, color: Color, x: int, y: int):
        self.game = game
        self.color = color
        self.x = x
        self.y = y
        self.id = next(Piece.NEXT_ID)
        self.cooldown = 0
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, val):
        if val < 1:
            return
        if val > 8:
            return
        self._x = val
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, val):
        if val < 1:
            return
        if val > 8:
            return
        self._y = val
    
    def x_cord(self, player):
        x = self.x
        if player == Color.WHITE:
            x = 8 - x + 1
        return x * 100 - 50
    
    def y_cord(self, player):
        y = self.y
        if player == Color.WHITE:
            y = 8 - y + 1
        return (y * 100)
        
    def pieces_between(self, x: int, y: int):
        delta_x = x - self.x
        delta_y = y - self.y
        sign_x = int(copysign(1, delta_x))
        sign_y = int(copysign(1, delta_y))
        delta_x = abs(delta_x)
        delta_y = abs(delta_y)
        # across y
        if delta_x == 0:
            for i in range(1, delta_y):
                for piece in self.game.pieces:
                    if piece.x == self.x and piece.y == self.y + (i * sign_y):
                        return False
            return True
        # across x
        elif delta_y == 0:
            for i in range(1, delta_x):
                for piece in self.game.pieces:
                    if piece.x == self.x + (i * sign_x) and piece.y == self.y:
                        return False
            return True
        # across diagonal
        elif delta_x == delta_y:
            for i in range(1, delta_x):
                for piece in self.game.pieces:
                    if piece.x == self.x + (i * sign_x) and piece.y == self.y + (i * sign_y):
                        return False
            return True
        else:
            raise ValueError("not a straight line or a diagonal")
    
    def move(self, x: int, y: int):
        if self.cooldown:
            return False
        if x < 1 or x > 8:
            return False
        if y < 1 or y > 8:
            return False
        for piece in self.game.pieces:
            if piece.x == x and piece.y == y and piece.color == self.color:
                return False
        return True
    
    def draw(self, win, player, is_held: bool):
        img = pygame.image.load(self.IMAGE[self.color]).convert_alpha()
        if self.cooldown:
            img.set_alpha(128)
        if is_held:
            x_cord, y_cord = pygame.mouse.get_pos()
            win.blit(img, (x_cord - round(img.get_width() / 2), y_cord - round(img.get_height() / 2)))
        else:
            win.blit(img, (self.x_cord(player) + 50 - round(img.get_width() / 2), self.y_cord(player) + 50 - round(img.get_height() / 2)))
        
    def click(self, player: int, x: int, y: int):
        if not (self.x_cord(player) < x < self.x_cord(player) + 100):
            return False
        if not (self.y_cord(player) < y < self.y_cord(player) + 100):
            return False
        return True


class King(Piece):
    IMAGE = [
        "assets/white_king.png",
        "assets/black_king.png",
    ]
    COST = 2
    
    def move(self, x: int, y: int):
        if not super().move(x, y):
            return False
        if abs(self.x - x) <= 1 and abs(self.y - y) <= 1:
            return True
        if (self.color == Color.WHITE and y == 1) or (self.color == Color.BLACK and y == 8):
            if self.game.can_castle_short[self.color] and x == 2:
                for piece in self.game.pieces:
                    if piece.x in (2, 3) and piece.y == y:
                        return False
                return True
            if self.game.can_castle_long[self.color] and x == 6:
                for piece in self.game.pieces:
                    if piece.x in (5, 6, 7) and piece.y == y:
                        return False
                return True
        return False

class Queen(Piece):
    IMAGE = [
        "assets/white_queen.png",
        "assets/black_queen.png",
    ]
    COST = 9
    
    def move(self, x: int, y: int):
        if not super().move(x, y):
            return False
        if not (abs(self.x - x) == 0 or abs(self.y - y) == 0 or abs(self.x - x) == abs(self.y - y)):
            return False
        if not self.pieces_between(x, y):
            return False
        return True

class Rook(Piece):
    IMAGE = [
        "assets/white_rook.png",
        "assets/black_rook.png",
    ]
    COST = 5
    
    def move(self, x: int, y: int):
        if not super().move(x, y):
            return False
        if abs(self.x - x) and abs(self.y - y):
            return False
        if not self.pieces_between(x, y):
            return False
        return True

class Bishop(Piece):
    IMAGE = [
        "assets/white_bishop.png",
        "assets/black_bishop.png",
    ]
    COST = 3
    
    def move(self, x: int, y: int):
        if not super().move(x, y):
            return False
        if not abs(self.x - x) == abs(self.y - y):
            return False
        if not self.pieces_between(x, y):
            return False
        return True

class Knight(Piece):
    IMAGE = [
        "assets/white_knight.png",
        "assets/black_knight.png",
    ]
    COST = 3
    
    def move(self, x: int, y: int):
        if not super().move(x, y):
            return False
        delta_x = abs(self.x - x)
        delta_y = abs(self.y - y)
        if delta_x == 1 and delta_y == 2:
            return True
        if delta_x == 2 and delta_y == 1:
            return True    
        return False

class Pawn(Piece):
    IMAGE = [
        "assets/white_pawn.png",
        "assets/black_pawn.png",
    ]
    COST = 1
    
    def move(self, x: int, y: int):
        if not super().move(x, y):
            return False
        delta_x = x - self.x
        delta_y = y - self.y
        if self.color == Color.BLACK:
            delta_y = -delta_y
        # Move forward
        if not delta_x:
            # Pawns cannot capture the way they traditionally move, unlike other pieces
            for piece in self.game.pieces:
                if piece.x == x and piece.y == y:
                    return False
            if ((self.color == Color.WHITE and self.y == 2) or (self.color == Color.BLACK and self.y == 7)) and delta_y == 2:
                if not self.pieces_between(x, y):
                    return False
                self.game.en_passantable_pawns[not self.color].append(self)
                return True
            if delta_y == 1:
                return True
            return False
        # Capture diagonal
        if abs(delta_x) == 1 and delta_y == 1:
            for piece in self.game.pieces:
                if piece.x == x and piece.y == y and piece.color != self.color:
                    return True
            for piece in self.game.en_passantable_pawns[self.color]:
                if piece.x == x and piece.y + (1 if self.color == Color.WHITE else -1) == y and piece.color != self.color:
                    self.game.pieces.remove(piece)
                    return True
        return False

class Move:
    def __init__(self, piece, x, y):
        self.piece = piece
        self.x = x
        self.y = y
