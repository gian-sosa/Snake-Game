import pygame
import numpy as np
import time
import math

pygame.init()
size = width, height = 700, 700
numberXCells = 60
numberYCells = 60
sizeCellWidth = (width - 1) / numberXCells
sizeCellHeight = (height - 1) / numberYCells
background = 25, 25, 25
screen = pygame.display.set_mode((height, width), pygame.RESIZABLE)
screen.fill(background)
gameState = np.zeros((numberXCells, numberYCells))
print(gameState)
pauseExec = False
while 1:
    newGameState = np.copy(gameState)
    eventt = pygame.event.get()
    for event in eventt:
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            positionX, positionY = pygame.mouse.get_pos()
            if 0 < positionX < (width - 1) and 0 < positionY < (height - 1):
                newGameState[math.floor(positionX / sizeCellWidth),
                             math.floor(positionY / sizeCellHeight)] = mouseClick[0] and not mouseClick[2]
    screen.fill(background)
    for y in range(0, numberYCells):
        for x in range(0, numberXCells):
            if not pauseExec:
                numberNeigh = gameState[(x - 1) % numberXCells, (y - 1) % numberYCells] + \
                              gameState[(x) % numberXCells, (y - 1) % numberYCells] + \
                              gameState[(x + 1) % numberXCells, (y - 1) % numberYCells] + \
                              gameState[(x - 1) % numberXCells, (y) % numberYCells] + \
                              gameState[(x + 1) % numberXCells, (y) % numberYCells] + \
                              gameState[(x - 1) % numberXCells, (y + 1) % numberYCells] + \
                              gameState[(x) % numberXCells, (y + 1) % numberYCells] + \
                              gameState[(x + 1) % numberXCells, (y + 1) % numberYCells]
                # R1: Una celula muerta con exactamente 3 celulas vecinas vivas NACE
                if gameState[x, y] == 0 and numberNeigh == 3:
                    newGameState[x, y] = 1
                # R2: Una celula viva con 2 o 3 celulas vecinas vivas sigue VIVA, en otro caso MUERE
                elif gameState[x, y] == 1 and (numberNeigh < 2 or numberNeigh > 3):
                    newGameState[x, y] = 0

            poly = [((x) * sizeCellWidth, (y) * sizeCellHeight),
                    ((x + 1) * sizeCellWidth, (y) * sizeCellHeight),
                    ((x + 1) * sizeCellWidth, (y + 1) * sizeCellHeight),
                    (x * sizeCellWidth, (y + 1) * sizeCellHeight)]
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
    time.sleep(1 / 30)
    gameState = np.copy(newGameState)
    pygame.display.flip()
