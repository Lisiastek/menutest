import os.path

import pygame
import blocks
from pygame.math import Vector2

class gui_hearth(pygame.sprite.Sprite):
    usekeys = False
    def __init__(self, img):
        super().__init__()
        self.isimportant = False
        self.isgui = True
        self.pos = Vector2(0,0)
        self.importantlevel = 50
        self.img = pygame.image.load(img).convert_alpha()
        self.rect = self.img.get_rect(x = 0, y = 0)


class tile_cursor(pygame.sprite.Sprite):
    usekeys = False
    def __init__(self, img):
        super().__init__()
        self.isgui = True
        self.isimportant = True
        self.importantlevel = 25
        self.pos = Vector2(0,0)

        self.img = pygame.image.load(img).convert_alpha()
        self.rect = self.img.get_rect(x = 0, y = 0)


class CameraGroup(pygame.sprite.Group):
    def updategui(self, hp):

        cursor_pos = pygame.mouse.get_pos()
        # cursor_pos = cursor_pos + self.offset

        self.grid_x = (cursor_pos[0] + self.offset.x) // 40
        self.grid_y = (cursor_pos[1] + self.offset.y) // 40
        self.tile_cursor.rect = self.tile_cursor.img.get_rect(x=self.grid_x * 40, y=self.grid_y * 40)

        for sprite in self.sprites():
            # tile selector
            # if isinstance(sprite, tile_cursor):
            #     cursor_pos = pygame.mouse.get_pos()
            #     #cursor_pos = cursor_pos + self.offset
            #
            #     self.grid_x = (cursor_pos[0] + self.offset.x ) // 40
            #     self.grid_y = (cursor_pos[1] + self.offset.y) // 40


                # sprite.rect = sprite.img.get_rect(x = self.grid_x * 40, y = self.grid_y * 40)

                # grid_x = grid_x + self.offset.x / 40
                # grid_y = grid_y + self.offset.y / 40
                #
                # #print(self.offset, temp_offset)
                #
                #
                #
                # sprite.rect = sprite.img.get_rect(x = grid_x, y = grid_y)


           # self.scene.tile_cursor.rect(x = temp_x, y = temp_y)



            # hearth icons
            if isinstance(sprite, gui_hearth):
                sprite.kill()
        x_temp = 10
        while hp != 0:
            if hp > 1:
                temp_ob = gui_hearth(self.scene.game.whereimg+"\\gui\\hearth_full.png")
                temp_ob.add(self)
                temp_ob.rect = temp_ob.img.get_rect(y = 10, x = x_temp)
                x_temp += 45
                hp -= 1
            elif hp >= 0.75:
                temp_ob = gui_hearth(self.scene.game.whereimg+"\\gui\\hearth_75.png")
                temp_ob.add(self)
                temp_ob.rect = temp_ob.img.get_rect(y = 10, x = x_temp)
                x_temp += 45
                hp = 0
            elif hp >= 0.50:
                temp_ob = gui_hearth(self.scene.game.whereimg+"\\gui\\hearth_half.png")
                temp_ob.add(self)
                temp_ob.rect = temp_ob.img.get_rect(y = 10, x = x_temp)
                x_temp += 45
                hp = 0
            elif hp >= 0.25:
                temp_ob = gui_hearth(self.scene.game.whereimg+"\\gui\\hearth_25.png")
                temp_ob.add(self)
                temp_ob.rect = temp_ob.img.get_rect(y = 10, x = x_temp)
                x_temp += 45
                hp = 0


            # update layer information
        # if self.scene.game.devmode and self.scene.editor_buildmode:
        #     match self.scene.editor_selectedlayer:
        #         case _:
        #

    def updategui_selectedlayer(self):
        match self.scene.editor_selectedlayer:
            case 1:
                self.tilechangerlayer_img = self.scene.game.global_font.render("TOP", False, (255, 255, 255)).convert_alpha()
            case 2:
                self.tilechangerlayer_img = self.scene.game.global_font.render("BG1", False, (255, 255, 255)).convert_alpha()
            case 3:
                self.tilechangerlayer_img = self.scene.game.global_font.render("BG2", False, (255, 255, 255)).convert_alpha()
            case 4:
                self.tilechangerlayer_img = self.scene.game.global_font.render("BG3", False, (255, 255, 255)).convert_alpha()
            case 5:
                self.tilechangerlayer_img = self.scene.game.global_font.render("EVE", False, (255, 255, 255)).convert_alpha()
            case _:
                self.tilechangerlayer_img = self.scene.game.global_font.render("ERR", False, (255, 255, 255)).convert_alpha()

        self.tilechangerlayer_rect = self.tilechangerlayer_img.get_rect(x=self.scene.game.width * 0.85,
                                                                        y=self.scene.game.height // 20)

    def rendergui(self):
        for sprite in self.sprites():
            # if isinstance(sprite, tile_cursor):
            #     self.display.blit(sprite.img, sprite.rect)
            if isinstance(sprite, gui_hearth):

                self.display.blit(sprite.img, sprite.rect)

        self.scene.game.GameClock.draw()
        
        if self.scene.game.devmode and self.scene.editor_buildmode:
            self.display.blit(self.tile_changer_img, self.tile_changer_rect)
            self.display.blit(self.tilechangerlayer_img, self.tilechangerlayer_rect)




    def get_actually_by(self, object):
        self.offset.x = object.pos.x - self.scene.game.width //2
        self.offset.y = object.pos.y - self.scene.game.height //2
    def get_actually_by_box(self, object):
        if object.rect.left < self.camerabox_rect.left:
            self.camerabox_rect.left = object.rect.left

        if object.rect.right > self.camerabox_rect.right:
            self.camerabox_rect.right = object.rect.right

        if object.rect.top < self.camerabox_rect.top:
            self.camerabox_rect.top = object.rect.top

        if object.rect.bottom > self.camerabox_rect.bottom:
            self.camerabox_rect.bottom = object.rect.bottom


        self.offset.x = self.camerabox_rect.left - self.camerabox_borders['left']
        self.offset.y = self.camerabox_rect.top - self.camerabox_borders['top']
    def __init__(self, scene):
        super().__init__()
        self.scene = scene

        # background tiles

        self.BT1 = BackgroundTilesGroup(self)
        self.BT2 = BackgroundTilesGroup(self)
        self.BT3 = BackgroundTilesGroup(self)

        # for editor

        self.tile_cursor = tile_cursor(self.scene.game.whereimg + "\\gui\\map_grid.png")

        self.tile_changer_img = pygame.image.load(self.scene.game.whereimg + "\\gui\\none_tile.png").convert_alpha()
        self.tile_changer_rect = self.tile_changer_img.get_rect(x = self.scene.game.width * 0.8, y = self.scene.game.height // 20)

        self.tilechangerlayer_img = self.scene.game.global_font.render("TOP", False, (255, 255, 255)).convert_alpha()
        self.tilechangerlayer_rect = self.tilechangerlayer_img.get_rect(x = self.scene.game.width * 0.85, y = self.scene.game.height // 20)


        # get area to draw
        self.display = pygame.display.get_surface()

        # Camera box



        self.camerabox_borders = {'top': 100, 'bottom': 100, 'left': 200, 'right': 200}

        self.camerabox_left = self.camerabox_borders['left']
        self.camerabox_right = self.camerabox_borders['top']
        self.camerabox_width = self.display.get_size()[0] - self.camerabox_borders['left'] - self.camerabox_borders['right']
        self.camerabox_height = self.display.get_size()[1] - self.camerabox_borders['top'] - self.camerabox_borders['bottom']

        self.camerabox_rect = pygame.Rect(self.camerabox_left,self.camerabox_right,self.camerabox_width,self.camerabox_height)



        self.ground = blocks.Object(self.scene, "null", "\\img\\map_background.png", Vector2(0,0), True, False)

        # Variable for Camera moving
        self.offset = Vector2(0,0)
    def gfx(self):
        # rendering ground

        offset_temp = self.ground.rect.center - self.offset
        self.display.blit(self.ground.img, offset_temp)

        # rendering background tiles

        self.BT3.draw(self.display)
        self.BT2.draw(self.display)
        self.BT1.draw(self.display)



        # sorting common main sprites and tiles

        sorted_group = sorted(self.sprites(), key = lambda sprite: sprite.rect.centery)

        # rendering common sprites
        for sprite in sorted_group:
            if sprite.isgui == False and sprite.isimportant == False:
                if isinstance(sprite, blocks.Player):
                    offset_temp_tilecursor = self.tile_cursor.rect.topleft - self.offset
                    self.display.blit(self.tile_cursor.img, offset_temp_tilecursor)
                offset_temp = sprite.rect.topleft - self.offset
                self.display.blit(sprite.img,offset_temp)

        # offset_temp_tilecursor = self.tile_cursor.rect.topleft - self.offset
        # self.display.blit(self.tile_cursor.img, offset_temp_tilecursor)

        for sprite in sorted_group:
            if sprite.isimportant:
                if isinstance(sprite, tile_cursor):
                    continue
                offset_temp = sprite.rect.topleft - self.offset
                self.display.blit(sprite.img,offset_temp)
        #pygame.draw.rect(self.display, 'yellow', self.camerabox_rect, 5)


        # render gui

        self.rendergui()
    def keys(self, keys):
        for sprite in self.sprites():
            if sprite.usekeys == True:
                sprite.keys(keys)



class BackgroundTilesGroup(pygame.sprite.Group):
    def draw(self, display):
        for sprite in self.sprites():
            offset_temp = sprite.rect.topleft - self.RT.offset
            display.blit(sprite.img, offset_temp)
    def __init__(self, maincameragroup):
        super().__init__()
        self.RT = maincameragroup