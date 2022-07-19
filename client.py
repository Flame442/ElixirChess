import pygame
import pickle
from network import Network
from game import Game, Color, Pawn, Queen, Move


class Client:
    def __init__(self):
        self.width = 900
        self.height = 1000
        self.win = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Elixir Chess")
        pygame.font.init()
        self.network = Network()
        self.player = Color(self.network.player)
        self.elixir = 0
        self.elixir_per_unit = 90
        self.holding = None
        
    def draw(self, game):
        # Background
        self.win.fill((128, 128, 128))
        # Tiles
        for x in range(8):
            for y in range(8):
                color = (120, 64, 45) if (x + y) % 2 else (193, 150, 94)
                pygame.draw.rect(self.win, color, ((x * 100) + 50, (y * 100) + 100, 100, 100))
        # Pieces
        for piece in game.pieces:
            piece.draw(self.win, self.player, self.holding is not None and piece.id == self.holding.id)
        # Elixir bar
        pygame.draw.rect(self.win, (60, 60, 60), (50, 925, 800, 50))
        pygame.draw.rect(self.win, (100, 100, 100), (55, 930, 790, 40))
        bar_px = int((self.elixir / (self.elixir_per_unit * 10)) * 790)
        pygame.draw.rect(self.win, (214, 56, 214), (55, 930, bar_px, 40))
        for px in range(79, 790, 79):
            color = (142, 67, 142) if px <= bar_px else (76, 76, 76)
            pygame.draw.rect(self.win, color, (55 + px, 930, 2, 10))
        font = pygame.font.SysFont("montserrat", 50)
        text = font.render(str((self.elixir // (self.elixir_per_unit))), 1, (142, 67, 142))
        self.win.blit(text, (25 - round(text.get_width() / 2), 950 - round(text.get_height() / 2)))
        # Winner
        if game.winner is not None:
            if game.winner == Color.WHITE:
                text = font.render("White wins!", 1, (255, 255, 255))
            else:
                text = font.render("Black wins!", 1, (0, 0, 0))
            self.win.blit(text, (450 - round(text.get_width() / 2), 50 - round(text.get_height() / 2)))
        # Update
        pygame.display.update()

    def run(self):
        while True:
            self.clock.tick(60)
            game = self.network.send(pickle.dumps("get"))
            if game.started and game.winner is None:
                self.elixir = min(self.elixir + 1, self.elixir_per_unit * 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if game.winner is not None:
                    self.holding = None
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for piece in game.pieces:
                        if piece.color != self.player:
                            continue
                        if not piece.click(self.player, x, y):
                            continue
                        self.holding = piece
                if event.type == pygame.MOUSEBUTTONUP and self.holding is not None:
                    for piece in game.pieces:
                        if piece.id == self.holding.id:
                            break
                    else:
                        piece = None
                    if piece:
                        x, y = pygame.mouse.get_pos()
                        x = (x + 50) // 100
                        y //= 100
                        if self.player == Color.WHITE:
                            x = 8 - x + 1
                            y = 8 - y + 1
                        if piece.move(x, y):
                            if self.elixir >= (piece.COST * self.elixir_per_unit):
                                self.elixir -= piece.COST * self.elixir_per_unit
                                game = self.network.send(pickle.dumps(Move(piece.id, x, y)))
                    self.holding = None
                    
            self.draw(game)

Client().run()
