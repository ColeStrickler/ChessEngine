import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
INITIALIZE GLOBAL DICT OF IMAGES
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # LOADS EACH IMAGE AND SCALES THEM TO THE CORRECT SIZE


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill((p.Color("white")))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # use this variable to only get valid moves when game state changes
    loadImages()
    running = True
    sqSelected = ()  # no square selected initially, keeps track of last click
    playerClicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #  mouse handler

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # saves x,y of mouse click
                col = location[0]//SQ_SIZE  # // to round the divide
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):  # reset clicks if user clicks same square twice
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:  # enter after there have been two clicks
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []  # empty afterward
                    else:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

# responsible for graphics in the game state
def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on board
    drawPieces(screen, gs.board)  # draw pieces on top of the boards


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":  # draw if not an empty square
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == "__main__":
    main()

