# ElixirChess
Realtime chess with a Clash Royale style elixir bar.

This is a barebones proof of concept for a variant of Chess which allows for realtime piece movement. Movement is restricted in two ways: A piece is put on "cooldown" after it is moved, and cannot be moved again for 2 seconds. Additionally, an elixir/mana bar slowly fills up over time, and a piece can only be moved if you have enough elixir to cover its "move cost". The move cost of each piece is as follows:  
Queen - 9  
Rook - 5  
Bishop - 3  
Knight - 3  
King/Castling - 2  
Pawn - 1  
This game does not include a "check/checkmate" mechanic due to the realtime nature of the game. Instead, the game is won when a piece is able to capture the enemy king.

As this is a proof of concept, special care has not been put into ensuring the game is unable to be tampered with client-side. The server does not do extensive checks or record keeping to ensure the "rules" are being followed, and instead assumes both clients are acting in good faith. It only serves to allow the game to be played realtime by two players.

This project is loosely based on the teachings of [Tech With Tim's Python Online Game Tutorial](https://www.youtube.com/playlist?list=PLzMcBGfZo4-kR7Rh-7JCVDN8lm3Utumvq).

# Setup
> These steps should be performed on any machines that will be used to host or play the game.
1. Install [Python](https://www.python.org/) version 3.7 or higher.
2. Install [Pygame](https://www.pygame.org/) into your python install using `pip install pygame`.
3. Download the source code contained in this repository.
4. Modify `settings.py` to have the proper IP for your machine, and a port which does not conflict with any other port on the server's network.
- If you are going to use this computer as a server, hosting a game for 2 clients to play, set `SERVER_IP` and `SERVER_PORT`. If you intend to host the game for only machines on the same network as your server computer, `SERVER_IP` should be the local IP of the server's computer on your network. If you intend to allow computers outside of your network to connect to your server to play the game, `SERVER_IP` should be the public IP of the server's computer's network, and you must port forward the `SERVER_PORT` to your server computer.
- If you are going to use this computer as a client, connecting to a server to play the game, set `CLIENT_IP` and `CLIENT_PORT`. If you are connecting to a machine on the same network as your client computer, `CLIENT_IP` should be the local IP of the server's computer on your network. If you intend to connect to a machine on a different network than your client computer, `CLIENT_IP` should be the public IP of that server's computer's network. You should use the same `CLIENT_PORT` that the server used as their `SERVER_PORT`.
5. Run one `server.py` and connect to it by running two `client.py`s.
