import pygame
from pygame.math import Vector2
import colission

class Object(pygame.sprite.Sprite):
    usekeys = False
    isgui = False
    isimportant = False
    importantlevel = 0
    def __init__(self, scene, group, graphic, pos, isalpha, iscollide, tile_name="__null"):
        self.tile_name = tile_name
        if group == "null":
            super().__init__()
        else:
            super().__init__(group)
        if isalpha:
            self.img = pygame.image.load(scene.game.assets + graphic).convert_alpha()
        else:
            self.img = pygame.image.load(scene.game.assets + graphic).convert()
        if iscollide:
            self.collide = True
            scene.collide_group.add(self)
        else:
            self.collide = False
        self.scene = scene
        self.pos = pos
        self.rect = self.img.get_rect(center=self.pos)
    def update(self, *args, **kwargs):
        self.rect = self.img.get_rect(center=self.pos)
    def keys(self, keys):
        pass

class PhysicObject(Object):



    def update(self, *args, **kwargs):
        Object.update(self, *args, **kwargs)


        self.speed.x = round(self.speed.x, 2)
        self.speed.y = round(self.speed.y, 2)

        if abs(self.speed.x) == 0.01:
            self.speed.x = 0
        if abs(self.speed.y) == 0.01:
            self.speed.y = 0

        self.speed *= self.air_reistance

        self.speed += self.acc



        # collision
        if self.noclip == False:
            self.scene.collide_group.checkcolide(self)

        self.pos += self.speed
        self.acc = Vector2(0,0)



    def __init__(self, scene, group, graphic, pos, isalpha, iscollide):
        Object.__init__(self, scene, group, graphic, pos, isalpha, iscollide)

        self.speed = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.air_reistance = 0.65
        self.maxspeed = Vector2(0,0)
        self.accspeed = 2.5
        self.noclip = False

class Player(PhysicObject):
    ks = 0
    def update(self, *args, **kwargs):
        PhysicObject.update(self, *args, **kwargs)
    def keys(self, keys):
        if keys[pygame.K_w]:
            self.acc.y -= self.accspeed
        elif keys[pygame.K_s]:
            self.acc.y += self.accspeed
        if keys[pygame.K_a]:
            self.acc.x -= self.accspeed
        elif keys[pygame.K_d]:
            self.acc.x += self.accspeed


        if self.ks == 0:

            if keys[pygame.K_i]:
                self.hp -= 0.25
                self.ks = 15
            elif keys[pygame.K_o]:
                self.hp += 0.25
                self.ks = 15
        else:
            self.ks -= 1

    def __init__(self, scene, group, graphic, pos, isalpha):
        PhysicObject.__init__(self, scene, group, graphic, pos, isalpha, False)
        self.usekeys = True
        self.hp = 5
        self.importantlevel = 40
        self.isimportant = False



