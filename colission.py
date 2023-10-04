import pygame
from pygame.math import Vector2

class ColissionGroup(pygame.sprite.Group):
    def checkcolide(self, object):
        hits = pygame.sprite.spritecollide(object, self.sprites(), False)
        for sprite in hits:
            if object.rect.colliderect(sprite):


                if abs(sprite.rect.top - object.rect.bottom) < 15:
                    if object.speed.y > 0:
                        object.speed.y = 0


                elif abs(sprite.rect.bottom - object.rect.top) < 15:
                    if object.speed.y < 0:
                        object.speed.y = 0


                elif abs(sprite.rect.right - object.rect.left) < 10:
                    if object.speed.x < 0:
                        object.speed.x = 0
                elif abs(sprite.rect.left - object.rect.right) < 10:
                    if object.speed.x > 0:
                        object.speed.x = 0

    def __init__(self):
        super().__init__()
