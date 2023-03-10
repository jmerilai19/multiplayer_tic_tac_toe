import game
from flask import Flask, redirect, request, url_for

app = Flask(__name__)

games = {}

@app.route("/creategame", methods=["GET"])
def create_game():
    # Create game
    game_id = len(games)
    g = game.Game(game_id)
    games[str(game_id)] = g

    # Add first player to the game
    token, player = g.add_player()

    if g.start() == 0:
        return {"game_id": game_id, "token": token, "player": player}
    else:
        return {"error": "Error creating the game"}


@app.route("/<id>/joingame", methods=["POST"])
def join_game(id):
    # Check if game exists
    if id not in games:
        return {"error": "Game does not exist"}

    # Check if game is full
    if games[id].is_full():
        return {"error": "Game is full"}

    # Add player to game
    token, player = games[id].add_player()
    return {"token": token, "player": player}


@app.route("/<id>/getgamestatus", methods=["GET"])
def get_game_status(id):
    # Check if game exists
    if id not in games:
        return {"error": "Game does not exist"}

    # Return game info
    return {"status": games[id].status, "board": games[id].board, "turn": games[id].symbols[str(games[id].turn)]}


@app.route("/<id>/play", methods=["POST"])
def play(id):
    data = request.get_json()
    token = data["token"]
    x = data["x"]
    y = data["y"]

    # Check if game exists
    if id not in games:
        return {"error": "Game does not exist"}

    # Check if it's the player's turn
    if games[id].check_turn(token) == 0:
        return {"error": "It's not your turn"}

    # Check if enough players
    if games[id].number_of_players() < 2:
        return {"error": "Not enough players"}

    # Play move
    result = games[id].play(x, y)

    if result == 0 or result == 2 or result == 3:
        # Return game info
        return redirect(url_for("get_game_status", id=id))

    else:
        return {"error": "Invalid move"}

@app.route("/<id>/endgame", methods=["POST"])
def end_game(id):
    data = request.get_json()
    token = data["token"]

    # Check if game exists
    if id in games:
        # Remove player from game
        if games[id].get_player(token) != None:
            games[id].remove_player(token)

        # Delete game if no players left
        if games[id].number_of_players() == 0:
            games.pop(id)
            return {"message": "Game deleted"}

        else:
            return {"message": "Player removed from game"}
    return {"error": "Game does not exist"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
