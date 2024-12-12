import pygame
import sys
import random

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation")

baseColor = (255, 255, 255)
sand = (194, 178, 128)

gridSize = 80
cellSize = width // gridSize

class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]

    def gravity(self):
        for i in range(len(self.grid) - 2, -1, -1):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1 and self.grid[i + 1][j] == 0:
                    self.grid[i][j] = 0
                    self.grid[i + 1][j] = 1
                elif self.grid[i][j] == 1 and self.grid[i + 1][j] == 1:
                    lBelow = self.grid[i + 1][j + 1] if j + 1 < gridSize else 1
                    rBelow = self.grid[i + 1][j - 1] if j - 1 >= 0 else 1

                    if random.randint(1, 2) == 1:
                        if lBelow == 0 and j + 1 < gridSize:
                            self.grid[i + 1][j + 1] = 1
                            self.grid[i][j] = 0
                    else:
                        if rBelow == 0 and j - 1 >= 0:
                            self.grid[i + 1][j - 1] = 1
                            self.grid[i][j] = 0

    def draw(self, win):
        for i in range(gridSize):
            for j in range(gridSize):
                rect = pygame.Rect(j * cellSize, i * cellSize, cellSize, cellSize)
                if self.grid[i][j] == 1:
                    pygame.draw.rect(win, sand, rect)

    def handleMouseClick(self, pos):
        x, y = pos
        row = y // cellSize
        col = x // cellSize

        dirs = []
        for i in range(-1,2):
            for j in range(-1,2):
                dirs.append([i,j])

        for dir in dirs:
            newRow = row + dir[0]
            newCol = col + dir[1]
            if 0 <= newRow < gridSize and 0 <= newCol < gridSize:
                self.grid[newRow][newCol] = 1 
    
    def erase(self, pos):
        x, y = pos
        row = y // cellSize
        col = x // cellSize
    
        if 0 <= row < gridSize and 0 <= col < gridSize:
            self.grid[row][col] = 0 


sim = Grid()

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(baseColor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.mouse.get_pressed()[0]:
            sim.handleMouseClick(pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[2]:
            sim.erase(pygame.mouse.get_pos())

        sim.gravity()
        sim.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

main()
