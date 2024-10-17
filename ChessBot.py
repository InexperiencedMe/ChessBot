import cv2 as cv
import numpy as np
import pyautogui as pag
import chess
import chess.engine
import time

pieceNames = {
    'bKing'     : 'k',
    'bQueen'    : 'q',
    'bRook'     : 'r',
    'bBishop'   : 'b',
    'bKnight'   : 'n',
    'bPawn'     : 'p',
    'wKnight'   : 'N',
    'wPawn'     : 'P',
    'wKing'     : 'K',
    'wQueen'    : 'Q',
    'wRook'     : 'R',
    'wBishop'   : 'B'
}

def locatePieces(screenshot):
    pieceLocations = {
        'bKing'    : [],
        'bQueen'   : [],
        'bRook'    : [],
        'bBishop'  : [],
        'bKnight'  : [],
        'bPawn'    : [],
        'wKnight'  : [],
        'wPawn'    : [],
        'wKing'    : [],
        'wQueen'   : [],
        'wRook'    : [],
        'wBishop'  : []
    }

    for piece in pieceNames.keys():
        tempLocationsList = []
        pieceImg = cv.imread("pieces/" + piece + '.png', 0)
        desiredPieceSize = (int(cellSize), int(cellSize))
        pieceResized = cv.resize(pieceImg, desiredPieceSize, interpolation = cv.INTER_AREA)
        for location in pag.locateAll(pieceResized, screenshot, confidence=matchingConfidence, grayscale=True):
           tempLocationsList.append(location)
           tempLocationsList.append(location)
        pieceLocations[piece], weights = cv.groupRectangles(tempLocationsList, 1, 0.5)
    return pieceLocations

def locationsToFEN(pieceLocations):
    fen = ""
    x = boardTopLeft[0]
    y = boardTopLeft[1]


    for row in range(8):
        empty = 0
        for column in range(8):
            hasPiece = False
            for piece in pieceLocations.keys():
                for location in pieceLocations[piece]:
                    if abs(x - location[0]) < detectionThreshold and abs(y - location[1]) < detectionThreshold:
                        hasPiece = True
                        if empty > 0:
                            fen += str(empty)
                            empty = 0
                        fen += pieceNames[piece]
            if not hasPiece:
                empty += 1
            x += cellSize

        if empty > 0:
            fen += str(empty)
        if row < 7: fen += '/'

        x = boardTopLeft[0]
        y += cellSize

    fen += ' '+playerSide+' - - 0 1' # No en passant and no castling. White to move
    print("FEN: "+fen)
    return fen

def calculateBestMove(fen):
    try:
        engine = chess.engine.SimpleEngine.popen_uci("Engine/stockfish-windows-2022-x86-64-avx2.exe")
        board = chess.Board(fen=fen)
        bestMove = str(engine.play(board, chess.engine.Limit(time=1)).move)
        print("Best move: "+bestMove)
        return bestMove
    except:
        print("Impossible position. Cannot find a legal move")
        exit()

def playMove(bestMove):
    mouseInitial = (boardTopLeft[0]+cellSize/2,boardTopLeft[1]+cellSize/2) # a8
    mouseFrom = (mouseInitial[0]+cellSize*(ord(bestMove[0])-97), mouseInitial[1]+cellSize*(8-int(bestMove[1])))
    mouseTo = (mouseInitial[0]+cellSize*(ord(bestMove[2])-97), mouseInitial[1]+cellSize*(8-int(bestMove[3])))

    pag.moveTo(mouseFrom[0], mouseFrom[1], 0.5)
    pag.click()
    pag.moveTo(mouseTo[0], mouseTo[1], 0.5)
    pag.click()

    time.sleep(0.4)
    waitForYourTurn(mouseTo[0], mouseTo[1])

def getScreenshot(mode=0):
    pag.screenshot('screenshot.png')
    return cv.imread('screenshot.png', mode)

def initializeParameters():
    cornerRef = cv.imread("CornerRef.png")
    screenshot = getScreenshot()
    ret, screenshot = cv.threshold(screenshot, 160, 255, cv.THRESH_BINARY)
    tempLocationsList = []
    for location in pag.locateAll(cornerRef, screenshot, confidence=0.8, grayscale=True):
        tempLocationsList.append(location)
        tempLocationsList.append(location)
    locationsList, weights = cv.groupRectangles(tempLocationsList, 1, 0.5)


    if abs(locationsList[0][1] - locationsList[1][1]) < 2: # Comparing Y's of first 2 corners just to be sure
        cellSize = (locationsList[1][0] - locationsList[0][0])/2
        boardSize = cellSize*8
        boardTopLeft = (locationsList[0][0]+cornerRef.shape[0]/2-cellSize, locationsList[0][1]+cornerRef.shape[0]/2-cellSize)
    else:
        print("Something went wrong while setting initial parameters")
    print(cellSize,boardTopLeft)
    return cellSize, boardSize, boardTopLeft

def waitForYourTurn(lastMoveX, lastMoveY):
    cellCornerX = int(lastMoveX - cellSize/2)
    cellCornerY = int(lastMoveY - cellSize/2)
    print("CellCornerX: "+str(cellCornerX))
    print("CellCornerY: " + str(cellCornerY))
    cellImage = getScreenshot(1)[int(cellCornerY):int(cellCornerY+cellSize),int(cellCornerX):int(cellCornerX+cellSize),:]
    # We Will check just the blue channel, as the color highlight is usually yellow, so lack of blue
    cellColor = np.average(cellImage[:, :, 2])
    while True:
        cellImage = getScreenshot(1)[int(cellCornerY):int(cellCornerY+cellSize),int(cellCornerX):int(cellCornerX+cellSize),:]
        newCellColor = np.average(cellImage[:, :, 2])
        if int(newCellColor) == int(cellColor):
            #It is still opponent's turn, we gotta wait
            continue
        else:
            break


cellSize, boardSize, boardTopLeft = initializeParameters()
matchingConfidence = 0.75
detectionThreshold = 5

# 'w' for white, 'b' for black
playerSide = 'w'

while True:
    screenshot = getScreenshot()
    ret, screenshot = cv.threshold(screenshot, 50, 255, cv.THRESH_BINARY)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_GRAY2RGB)
    pieceLocations = locatePieces(screenshot)
    fen = locationsToFEN(pieceLocations)
    bestMove = calculateBestMove(fen)
    playMove(bestMove)
    time.sleep(0.4)