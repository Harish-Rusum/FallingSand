import pygame
import sys
import random

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation")

baseColor = (255, 255, 255)
sand = (194, 178, 128)
concrete = (128, 128, 128)
water = (0, 150, 225)

gridSize = 80
cellSize = width // gridSize


class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]


    def gravity(self):
        for i in range(len(self.grid) - 2, -1, -1):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    if self.grid[i + 1][j] == 0:
                        self.grid[i][j] = 0
                        self.grid[i + 1][j] = 1
                    elif self.grid[i + 1][j] in [1, 2]:
                        if j > 0 and self.grid[i + 1][j - 1] == 0:
                            self.grid[i][j] = 0
                            self.grid[i + 1][j - 1] = 1
                        elif j < gridSize - 1 and self.grid[i + 1][j + 1] == 0:
                            self.grid[i][j] = 0
                            self.grid[i + 1][j + 1] = 1

                if self.grid[i][j] == 3:
                    if self.grid[i + 1][j] == 0:
                        self.grid[i][j] = 0
                        self.grid[i + 1][j] = 3
                    else:
                        left = j > 0 and self.grid[i][j - 1] == 0
                        right = j < gridSize - 1 and self.grid[i][j + 1] == 0
                        if left and right:
                            if random.randint(0, 1) == 0:
                                self.grid[i][j] = 0
                                self.grid[i][j - 1] = 3
                            else:
                                self.grid[i][j] = 0
                                self.grid[i][j + 1] = 3
                        elif left:
                            self.grid[i][j] = 0
                            self.grid[i][j - 1] = 3
                        elif right:
                            self.grid[i][j] = 0
                            self.grid[i][j + 1] = 3

    def draw(self, win):
        for i in range(gridSize):
            for j in range(gridSize):
                rect = pygame.Rect(j * cellSize, i * cellSize, cellSize, cellSize)
                if self.grid[i][j] == 1:
                    pygame.draw.rect(win, sand, rect)
                elif self.grid[i][j] == 2:
                    pygame.draw.rect(win, concrete, rect)
                elif self.grid[i][j] == 3:
                    pygame.draw.rect(win, water, rect)

    def handleMouseClick(self, pos, material):
        x, y = pos
        row = y // cellSize
        col = x // cellSize

        dirs = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                dirs.append([i, j])

        for dir in dirs:
            newRow = row + dir[0]
            newCol = col + dir[1]
            if 0 <= newRow < gridSize and 0 <= newCol < gridSize:
                self.grid[newRow][newCol] = material

    def erase(self, pos):
        x, y = pos
        row = y // cellSize
        col = x // cellSize
        dirs = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                dirs.append([i, j])

        for dir in dirs:
            newRow = row + dir[0]
            newCol = col + dir[1]
            if 0 <= newRow < gridSize and 0 <= newCol < gridSize:
                self.grid[newRow][newCol] = 0


sim = Grid()

def main():
    clock = pygame.time.Clock()
    running = True
    currentMaterial = 1

    while running:
        screen.fill(baseColor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    currentMaterial = 1
                elif event.key == pygame.K_2:
                    currentMaterial = 2
                elif event.key == pygame.K_3:
                    currentMaterial = 3

        if pygame.mouse.get_pressed()[0]:
            sim.handleMouseClick(pygame.mouse.get_pos(), currentMaterial)
        if pygame.mouse.get_pressed()[2]:
            sim.erase(pygame.mouse.get_pos())

        sim.gravity()
        sim.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


main()
