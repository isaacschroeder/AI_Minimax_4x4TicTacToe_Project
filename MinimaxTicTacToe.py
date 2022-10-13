# CS4750 HW4

from enum import Enum

class Tile(Enum):
    EMPTY = 0
    X = 1
    O = 2

class Player(Enum):
    PLAYER_1 = 0
    PLAYER_2 = 1

class Game:
    def __init__(self):
        # A 5 row, 6 column game board whose tiles are empty
        board = []
        for x in range(5):
            row = []
            for y in range(6):
                row.append(Tile.EMPTY)
            board.append(row)
        self.board = board

        # Assign Players a tile type
        self.p1_tile = Tile.X
        self.p2_tile = Tile.O

    # Currently assumes valid play is made.
    def makePlay(self, player, row, col):
        if player == Player.PLAYER_1:
            self.board[row][col] = self.p1_tile
        else:
            self.board[row][col] = self.p2_tile

    def getPlayAt(self, row, col):
        return self.board[row][col]

    def tileToString(self, row, col):
        play = self.getPlayAt(row, col)
        if play == Tile.X:
            return "X"
        elif play == Tile.O:
            return "O"
        else:
            return " "

    def printBoard(self):
        print("_________________________")
        for row in range(5):
            row_string = "| "
            for col in range(6):
                row_string += self.tileToString(row, col)
                row_string += " | "
            print(row_string)
            print("_________________________")

def main():
    game = Game()
    game.makePlay(Player.PLAYER_1, 3, 3)
    game.makePlay(Player.PLAYER_2, 3, 4)
    game.printBoard()

# Call to main
main()


