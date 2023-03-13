import requests
import os

from time import sleep
from datetime import datetime


WAITING = 0
INPROGRESS = 1
WIN = 2
DRAW = 3

GAMESERVER_URL = "http://localhost:5000"
DATABASE_URL = "http://localhost:3000"

def print_board(board):
    print("     |     |     ")
    print(f"  {board[0][0]}  |  {board[0][1]}  |  {board[0][2]}  ")
    print("_____|_____|_____")
    print("     |     |     ")
    print(f"  {board[1][0]}  |  {board[1][1]}  |  {board[1][2]}  ")
    print("_____|_____|_____")
    print("     |     |     ")
    print(f"  {board[2][0]}  |  {board[2][1]}  |  {board[2][2]}  ")
    print("     |     |     ")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":

    menu = True

    while menu:
        print("Start: 1, Join: 2, Game history: 3, Exit: 4")

        try:
            start = int(input("Enter: "))
        except ValueError:
            print("Invalid input")
        else:
            if start == 1: # Create game
                resp = requests.get(GAMESERVER_URL + "/creategame").json()

                if "error" not in resp:
                    game_id = resp["game_id"]
                    token = resp["token"]
                    mysymbol = resp["player"]

                    print(f"Game ID: {game_id}")
                    print(f"Token: {token}")

                    menu = False
                else:
                    print(resp["error"])
            elif start == 2: # Join game
                game_id = input("Enter game ID: ")

                resp = requests.post(GAMESERVER_URL + f"/{game_id}/joingame").json()

                if "error" not in resp:
                    token = resp["token"]
                    mysymbol = resp["player"]

                    print(f"Token: {token}")

                    menu = False
                else:
                    print(resp["error"])
            elif start == 3: # Game history
                try:
                    resp = requests.get(DATABASE_URL + "/game_history/")
                    if resp.ok:
                        data = resp.json()
                        print(f"{'Game ID':^10}|{'Result':^10}|{'Duration (s)':^12}|{'Start time':^24}|{'End time':^24}")
                        for game in data:
                            start_time = datetime.strptime(game["start_time"], "%Y-%m-%d %H:%M:%S.%f")
                            end_time = datetime.strptime(game["end_time"], "%Y-%m-%d %H:%M:%S.%f")
                            duration =  (end_time - start_time).seconds
                            print(f"{game['id']:^10}|{game['result']:^10}|{duration:^12}|{start_time.strftime('%H:%M:%S %d-%m-%Y'):^24}|{end_time.strftime('%H:%M:%S %d-%m-%Y'):^24}")
                except ConnectionError:
                    print("Database not available.")

            elif start == 4: # Exit
                exit()
            else:
                print("Invalid input")

    while True:
        clear_screen()

        resp = requests.get(GAMESERVER_URL + f"/{game_id}/getgamestatus").json()

        if "error" not in resp:
            status = resp["status"]

            if status == WAITING:
                print("Game ID: " + str(game_id))
                print("Waiting for other player to join...")
            elif status == INPROGRESS:
                print_board(resp["board"])

                if resp["turn"] == mysymbol:
                    while True:
                        move = input("Your turn: ")

                        try:
                            x, y = move.split()
                            x = int(x)
                            y = int(y)
                        except ValueError:
                            print("Invalid input")
                        else:
                            print(f"{mysymbol} to ({x}, {y})")
                            break

                    # Send move to server
                    resp = requests.post(GAMESERVER_URL + f"/{game_id}/play", json={"token": token, "x": x, "y": y}).json()

                    if "error" in resp:
                        print(resp["error"])
                else:
                    print("Waiting for other player...")
            elif status == WIN:
                print_board(resp["board"])
                print(f"{str(resp['turn'])} wins!")

                resp = requests.post(GAMESERVER_URL + f"/{game_id}/endgame", json={"token": token}).json()
                break
            elif status == DRAW:
                print_board(resp["board"])
                print("Draw!")

                resp = requests.post(GAMESERVER_URL + f"/{game_id}/endgame", json={"token": token}).json()
                break
        else:
            print(resp["error"])

        # Refresh every second
        sleep(1)

    # Wait before exiting after game ends
    sleep(5)
