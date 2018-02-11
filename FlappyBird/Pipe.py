import pygame

from FlappyBird.PipeBlock import PipeBlock
from numpy.random import randint,choice

class Pipe(pygame.sprite.Sprite):

    def __init__(self, screen, x, PIPEGAPSIZE, SCREENWIDTH):
        pygame.sprite.Sprite.__init__(self)

        self.PIPEGAPSIZE = PIPEGAPSIZE
        self.SCREENWIDTH = SCREENWIDTH
        self.screen = screen
        self.lowerBlock = PipeBlock('./assets/pipe-red.png', False)
        self.upperBlock = PipeBlock('./assets/pipe-red.png', True)

        self.pipeWidth = self.upperBlock.rect.width
        self.x = x

        heights = self.getHeight()
        self.upperY, self.lowerY = heights[0], heights[1]

        self.behindBird = 0
        self.display()

    def getHeight(self):
        # randVal = randint(1,10)
        randVal = choice([1, 2, 3, 4, 5, 6, 7, 8, 9],
                         p=[0.04, 0.04 * 2, 0.04 * 3, 0.04 * 4, 0.04 * 5, 0.04 * 4, 0.04 * 3, 0.04 * 2, 0.04])

        midYPos = 106 + 30 * randVal

        upperPos = midYPos - (self.PIPEGAPSIZE / 2)
        lowerPos = midYPos + (self.PIPEGAPSIZE / 2)

        # print(upperPos)
        # print(lowerPos)
        # print('-------')
        return ([upperPos, lowerPos])

    def display(self):
        self.screen.blit(self.lowerBlock.image, (self.x, self.lowerY))
        self.screen.blit(self.upperBlock.image, (self.x, self.upperY - self.upperBlock.rect.height))
        self.upperBlock.rect.x, self.upperBlock.rect.y = self.x, (self.upperY - self.upperBlock.rect.height)
        self.lowerBlock.rect.x, self.lowerBlock.rect.y = self.x, self.lowerY

    def move(self):
        self.x -= 3

        if self.x <= 0:
            self.x = self.SCREENWIDTH
            heights = self.getHeight()
            self.upperY, self.lowerY = heights[0], heights[1]
            self.behindBird = 0

        self.display()
        return ([self.x + (self.pipeWidth / 2), self.upperY, self.lowerY])
