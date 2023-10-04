import pygame
import time
import sys
import random
import subprocess
import os
from PIL import Image
# REMEMBER: USE PILLOW library NOT PIL!


from scene import *
import ingameclock


def fixvc(text, num):
    text = round(text, 2)
    text = str(text)
    while num >= len(text):
        text = "0" + text
        num -= 1
    return text



class Arrow(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.img = pygame.image.load(self.game.whereimg+"arrow.png").convert_alpha()
        self.tick = 0
        self.rect = self.img.get_rect(x=0, y=0)
    def render(self):
        self.game.screen.blit(self.img, self.rect)
    def update(self):
        self.tick += 1
        if self.tick > 40:
            self.tick = 0
        if self.tick < 20:
            temp_x = 280+(3*self.tick)
        else:
            temp_x = 340-(3*(self.tick-20))

        self.rect = self.img.get_rect(x = temp_x, y = 320+(abs(self.game.menunumber-5)*60))

class ven_1(pygame.sprite.Sprite):
    def __init__(self, y, game, id):
        self.y = y
        self.x = 1280
        self.game = game
        self.id = id
        self.image = pygame.image.load(self.game.whereimg+"menu_airship.png").convert_alpha()
        self.rect = self.image.get_rect(x=self.x, y=self.y)
    def render(self):
        self.game.screen.blit(self.image, self.rect)
    def update(self):
        self.x -= 10
        self.rect = self.image.get_rect(x = self.x, y = self.y)
        if self.x < -300:
            self.game.vens_d.append(self)
    def Del(self):
        del self.game.vens[self.id]
        del self

class menu():

    # create new air ship for the menu
    def new_ven(self):
        id_ = random.randint(0, 50000000)
        temp = ven_1(random.randint(0, 500), self, id_)
        self.vens.update({id_:temp})


    # load settings from settings.json
    def loadsettings(self):
        settings_file = os.path.abspath(os.path.dirname(__file__))+"\\assets\\settings.json"
        if os.path.exists(settings_file):
            tempfile = open(settings_file)
            tempjson = json.load(tempfile)
            self.settings = tempjson
        else:
            self.savesettings()

    def savesettings(self):
        settings_file = os.path.abspath(os.path.dirname(__file__)) + "\\assets\\settings.json"
        tempjson = json.dumps(self.settings, indent=4)
        with open(settings_file, "w") as outfile:
            outfile.write(tempjson)


    # def editor_changetile(self):
    #
    #     while True:
    #         g = input("Tile:\n>>")
    #         if g == "/list":
    #             print("0 - air")
    #             print("1 - metal_block")
    #             print("2 - Stone")
    #         elif g.isnumeric():
    #             self.gameeditor_usedtile = g
    #             print("tak")
    #             break
    #         else: print("nie")

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        self.keys(keys)

        if self.devmode_animtemp2:
            self.devmode_animtemp += 1
            if self.devmode_animtemp < 30:
                self.devmode_info_rect = self.devmode_info.get_rect(y = self.height - 100, x = self.devmode_animtemp * 10)
                self.devmode_info2_rect = self.devmode_info2.get_rect(y = self.height - 100, x = self.devmode_animtemp * 10 + 140)

            else:
                self.devmode_info_rect = self.devmode_info.get_rect(y = self.height - 100, x = 300-(self.devmode_animtemp - 30 )* 10)
                self.devmode_info2_rect = self.devmode_info2.get_rect(y = self.height - 100, x = 300-(self.devmode_animtemp - 30 )* 10 + 140)
            if self.devmode_animtemp > 60:
                self.devmode_info_rect = self.devmode_info.get_rect(y=-500,x=-500)
                self.devmode_info2_rect = self.devmode_info.get_rect(y=-500, x=-500)
                self.devmode_animtemp = 0
                self.devmode_animtemp2 = False




        if self.devmode:
            tempmouse = pygame.mouse.get_pos()
            tempmouse += self.mainscene.camera_group.offset
            self.devmode_mousepos_img = self.global_font_sm.render("Mouse pos, spos: [" +
                                                                   str(pygame.mouse.get_pos()[0]) + "," +
                                                                   str(pygame.mouse.get_pos()[1]) + "], [" +
                                                                   str(tempmouse.x) + "," + str(tempmouse.y) + "]",
                                                                   False,
                                                                   (255, 255, 255)).convert_alpha()
            self.devmode_mousepos_rect = self.devmode_playerpos_img.get_rect(x=30, y=220)
            self.devmode_counter += 1
            if self.devmode_counter > 3:

                x, y = self.mainscene.player.pos

                TempPlayerPos = round(x, 2), round(y,2)

                x, y = self.mainscene.player.speed

                TempPlayerSpeed = round(x, 2), round(y,2)

                self.devmode_playerpos_img = self.global_font_sm.render("Player: "
                                                                        + str(TempPlayerPos) + ", "
                                                                        + str(TempPlayerSpeed) + ", "
                                                                        + str(self.mainscene.player.acc),
                                                                        False, (255, 255, 255)).convert_alpha()
                self.devmode_playerpos_rect = self.devmode_playerpos_img.get_rect(x=30, y=200)




        if self.settings['showfps']:
            self.showfps_counter += 1
            if self.showfps_counter > 10:


                if self.settings['showfps']:
                    self.showfps_counter = 0

                    self.fps_img = self.global_font.render(str(int(self.clock.get_fps())) + " FPS", False, (255,0,0)).convert_alpha()
                    self.fps_rect = self.fps_img.get_rect(y = 30, x = 0)
        if self.menu:
            if self.counting_v == 120:
                self.counting_v = 0
                self.new_ven()
            else:
                self.counting_v += 1
            for ven_id, ven in self.vens.items():
                ven.update()
            for ven in self.vens_d:
                ven.Del()
            del self.vens_d
            self.vens_d = []
            self.arrow.update()




    def gfx(self):
        self.screen.fill((0, 0, 0))
        if self.menu:
            self.screen.blit(self.background_image, self.background_rect)
            for ven_id, ven in self.vens.items():
                ven.render()
            self.screen.blit(self.menu_img, self.menu_rect)
            self.screen.blit(self.awsdmenu_img, self.awsdmenu_rect)
            if self.showarrow:
                self.arrow.render()
            if self.selected:
                self.screen.blit(self.selected_img, self.selected_rect)
            if self.submenu == "settings" or self.submenu == "settings.maxfps":
                self.screen.blit(self.showfps_simg, self.showfps_srect)
                self.screen.blit(self.maxfps_simg, self.maxfps_srect)
        else:
            self.mainscene.loop()
            self.mainscene.gfx()

        if self.devmode:
            self.screen.blit(self.devmode_playerpos_img, self.devmode_playerpos_rect)
            self.screen.blit(self.devmode_mousepos_img, self.devmode_mousepos_rect)
            self.screen.blit(self.devmode_keysinfo_img, self.devmode_keysinfo_rect)
            self.screen.blit(self.devmode_keysinfo2_img, self.devmode_keysinfo2_rect)

        if self.gamestopped:
            self.screen.blit(self.gamestopped_img, self.gamestopped_rect)
            self.screen.blit(self.gamestopped_text, self.gamestopped_textrect)

        if self.settings['showfps']:
            self.screen.blit(self.fps_img, self.fps_rect)



        if self.devmode_animtemp2:
            self.screen.blit(self.devmode_info, self.devmode_info_rect)
            self.screen.blit(self.devmode_info2, self.devmode_info2_rect)
        pygame.display.flip()
    def menuspace(self):
        match self.submenu:
            case "main":
                match self.menunumber:
                    case 1:
                        # Close game
                        self.savesettings()
                        pygame.quit()
                        sys.exit()
                    case 2:
                        # Settings
                        self.awsdmenu_img = self.global_font.render(
                            "Use W, S, ESC and Space to manage menu.", False, (255, 255, 255))
                        self.awsdmenu_rect = self.awsdmenu_img.get_rect(x=15, y=685)
                        self.submenu = "settings"
                        self.menu_img = pygame.image.load(self.whereimg+"menu_settings.png").convert_alpha()
                        self.menu_rect = self.menu_img.get_rect(x=30, y=300)
                        self.menunumber = 5
                        self.keysafe = 10
                    case 3:
                        # open mods folder
                        #print(mod_path)
                        subprocess.Popen(f'explorer "{self.mod_path}"')
                        self.keysafe = 10
                    case 5:
                        # newgame
                        self.awsdmenu_img = self.global_font.render(
                            "Use W, S, ESC and Space to manage menu.", False, (255, 255, 255))
                        self.awsdmenu_rect = self.awsdmenu_img.get_rect(x=15, y=685)
                        self.submenu = "newgame"
                        self.menu_img = pygame.image.load(self.whereimg+"menu_newgame.png").convert_alpha()
                        self.menu_rect = self.menu_img.get_rect(x=30, y=300)
                        self.menunumber = 5
                        self.keysafe = 10
            case "newgame":
                # newgame
                # set dificulty level (higher = more dificulty)
                self.submenu = "game"
                self.dificulty = abs(self.menunumber - 5)
                self.mainscene = Scene(self)
                self.menu = False
                self.scene = True
                self.vens = {}

            case "settings":
                match self.menunumber:
                    case 2:
                        self.awsdmenu_img = self.global_font.render(
                            "Use W, S and Space to manage menu.", False, (255, 255, 255))
                        self.awsdmenu_rect = self.awsdmenu_img.get_rect(x=15, y=685)
                        self.selected = True
                        self.submenu = "settings.maxfps"
                        self.selected_img = pygame.image.load(self.whereimg+"menu_selected.png").convert_alpha()
                        self.selected_rect = self.selected_img.get_rect(y = 480, x = 45)
                        self.showarrow = False
                        self.keysafe = 10
                    case 3:
                        if self.settings['showfps']:
                            self.settings['showfps'] = False
                            self.showfps_simg = pygame.image.load(self.whereimg+"off.png").convert_alpha()
                            self.showfps_srect = self.showfps_simg.get_rect(y = 440, x = 210)
                            self.keysafe = 10
                        else:
                            self.settings['showfps'] = True
                            self.showfps_simg = pygame.image.load(self.whereimg+"on.png").convert_alpha()
                            self.showfps_srect = self.showfps_simg.get_rect(y=440, x=210)
                            self.keysafe = 10
            case "settings.maxfps":
                self.awsdmenu_img = self.global_font.render(
                    "Use W, S, ESC and Space to manage menu.", False, (255, 255, 255)).convert_alpha()
                self.awsdmenu_rect = self.awsdmenu_img.get_rect(x=15, y=685)
                self.submenu = "settings"
                self.showarrow = True
                self.selected = False
                self.menunumber = 2
                self.keysafe = 10
    def fpsup(self):
        match self.settings['maxfps']:
            case 15:
                self.settings['maxfps'] = 30
            case 30:
                self.settings['maxfps'] = 60
            case 60:
                self.settings['maxfps'] = 120
            case 120:
                self.settings['maxfps'] = 99999999999999
        self.setrect_likefps()
    def fpsdown(self):
        match self.settings['maxfps']:
            case 15:
                pass
            case 30:
                self.settings['maxfps'] = 15
            case 60:
                self.settings['maxfps'] = 30
            case 120:
                self.settings['maxfps'] = 60
            case _:
                self.settings['maxfps'] = 120
        self.setrect_likefps()
    def setrect_likefps(self):
        match self.settings['maxfps']:
            case 15:
                self.maxfps_simg = pygame.image.load(self.whereimg+"15.png").convert_alpha()
            case 30:
                self.maxfps_simg = pygame.image.load(self.whereimg+"30.png").convert_alpha()
            case 60:
                self.maxfps_simg = pygame.image.load(self.whereimg+"60.png").convert_alpha()
            case 120:
                self.maxfps_simg = pygame.image.load(self.whereimg+"120.png").convert_alpha()
            case _:
                self.maxfps_simg = pygame.image.load(self.whereimg+"nsk.png").convert_alpha()
        self.maxfps_srect = self.maxfps_simg.get_rect(y=500, x=210)
    def keys(self, keys):
        if self.menu == True:
            if self.keysafe < 1:
                if keys[pygame.K_s]:
                    if self.submenu != "settings.maxfps" and self.menu:
                        self.menunumber -= 1
                        if self.menunumber < 1 and self.submenu != "settings":
                            self.menunumber = 1
                        elif self.menunumber < 0:
                            self.menunumber = 0
                    elif self.menu:
                        self.fpsdown()
                    self.keysafe = 10
                elif keys[pygame.K_w]:
                    if self.submenu != "settings.maxfps" and self.menu:
                        self.menunumber += 1
                        if self.menunumber > 5:
                            self.menunumber = 5
                    elif self.menu:
                        self.fpsup()
                    self.keysafe = 10
                if keys[pygame.K_SPACE]:
                    if self.menu:
                        self.menuspace()
                if keys[pygame.K_ESCAPE]:
                    if self.menu:
                        match self.submenu:
                            case "newgame" | "settings":
                                self.awsdmenu_img = self.global_font.render(
                                    "Use W, S and Space to manage menu.", False, (255, 255, 255))
                                self.awsdmenu_rect = self.awsdmenu_img.get_rect(x=15, y=685)
                                self.submenu = "main"
                                self.menu_img = pygame.image.load(self.whereimg+"menu_start.png").convert_alpha()
                                self.menu_rect = self.menu_img.get_rect(x=30, y=300)
                                self.keysafe = 10
                                self.menunumber = 5
            else:
                self.keysafe -= 1
        else:
            if keys[pygame.K_n] and self.devmode and self.keysafe == 0:
                self.mainscene.player.noclip = not self.mainscene.player.noclip
                self.keysafe = 20
            if keys[pygame.K_F8] and keys[pygame.K_l] and self.gamestopped and self.keysafe == 0:
                canenter = False

                try:
                    canenter = self.settings['dev']
                except:
                    pass
                if canenter:
                    self.devmode = not self.devmode
                    self.devmode_animtemp = 0
                    self.devmode_animtemp2 = True
                    if self.devmode:
                        self.devmode_info2 = self.global_font.render("On", False, (0, 255, 0)).convert_alpha()
                        self.devmode_info2_rect = self.devmode_info2.get_rect(x=-200, y=2-00)
                    else:
                        self.devmode_info2 = self.global_font.render("Off", False, (255, 0, 0)).convert_alpha()
                        self.devmode_info2_rect = self.devmode_info2.get_rect(x=-200, y=-200)
                    self.keysafe = 50
            if keys[pygame.K_ESCAPE] and self.keysafe == 0:
                if self.gamestopped:
                    self.keysafe = 20
                    self.gamestopped = False
                else:
                    self.keysafe = 20
                    self.gamestopped = True

            if self.keysafe != 0:
                self.keysafe -= 1


            self.mainscene.keys(keys)
    def __init__(self):

        # settings
        self.settings = {
            "maxfps":60,
            "showfps":False,
            "tickrate":20,
            "resx":1280,
            "resy":720,
            "paths":
                {
                    "path_mod":"\\mods\\",
                    "path_assets":"\\assets\\"

                }


        }

        self.loadsettings()
        # inits

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("The Spacers")

        # basic informations
        self.height = self.settings['resy']
        self.width = self.settings['resx']
        self.res = self.width, self.height
        self.screen = pygame.display.set_mode(self.res)

        self.tickrate = self.settings['tickrate']



        self.mylocalisation = os.path.abspath(os.path.dirname(__file__))
        self.mod_path = self.mylocalisation + self.settings['paths']['path_mod']
        self.assets = self.mylocalisation + self.settings['paths']['path_assets']
        self.defaulttiles = self.mylocalisation + self.settings['paths']['path_assets'] +"tiles\\"
        self.whereimg = self.mylocalisation + self.settings['paths']['path_assets'] + "img\\"
        self.wheremusic = self.mylocalisation + self.settings['paths']['path_assets'] + "music\\"
        self.whereraudio = self.mylocalisation + self.settings['paths']['path_assets'] + "audio\\" # raudio means reactions audio
        self.wherefonts = self.mylocalisation + self.settings['paths']['path_assets'] + "fonts\\"
        self.wheremaps = self.mylocalisation + self.settings['paths']['path_assets'] + "maps\\"

        self.keysafe = 0
        self.clock = pygame.time.Clock()
        self.delta = 0
        #self.showfps = self.settings['showfps']
        self.exit = True  # if self.exit is False game will be closed
        self.setrect_likefps()

        self.devmode = False  # dev mode allows you console and other (f8 and l to change mode)
        try:
            if self.settings['dev'] == True:
                self.canenterdevmode = True
        except:
            pass






        # fonts
        self.global_font = pygame.font.Font(self.wherefonts + "ariblk.ttf", 20)
        self.global_font_sm = pygame.font.Font(self.wherefonts + "ariblk.ttf", 15)
        self.monster_font = pygame.font.Font(self.wherefonts + "monster.ttf", 95)

        # variables for dev mode

        self.devmode_info = self.global_font.render("Dev Mode: ", False, (30, 30, 30)).convert_alpha()
        self.devmode_info_rect = self.devmode_info.get_rect(x = 200, y = 200)

        self.devmode_info2 = self.global_font.render("Off", False, (30, 30, 30)).convert_alpha()
        self.devmode_info2_rect = self.devmode_info2.get_rect(x = 200, y = 200)

        self.devmode_animtemp = 0
        self.devmode_animtemp2 = False



        self.devmode_playerpos_img = self.global_font.render("Player: (0,0), (0,0), (0,0)", False, (255,255,255)).convert_alpha()
        self.devmode_playerpos_rect = self.devmode_playerpos_img.get_rect(x = -200, y = -200)
        self.devmode_mousepos_img = self.global_font.render("Mouse pos, spos: (0,0), (0,0)", False, (255,255,255)).convert_alpha()
        self.devmode_mousepos_rect = self.devmode_playerpos_img.get_rect(x = -200, y = -200)


        self.devmode_keysinfo_img = self.global_font_sm.render("H to hide menu, N for Noclip, ~ for console", False,
                                                               (255, 255, 255)).convert_alpha()
        self.devmode_keysinfo_rect = self.devmode_keysinfo_img.get_rect(x=30, y=240)

        self.devmode_keysinfo2_img = self.global_font_sm.render("Also use J to change tile, = to Save Map", False, (255, 255, 255)).convert_alpha()
        self.devmode_keysinfo2_rect = self.devmode_keysinfo2_img.get_rect(x = 30, y = 260)

        self.devmode_counter = 0

        # game editor

        self.gameeditor_usedtile = 0


        # game stopped blackout

        self.gamestopped = False
        self.gamestopped_img = pygame.image.load(self.whereimg+"blackout_1280x720.png").convert_alpha()
        self.gamestopped_img = pygame.transform.scale(self.gamestopped_img, self.res)
        self.gamestopped_rect = self.gamestopped_img.get_rect(x = 0, y = 0)
        self.gamestopped_text = self.monster_font.render("Game Stopped!", False, (255,255,255)).convert_alpha()

        self.gamestopped_textrect = self.gamestopped_text.get_rect(y = int(self.height*0.3), x = int(self.width * 0.4))


        # menu music
        pygame.mixer.music.load(self.wheremusic+'menusong.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # setup fps counter (settings)
        if self.settings['showfps']:
            self.showfps_simg = pygame.image.load(self.whereimg+"on.png").convert_alpha()
            self.showfps_srect = self.showfps_simg.get_rect(y=440, x=210)
        else:
            self.showfps_simg = pygame.image.load(self.whereimg+"off.png").convert_alpha()
            self.showfps_srect = self.showfps_simg.get_rect(y=440, x=210)

        # setup fps counter (real)

        self.showfps_counter = 0
        self.fps_img = self.global_font.render("Unkown FPS", False,(255, 0, 0)).convert_alpha()
        self.fps_rect = self.fps_img.get_rect(y=30, x=0)



        # setup start menu
        self.awsdmenu_img = self.global_font.render("Use W, S and Space to manage menu.", False, (255,255,255)).convert_alpha()
        self.awsdmenu_rect = self.awsdmenu_img.get_rect(x = 15, y = 685)
        self.menu_img = pygame.image.load(self.whereimg+"menu_start.png")
        self.menu_rect = self.menu_img.get_rect(x= 30, y = 300)

        # menu background

      #  temp_image = Image.open(self.whereimg + "menu_background.png")
        #temp_image.resize(self.res)

        self.background_image = pygame.image.load(self.whereimg + "menu_background.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, self.res)
        self.background_rect = self.background_image.get_rect(x = 0, y = 0)

        # setup arrow and selected box and other similar like submenu system
        self.arrow = Arrow(self)
        self.showarrow = True
        self.selected = False
        self.menunumber = 5
        self.submenu = "main"
        self.menu = True

        # time clock

        self.GameClock = ingameclock.InGameClock(self)

        # airships (menu)
        self.vens = {}
        self.vens_d = []   # table for deleting airships
        self.counting_v = 0

        # general loop
        while exit:
            self.delta += self.clock.tick(self.settings['maxfps'])
            if self.delta >= self.tickrate:
                self.delta -= self.tickrate
                self.loop()
            self.gfx()





Game = menu()





