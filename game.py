class Game():
    def __init__(self, _id):
        self.symbols = {
            "empty": " ",
            "0": "O",
            "1": "X"
        }

        self.id = _id # game id
        self.board = []

        self.turn = 0

    def start(self):
        self.board = self.init_board()
        return 0

    def init_board(self):
        board = []

        for y in range(3):
            board.append([])
            for _ in range(3):
                board[y].append(" ")

        return board
    
    def play(self, x, y):
        if x < 0 or x > 2 or y < 0 or y > 2:
            return 1
        
        if self.board[y][x] == self.symbols["empty"]:
            self.board[y][x] = self.symbols[str(self.turn)]

            if self.check_win() == 0:
                return self.win()
            elif self.check_draw() == 0:
                return self.draw()

            self.turn = 1 if self.turn == 0 else 0

            return 0
        return 1
    
    def check_win(self):
        # check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != self.symbols["empty"]:
                return 0
        
        # check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != self.symbols["empty"]:
                return 0
        
        # check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != self.symbols["empty"]:
            return 0
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != self.symbols["empty"]:
            return 0
        
        return 1
    
    def check_draw(self):
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == self.symbols["empty"]:
                    return 1
        return 0
    
    def win(self):
        return 2
    
    def draw(self):
        return 3