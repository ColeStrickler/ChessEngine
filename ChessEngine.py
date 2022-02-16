
class GameState():
    def __init__(self):
        #  board = 8x8 2d list, each element with 2 characters, first char is
        #  color of the piece, second is type of piece, "--" is an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)



    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turn back
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    # considering check
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])  # REMOVE IF STILL IN CHECK
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        return moves


    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # take opponents point of view
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # this means that square can be attacked
                return True
        return False


    # not considering check
    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):  # number of rows
            for c in range(8):  # number of columns in row
                turn = self.board[r][c][0]  # access w or b
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # uses dict to call move function based on piece type

        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r-1][c] == "--":  # 1 sq pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 sq pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c-1 >= 0:  # up-left diagonal captures
                if self.board[r-1][c-1][0] == 'b':  # enemy piece
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:  # up-right diagonal captures
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:  # black pawn moves
            if self.board[r+1][c] == "--":  # 1 sq pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 sq pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c-1 >= 0:  # down-left diagonal captures
                if self.board[r+1][c-1][0] == 'w':  # enemy piece
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:  # down-right diagonal captures
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirections = ()
        if self.whiteToMove:  # white rook moves
            print(r)
            for row in range(0, r):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                    if row-1 >=0:
                        if self.board[row-1][c][0] == "b":
                            moves.append(Move((r, c), (row-1, c), self.board))
            for row in range(r, 8):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                    if  row + 1 <= 7:
                        if self.board[row + 1][c][0] == "b":
                            moves.append(Move((r, c), (row+1, c), self.board))
            for col in range(0, c):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                    if  col - 1 >= 0:
                        if self.board[r][col-1][0] == "b":
                            moves.append(Move((r, c), (r, col-1), self.board))
            for col in range(c, 8):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                    if col + 1 <= 7:
                        if self.board[r][col+1][0] == "b":
                            moves.append(Move((r, c), (r, col+1), self.board))
            if r+1 <= 7:
                if self.board[r+1][c][0] == "b":
                    moves.append(Move((r, c), (r+1, c), self.board))
            if r-1 >= 0:
                if self.board[r-1][c][0] == "b":
                    moves.append(Move((r, c), (r-1, c), self.board))
            if c+1 <= 7:
                if self.board[r][c+1][0] == "b":
                    moves.append(Move((r, c), (r, c+1), self.board))
            if c-1 >= 0:
                if self.board[r][c-1][0] == "b":
                    moves.append(Move((r, c), (r, c-1), self.board))

        if not self.whiteToMove:  # black rook moves
            print(r)
            for row in range(0, r):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                    if row-1 >=0:
                        if self.board[row-1][c][0] == "w":
                            moves.append(Move((r, c), (row-1, c), self.board))
            for row in range(r, 8):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                    if  row + 1 <= 7:
                        if self.board[row + 1][c][0] == "w":
                            moves.append(Move((r, c), (row+1, c), self.board))
            for col in range(0, c):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                    if  col - 1 >= 0:
                        if self.board[r][col-1][0] == "w":
                            moves.append(Move((r, c), (r, col-1), self.board))
            for col in range(c, 8):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                    if col + 1 <= 7:
                        if self.board[r][col+1][0] == "w":
                            moves.append(Move((r, c), (r, col+1), self.board))
            if r+1 <= 7:
                if self.board[r+1][c][0] == "w":
                    moves.append(Move((r, c), (r+1, c), self.board))
            if r-1 >= 0:
                if self.board[r-1][c][0] == "w":
                    moves.append(Move((r, c), (r-1, c), self.board))
            if c+1 <= 7:
                if self.board[r][c+1][0] == "w":
                    moves.append(Move((r, c), (r, c+1), self.board))
            if c-1 >= 0:
                if self.board[r][c-1][0] == "w":
                    moves.append(Move((r, c), (r, c-1), self.board))

    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
            if r+2 <= 7 and c+1 <= 7:
                if self.board[r+2][c+1] == "--" or self.board[r+2][c+1][0] == "b":
                    moves.append(Move((r, c), (r+2, c+1), self.board))
            if r-2 >= 0 and c+1 <= 7:
                if self.board[r-2][c+1] == "--" or self.board[r-2][c+1][0] == "b":
                    moves.append(Move((r, c), (r-2, c+1), self.board))
            if r-2 >= 0 and c-1 >= 0:
                if self.board[r-2][c-1] == "--" or self.board[r-2][c-1][0] == "b":
                    moves.append(Move((r, c), (r-2, c-1), self.board))
            if r+2 <= 7 and c-1 >= 0:
                if self.board[r+2][c-1] == "--" or self.board[r+2][c-1][0] == "b":
                    moves.append(Move((r, c), (r+2, c-1), self.board))


            if r + 1 <= 7 and c + 2 <= 7:
                if self.board[r + 1][c + 2] == "--" or self.board[r + 1][c + 2][0] == "b":
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
            if r - 1 >= 0 and c + 2 <= 7:
                if self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
            if r - 1 >= 0 and c - 2 >= 0:
                if self.board[r - 1][c - 2] == "--" or self.board[r - 1][c - 2][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
            if r + 1 <= 7 and c - 2 >= 0:
                if self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == "b":
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))

        if not self.whiteToMove:
            if r+2 <= 7 and c+1 <= 7:
                if self.board[r+2][c+1] == "--" or self.board[r+2][c+1][0] == "w":
                    moves.append(Move((r, c), (r+2, c+1), self.board))
            if r-2 >= 0 and c+1 <= 7:
                if self.board[r-2][c+1] == "--" or self.board[r-2][c+1][0] == "w":
                    moves.append(Move((r, c), (r-2, c+1), self.board))
            if r-2 >= 0 and c-1 >= 0:
                if self.board[r-2][c-1] == "--" or self.board[r-2][c-1][0] == "w":
                    moves.append(Move((r, c), (r-2, c-1), self.board))
            if r+2 <= 7 and c-1 >= 0:
                if self.board[r+2][c-1] == "--" or self.board[r+2][c-1][0] == "w":
                    moves.append(Move((r, c), (r+2, c-1), self.board))
            if r + 1 <= 7 and c + 2 <= 7:
                if self.board[r + 1][c + 2] == "--" or self.board[r + 1][c + 2][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
            if r - 1 >= 0 and c + 2 <= 7:
                if self.board[r - 1][c + 2] == "--" or self.board[r - 1][c + 2][0] == "w":
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
            if r - 1 >= 0 and c - 2 >= 0:
                if self.board[r - 1][c - 2] == "--" or self.board[r - 1][c - 2][0] == "w":
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
            if r + 1 <= 7 and c - 2 >= 0:
                if self.board[r + 1][c - 2] == "--" or self.board[r + 1][c - 2][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))

    def getKingMoves(self, r, c, moves):
        if self.whiteToMove:
            if r + 1 <= 7:
                if self.board[r+1][c] == "--" or self.board[r+1][c][0] == "b":
                    moves.append(Move((r, c), (r+1, c), self.board))
            if c + 1 <= 7:
                if self.board[r][c+1] == "--" or self.board[r][c+1][0] == "b":
                    moves.append(Move((r, c), (r, c+1), self.board))
            if r - 1 >= 0:
                if self.board[r-1][c] == "--" or self.board[r-1][c][0] == "b":
                    moves.append(Move((r, c), (r-1, c), self.board))
            if c - 1 >= 0:
                if self.board[r][c-1] == "--" or self.board[r][c-1][0] == "b":
                    moves.append(Move((r, c), (r, c-1), self.board))
            if c - 1 >= 0 and r - 1 >= 0:
                if self.board[r-1][c-1] == "--" or self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c + 1 <= 7 and r - 1 >= 0:
                if self.board[r-1][c+1] == "--" or self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            if c - 1 >= 0 and r + 1 <= 7:
                if self.board[r+1][c-1] == "--" or self.board[r+1][c-1][0] == "b":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c + 1 <= 7 and r + 1 <= 7:
                if self.board[r+1][c+1] == "--" or self.board[r+1][c+1][0] == "b":
                    moves.append(Move((r, c), (r+1, c+1), self.board))
        if not self.whiteToMove:
            if r + 1 <= 7:
                if self.board[r+1][c] == "--" or self.board[r+1][c][0] == "w":
                    moves.append(Move((r, c), (r+1, c), self.board))
            if c + 1 <= 7:
                if self.board[r][c+1] == "--" or self.board[r][c+1][0] == "w":
                    moves.append(Move((r, c), (r, c+1), self.board))
            if r - 1 >= 0:
                if self.board[r-1][c] == "--" or self.board[r-1][c][0] == "w":
                    moves.append(Move((r, c), (r-1, c), self.board))
            if c - 1 >= 0:
                if self.board[r][c-1] == "--" or self.board[r][c-1][0] == "w":
                    moves.append(Move((r, c), (r, c-1), self.board))
            if c - 1 >= 0 and r - 1 >= 0:
                if self.board[r-1][c-1] == "--" or self.board[r-1][c-1][0] == "w":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c + 1 <= 7 and r - 1 >= 0:
                if self.board[r-1][c+1] == "--" or self.board[r-1][c+1][0] == "w":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            if c - 1 >= 0 and r + 1 <= 7:
                if self.board[r+1][c-1] == "--" or self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c + 1 <= 7 and r + 1 <= 7:
                if self.board[r+1][c+1] == "--" or self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
            row = r
            col = c
            while row <= 7 and col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row + 1 <= 7 and col + 1 <= 7:
                        if self.board[row+1][col+1][0] == "b":
                            moves.append(Move((r, c), (row+1, col+1), self.board))
                row += 1
                col += 1
            row = r
            col = c
            while row >= 0 and col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row - 1 >= 0 and col + 1 <= 7:
                        if self.board[row-1][col+1][0] == "b":
                            moves.append(Move((r, c), (row-1, col+1), self.board))
                row -= 1
                col += 1
            row = r
            col = c

            while row >= 0 and col >= 0:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row - 1 >= 0 and col - 1 >= 0:
                        if self.board[row - 1][col - 1][0] == "b":
                            moves.append(Move((r, c), (row - 1, col - 1), self.board))
                row -= 1
                col -= 1
            row = r
            col = c
            while row <= 7 and col >= 0:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row + 1 <= 7 and col - 1 >= 0:
                        if self.board[row + 1][col - 1][0] == "b":
                            moves.append(Move((r, c), (row - 1, col + 1), self.board))
                row += 1
                col -= 1
            if r + 1 <= 7 and c + 1 <= 7:
                if self.board[r+1][c+1][0] == "b":
                    moves.append(Move((r, c), (r+1, c+1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r+1][c-1][0] == "b":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
        if not self.whiteToMove:
            row = r
            col = c
            while row <= 7 and col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row + 1 <= 7 and col + 1 <= 7:
                        if self.board[row+1][col+1][0] == "w":
                            moves.append(Move((r, c), (row+1, col+1), self.board))
                row += 1
                col += 1
            row = r
            col = c
            while row >= 0 and col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row - 1 >= 0 and col + 1 <= 7:
                        if self.board[row-1][col+1][0] == "w":
                            moves.append(Move((r, c), (row-1, col+1), self.board))
                row -= 1
                col += 1
            row = r
            col = c

            while row >= 0 and col >= 0:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row - 1 >= 0 and col - 1 >= 0:
                        if self.board[row - 1][col - 1][0] == "w":
                            moves.append(Move((r, c), (row - 1, col - 1), self.board))
                row -= 1
                col -= 1
            row = r
            col = c
            while row <= 7 and col >= 0:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row + 1 <= 7 and col - 1 >= 0:
                        if self.board[row + 1][col - 1][0] == "w":
                            moves.append(Move((r, c), (row - 1, col + 1), self.board))
                row += 1
                col -= 1
            if r + 1 <= 7 and c + 1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r-1][c+1][0] == "w":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r-1][c-1][0] == "w":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))

    def getQueenMoves(self, r, c, moves):
        if self.whiteToMove:  # white queen moves
            print(r)
            for row in range(0, r):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                    if row-1 >=0:
                        if self.board[row-1][c][0] == "b":
                            moves.append(Move((r, c), (row-1, c), self.board))
            for row in range(r, 8):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                    if  row + 1 <= 7:
                        if self.board[row + 1][c][0] == "b":
                            moves.append(Move((r, c), (row+1, c), self.board))
            for col in range(0, c):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                    if  col - 1 >= 0:
                        if self.board[r][col-1][0] == "b":
                            moves.append(Move((r, c), (r, col-1), self.board))
            for col in range(c, 8):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                    if col + 1 <= 7:
                        if self.board[r][col+1][0] == "b":
                            moves.append(Move((r, c), (r, col+1), self.board))
            if r+1 <= 7:
                if self.board[r+1][c][0] == "b":
                    moves.append(Move((r, c), (r+1, c), self.board))
            if r-1 >= 0:
                if self.board[r-1][c][0] == "b":
                    moves.append(Move((r, c), (r-1, c), self.board))
            if c+1 <= 7:
                if self.board[r][c+1][0] == "b":
                    moves.append(Move((r, c), (r, c+1), self.board))
            if c-1 >= 0:
                if self.board[r][c-1][0] == "b":
                    moves.append(Move((r, c), (r, c-1), self.board))
            row = r
            col = c
            while row <= 7 and col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row + 1 <= 7 and col + 1 <= 7:
                        if self.board[row + 1][col + 1][0] == "b":
                            moves.append(Move((r, c), (row + 1, col + 1), self.board))
                row += 1
                col += 1
            row = r
            col = c
            while row >= 0 and col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row - 1 >= 0 and col + 1 <= 7:
                        if self.board[row - 1][col + 1][0] == "b":
                            moves.append(Move((r, c), (row - 1, col + 1), self.board))
                row -= 1
                col += 1
            row = r
            col = c

            while row >= 0 and col >= 0:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row - 1 >= 0 and col - 1 >= 0:
                        if self.board[row - 1][col - 1][0] == "b":
                            moves.append(Move((r, c), (row - 1, col - 1), self.board))
                row -= 1
                col -= 1
            row = r
            col = c
            while row <= 7 and col >= 0:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row + 1 <= 7 and col - 1 >= 0:
                        if self.board[row + 1][col - 1][0] == "b":
                            moves.append(Move((r, c), (row - 1, col + 1), self.board))
                row += 1
                col -= 1
            if r + 1 <= 7 and c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "b":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
        if not self.whiteToMove:  # black queen moves
            print(r)
            for row in range(0, r):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                    if row-1 >=0:
                        if self.board[row-1][c][0] == "w":
                            moves.append(Move((r, c), (row-1, c), self.board))
            for row in range(r, 8):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                    if  row + 1 <= 7:
                        if self.board[row + 1][c][0] == "w":
                            moves.append(Move((r, c), (row+1, c), self.board))
            for col in range(0, c):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                    if  col - 1 >= 0:
                        if self.board[r][col-1][0] == "w":
                            moves.append(Move((r, c), (r, col-1), self.board))
            for col in range(c, 8):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                    if col + 1 <= 7:
                        if self.board[r][col+1][0] == "w":
                            moves.append(Move((r, c), (r, col+1), self.board))
            if r+1 <= 7:
                if self.board[r+1][c][0] == "w":
                    moves.append(Move((r, c), (r+1, c), self.board))
            if r-1 >= 0:
                if self.board[r-1][c][0] == "w":
                    moves.append(Move((r, c), (r-1, c), self.board))
            if c+1 <= 7:
                if self.board[r][c+1][0] == "w":
                    moves.append(Move((r, c), (r, c+1), self.board))
            if c-1 >= 0:
                if self.board[r][c-1][0] == "w":
                    moves.append(Move((r, c), (r, c-1), self.board))
            row = r
            col = c
            while row <= 7 and col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row + 1 <= 7 and col + 1 <= 7:
                        if self.board[row + 1][col + 1][0] == "w":
                            moves.append(Move((r, c), (row + 1, col + 1), self.board))
                row += 1
                col += 1
            row = r
            col = c
            while row >= 0 and col <= 7:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row - 1 >= 0 and col + 1 <= 7:
                        if self.board[row - 1][col + 1][0] == "w":
                            moves.append(Move((r, c), (row - 1, col + 1), self.board))
                row -= 1
                col += 1
            row = r
            col = c

            while row >= 0 and col >= 0:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row - 1 >= 0 and col - 1 >= 0:
                        if self.board[row - 1][col - 1][0] == "w":
                            moves.append(Move((r, c), (row - 1, col - 1), self.board))
                row -= 1
                col -= 1
            row = r
            col = c
            while row <= 7 and col >= 0:
                if self.board[row][col] == "--":
                    moves.append(Move((r, c), (row, col), self.board))
                    if row + 1 <= 7 and col - 1 >= 0:
                        if self.board[row + 1][col - 1][0] == "w":
                            moves.append(Move((r, c), (row - 1, col + 1), self.board))
                row += 1
                col -= 1
            if r + 1 <= 7 and c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))








class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile((self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol))

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
