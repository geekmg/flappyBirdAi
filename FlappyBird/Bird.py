import pygame


class Bird(pygame.sprite.Sprite):

    def __init__(self, displayScreen, SCREENWIDTH, SCREENHEIGHT):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./assets/redbird.png')

        self.SCREENWIDTH = SCREENWIDTH
        self.SCREENHEIGHT = SCREENHEIGHT
        self.x = int(SCREENWIDTH * 0.2)
        self.y = SCREENHEIGHT * 0.5

        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.screen = displayScreen

        self.playerVelY = -9
        self.playerMaxVelY = 10
        self.playerMinVelY = -8
        self.playerAccY = 1
        self.playerFlapAcc = -9
        self.playerFlapped = False

        self.display(self.x, self.y)

    def display(self, x, y):

        self.screen.blit(self.image, (x, y))
        self.rect.x, self.rect.y = x, y

    def move(self, input):

        if input != None:
            self.playerVelY = self.playerFlapAcc
            self.playerFlapped = True

        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False

        self.y += min(self.playerVelY, self.SCREENHEIGHT - self.y - self.height)
        self.y = max(self.y, 0)
        self.display(self.x, self.y)
