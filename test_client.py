import game

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

if __name__ == "__main__":
    g = game.Game(0)

    if g.start() == 0:
        print_board(g.board)
    else:
        print("Error")
        exit()

    while True:
        move = input(f"{g.symbols[str(g.turn)]}'s turn: ")

        try :
            x, y = move.split()
            x = int(x)
            y = int(y)
        except ValueError:
            print("Invalid input")
            continue
        else:
            status = g.play(x, y)

            if status == 0:
                print_board(g.board)
            elif status == 2:
                print_board(g.board)
                print(f"{g.symbols[str(g.turn)]} wins!")
                break
            elif status == 3:
                print_board(g.board)
                print("Draw!")
                break
            else:
                print(f"Invalid move")
