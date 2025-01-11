import pygame
import sys
import random

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Water and sand sim")

baseColor = (255, 255, 255)
sand = (194, 178, 128)
concrete = (128, 128, 128)
water = (0, 150, 225)

gridSize = 80
cellSize = width // gridSize



class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]
        self.colors = [[baseColor for _ in range(gridSize)] for _ in range(gridSize)]

    def reset(self):
        self.grid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]
        self.colors = [[baseColor for _ in range(gridSize)] for _ in range(gridSize)]

    def getDitheredColor(self, material):
        if material == 1:
            return (
                max(0, min(255, sand[0] + random.randint(-10, 10))),
                max(0, min(255, sand[1] + random.randint(-2, 2))),
                max(0, min(255, sand[2] + random.randint(-10, 10)))
            )
        elif material == 2:
            return (
                max(0, min(255, concrete[0] + random.randint(-2, 2))),
                max(0, min(255, concrete[1] + random.randint(-2, 2))),
                max(0, min(255, concrete[2] + random.randint(-2, 2)))
            )
        elif material == 3:
            return (
                max(0, min(255, water[0] + random.randint(-5, 5))),
                max(0, min(255, water[1] + random.randint(-5, 5))),
                max(0, min(255, water[2] + random.randint(-10, 10)))
            )
        return baseColor

    def handleMouseClick(self, pos, material, size):
        x, y = pos
        row = y // cellSize
        col = x // cellSize

        dirs = []
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                dirs.append([i, j])

        for dir in dirs:
            newRow = row + dir[0]
            newCol = col + dir[1]
            if 0 <= newRow < gridSize and 0 <= newCol < gridSize:
                if random.randint(0, 1) == 1:
                    self.grid[newRow][newCol] = material
                    self.colors[newRow][newCol] = self.getDitheredColor(material)

    def erase(self, pos, size):
        x, y = pos
        row = y // cellSize
        col = x // cellSize
        dirs = []
        for i in range(-size, size + 1):
            for j in range(-size, size + 1):
                dirs.append([i, j])

        for dir in dirs:
            newRow = row + dir[0]
            newCol = col + dir[1]
            if 0 <= newRow < gridSize and 0 <= newCol < gridSize:
                self.grid[newRow][newCol] = 0
                self.colors[newRow][newCol] = baseColor

    def gravity(self):
        for i in range(len(self.grid) - 2, -1, -1):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    if self.grid[i + 1][j] == 0:
                        self.grid[i][j] = 0
                        self.grid[i + 1][j] = 1
                        self.colors[i + 1][j] = self.colors[i][j]
                        self.colors[i][j] = baseColor
                    elif self.grid[i + 1][j] in [1, 2]:
                        if j > 0 and self.grid[i + 1][j - 1] == 0:
                            self.grid[i][j] = 0
                            self.grid[i + 1][j - 1] = 1
                            self.colors[i + 1][j - 1] = self.colors[i][j]
                            self.colors[i][j] = baseColor
                        elif j < gridSize - 1 and self.grid[i + 1][j + 1] == 0:
                            self.grid[i][j] = 0
                            self.grid[i + 1][j + 1] = 1
                            self.colors[i + 1][j + 1] = self.colors[i][j]
                            self.colors[i][j] = baseColor

                if self.grid[i][j] == 3:
                    if self.grid[i + 1][j] == 0:
                        self.grid[i][j] = 0
                        self.grid[i + 1][j] = 3
                        self.colors[i + 1][j] = self.colors[i][j]
                        self.colors[i][j] = baseColor
                    else:
                        left = j > 0 and self.grid[i][j - 1] == 0
                        right = j < gridSize - 1 and self.grid[i][j + 1] == 0
                        if left and right:
                            if random.randint(0, 1) == 0:
                                self.grid[i][j] = 0
                                self.grid[i][j - 1] = 3
                                self.colors[i][j - 1] = self.colors[i][j]
                                self.colors[i][j] = baseColor
                            else:
                                self.grid[i][j] = 0
                                self.grid[i][j + 1] = 3
                                self.colors[i][j + 1] = self.colors[i][j]
                                self.colors[i][j] = baseColor
                        elif left:
                            self.grid[i][j] = 0
                            self.grid[i][j - 1] = 3
                            self.colors[i][j - 1] = self.colors[i][j]
                            self.colors[i][j] = baseColor
                        elif right:
                            self.grid[i][j] = 0
                            self.grid[i][j + 1] = 3
                            self.colors[i][j + 1] = self.colors[i][j]
                            self.colors[i][j] = baseColor

    def draw(self, win):
        for i in range(gridSize):
            for j in range(gridSize):
                rect = pygame.Rect(j * cellSize, i * cellSize, cellSize, cellSize)
                pygame.draw.rect(win, self.colors[i][j], rect)
sim = Grid()

def main():
    clock = pygame.time.Clock()
    running = True
    currentMaterial = 1
    currentSize = 0
    holdingDown = False
    holdingUp = False

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
                elif event.key == pygame.K_c:
                    sim.reset()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if not holdingUp:
                currentSize += 1
                holdingUp = True
        else:
            holdingUp = False

        if keys[pygame.K_DOWN]:
            if not holdingDown:
                currentSize = max(0,currentSize - 1)
                holdingDown = True
        else:
            holdingDown = False

        if pygame.mouse.get_pressed()[0]:
            sim.handleMouseClick(pygame.mouse.get_pos(), currentMaterial,currentSize)
        if pygame.mouse.get_pressed()[2]:
            sim.erase(pygame.mouse.get_pos(), currentSize)

        sim.gravity()
        sim.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


main()
