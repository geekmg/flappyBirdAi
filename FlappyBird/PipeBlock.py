import pygame


class PipeBlock(pygame.sprite.Sprite):

    def __init__(self, image, upper):

        pygame.sprite.Sprite.__init__(self)

        if upper == False:
            self.image = pygame.image.load(image)
        else:
            self.image = pygame.transform.rotate(pygame.image.load(image), 180)

        self.rect = self.image.get_rect()
