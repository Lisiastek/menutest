import os

import pygame
from pygame.math import Vector2
import json

import camera
from camera import *
from blocks import *
import colission





class Scene():
    def editor_saveMapToFile(self, map_name):
        temp_json = {}
        temp_json['author'] = self.map_author
        temp_json['mapName'] = self.map_name

        temp_json['_comment1'] = "---------------------------------"
        temp_json['_comment2'] = "DONT EDIT ANYTHING DOWN BELOW!!!!"
        temp_json['_comment3'] = "---------------------------------"

        temp_json['mainTiles'] = {}
        temp_json['backgroundTiles1'] = {}
        temp_json['backgroundTiles2'] = {}
        temp_json['backgroundTiles3'] = {}

        # main
        for tile in self.tiles_main:
            if self.tiles_main[tile].tile_name != "__null":
                temp_json['mainTiles'][tile] = self.tiles_main[tile].tile_name

        # background
        for tile in self.tiles_background1:
            if self.tiles_background1[tile].tile_name != "__null":
                temp_json['backgroundTiles1'][tile] = self.tiles_background1[tile].tile_name

        # background 2
        for tile in self.tiles_background2:
            if self.tiles_background2[tile].tile_name != "__null":
                temp_json['backgroundTiles2'][tile] = self.tiles_background2[tile].tile_name

        # background 3
        for tile in self.tiles_background3:
            if self.tiles_background3[tile].tile_name != "__null":
                temp_json['backgroundTiles3'][tile] = self.tiles_background3[tile].tile_name


        finally_json = json.dumps(temp_json, indent=4)
        with open(self.game.wheremaps + map_name + ".json", "w") as outfile:
            outfile.write(finally_json)

    def editor_LoadMapFromFile(self, map_name):
        licznik = 0
        if os.path.isfile(self.game.wheremaps + map_name + ".json"):
            temp_file = open(self.game.wheremaps + map_name + ".json")
            temp_json = json.load(temp_file)
            self.map_author = temp_json['author']
            self.map_name = temp_json['mapName']

            # maintiles
            for tile in temp_json['mainTiles']:
                licznik += 1
                sep = tile.find("_")
                temp_x = tile[:sep]
                temp_y = tile[sep+1:]
                self.editor_addtile(int(temp_x), int(temp_y), temp_json['mainTiles'][tile], self.tiles_main, self.camera_group)
                #temp_cords =
                #self.editor_addtile()
                #print(tile, temp_json['mainTiles'][tile])

            # background tiles
            for tile in temp_json['backgroundTiles1']:
                licznik += 1
                sep = tile.find("_")
                temp_x = tile[:sep]
                temp_y = tile[sep + 1:]
                self.editor_addtile(int(temp_x), int(temp_y), temp_json['backgroundTiles1'][tile], self.tiles_background1, self.camera_group.BT1)
                # temp_cords =
                # self.editor_addtile()
                # print(tile, temp_json['mainTiles'][tile])

            for tile in temp_json['backgroundTiles2']:
                licznik += 1
                sep = tile.find("_")
                temp_x = tile[:sep]
                temp_y = tile[sep + 1:]
                self.editor_addtile(int(temp_x), int(temp_y), temp_json['backgroundTiles2'][tile], self.tiles_background2,
                                    self.camera_group.BT2)

            for tile in temp_json['backgroundTiles3']:
                licznik += 1
                sep = tile.find("_")
                temp_x = tile[:sep]
                temp_y = tile[sep + 1:]
                self.editor_addtile(int(temp_x), int(temp_y), temp_json['backgroundTiles3'][tile], self.tiles_background3,
                                    self.camera_group.BT3)


        else:
            print("Error: Game can't load map json file named " + str(map_name))
            print("Created not written file map with the same name")
            self.editor_saveMapToFile(str(map_name))
            return False
        print("zaladowano: " + str(licznik) + " elementow!")

    tiles_background1 = {
        # format: "X_Y": tile,
    }
    tiles_background2 = {
        # format: "X_Y": tile,
    }
    tiles_background3 = {
        # format: "X_Y": tile,
    }
    tiles_main = {
        # format: "X_Y": tile,
    }

    def editor_deltile(self, x, y, layer):
        temp_cords = str(x) + "_" + str(y)
        if temp_cords in layer:

            layer[temp_cords].kill()
            del layer[temp_cords]
        else:
            pass
            #print("niepoprawne usuwanie til'a "+temp_cords)
    def editor_addtile(self, x, y, tile_name, layer, layer2):
        try:
            if tile_name in [" ", "-"]:
                pass

            temp_cords = str(x) + "_" + str(y)

            temp_file = open(self.game.defaulttiles + tile_name + ".json")
            temp_data = json.load(temp_file)

            temp_x = (x * self.tile_size) + self.tile_size / 2
            temp_y = (y * self.tile_size) + self.tile_size / 2
            if not temp_cords in layer:
                match temp_data['objectType']:
                    case "object":
                        layer[temp_cords] = Object(self, layer2, "\\tiles\\" + temp_data['mainTexture'],
                                                   Vector2(temp_x, temp_y),
                                                        temp_data['transparent'], temp_data['colission'], tile_name)

                    case _:
                        print("Błąd z ładowaniem til'a (nieznany typ) o id: " + str(x) + ", " + str(
                                y) + " o rzekomej nazwie " + tile_name )
            else:
                self.editor_deltile(int(x), int(y), layer)
                self.editor_addtile(x, y, tile_name, layer, layer2)
        except:
            print("Błąd z ładowaniem til'a o id: " + str(x) + ", " + str(
                y) + " o rzekomej nazwie " + tile_name)


    tilemap_main = [
        "11111111111111111111111",
        "1 1 1 1 1 1 1 1 1 1 1 1",
        "2 1 5 2 1"
    ]
    hp_tmpcounter = 0
    tile_size = 40
    def generate_bytable(self, table, startcords):
        sx, sy = startcords
        for y, tile_temp in enumerate(table):
            for x, tile in enumerate(tile_temp):
                try:
                    if tile in [" ", "-"]:
                        continue
                    temp_file = open(self.game.defaulttiles + tile + ".json")
                    temp_data = json.load(temp_file)

                    #temp_x = (sx + x * self.tile_size) + self.tile_size / 2
                    #temp_y = (sy + y * self.tile_size) + self.tile_size / 2

                    match temp_data['objectType']:
                        case "object":
                            self.editor_addtile(x, y, tile, self.tiles_main)

                        case _:
                            print("Błąd z ładowaniem til'a (nieznany typ) o id: " + str(x) + ", " + str(y) + " o rzekomej nazwie " + tile)
                except:

                    print("Błąd z ładowaniem til'a o id: "+str(x)+", "+str(y)+" o rzekomej nazwie "+tile)

                # match tile:
                #     case " ":
                #         pass
                #     case "1":
                #         Object(self, self.camera_group, "1.png", Vector2(x*self.tile_size+sx, y*self.tile_size+sy), True, False)


    def editor_changetile(self):
        while True:
            tile_name = input("Tile\n>>")
            if tile_name.isnumeric():
                if tile_name == "-2":
                    break
                elif tile_name == "0":
                    self.editor_selecttile = "0"
                    self.camera_group.tile_changer_img = pygame.image.load(self.game.whereimg + "\\gui\\none_tile.png")
                    self.camera_group.tile_changer_rect = self.camera_group.tile_changer_img.get_rect(x=self.game.width * 0.8,y=self.game.height // 20)
                    break
                else:
                    if os.path.isfile(self.game.defaulttiles + tile_name + ".json"):
                        try:
                            self.editor_selecttile = tile_name
                            temp_file = open(self.game.defaulttiles + tile_name + ".json")
                            temp_json = json.load(temp_file)
                            self.camera_group.tile_changer_img = pygame.image.load(self.game.defaulttiles + temp_json['editorIcon'])
                            self.camera_group.tile_changer_rect = self.camera_group.tile_changer_img.get_rect(x = self.game.width * 0.8, y = self.game.height // 20)
                            break
                        except:
                            self.editor_selecttile = 0
                            print("wystapil nieznany blad")
                    else:
                        print("nie ma czegos takiego")
            else:
                print("Musi to być cyfra, wpisz -1 by wyswietlic liste (nie dziala) lub 0 by wybrac gumke. Możesz także za pomocą -2 wyjść")


    def keys(self, keys):
        if self.game.gamestopped == False:
            self.camera_group.keys(keys)
            if self.keysafe > 0:
                self.keysafe -= 1
            else:
                if self.game.devmode:

                    if keys[pygame.K_h]:
                        self.editor_buildmode = not self.editor_buildmode
                        self.keysafe = 20
                    if self.editor_buildmode:
                        if keys[pygame.K_j]:
                            self.editor_changetile()
                        elif keys[pygame.K_k]:
                            self.editor_selectedlayer -= 1
                            if self.editor_selectedlayer < 1:
                                self.editor_selectedlayer = 5
                            self.camera_group.updategui_selectedlayer()
                            self.keysafe = 20

                        elif keys[pygame.K_l]:
                            self.editor_selectedlayer += 1
                            if self.editor_selectedlayer > 5:
                                self.editor_selectedlayer = 1
                            self.camera_group.updategui_selectedlayer()

                            self.keysafe = 20
                            print("warstwa teraz to: " + str(self.editor_selectedlayer))
                        elif keys[pygame.K_EQUALS]:
                            self.editor_saveMapToFile("map")
                            self.keysafe = 20
                        elif pygame.mouse.get_pressed()[0]:
                            if self.editor_selecttile == "0":
                                match self.editor_selectedlayer:
                                    case 1:
                                        self.editor_deltile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                    self.tiles_main)
                                    case 2:
                                        self.editor_deltile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.tiles_background1)
                                    case 3:
                                        self.editor_deltile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.tiles_background2)
                                    case 4:
                                        self.editor_deltile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.tiles_background3)
                                    case 5:
                                        self.editor_deltile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.tiles_events)
                                    case _:
                                        print("Error: Trying to delete not exist layer")
                            else:
                                match self.editor_selectedlayer:
                                    # main layer
                                    case 1:
                                        self.editor_addtile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.editor_selecttile, self.tiles_main, self.camera_group)
                                    # background layer
                                    case 2:
                                        self.editor_addtile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.editor_selecttile, self.tiles_background1, self.camera_group.BT1)
                                    # background layer 2
                                    case 3:
                                        self.editor_addtile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.editor_selecttile, self.tiles_background2, self.camera_group.BT2)
                                    # background layer 3
                                    case 4:
                                        self.editor_addtile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.editor_selecttile, self.tiles_background3, self.camera_group.BT3)

                                    # main layer
                                    case _:
                                        self.editor_addtile(int(self.camera_group.grid_x), int(self.camera_group.grid_y),
                                                            self.editor_selecttile, self.tiles_main, self.camera_group)



    def gfx(self):
        self.camera_group.gfx()
    def loop(self):
        if self.game.gamestopped == False:
            self.game.GameClock.normalupdate()
            self.hp_tmpcounter += 1
            if self.hp_tmpcounter > 6:
                self.hp_tmpcounter = 0
                self.camera_group.updategui(self.player.hp)



            self.camera_group.update()
            self.camera_group.get_actually_by_box(self.player)
        #self.camera_group.get_actually_by(self.player)
    def __init__(self, game):
        self.game = game
        self.res = game.res
        self.keysafe = 0


        # map system
        self.editor_selecttile = "1"
        self.editor_selectedlayer = 1
        self.editor_buildmode = False

        # map_file = {
        #     "mapName":"default",
        #     "author": "patryk",
        #     "mainTiles":
        #         {
        #
        #         },
        #     "backgroundTiles":
        #         {
        #
        #         },
        #     "backgroundTiles2":
        #         {
        #
        #         },
        #     "backgroundTiles3":
        #         {
        #
        #         }
        # }

        self.map_author = "NULL"
        self.map_name = "NULL"


        self.camera_group = CameraGroup(self)

        self.collide_group = colission.ColissionGroup()
        self.player = Player(self, self.camera_group, "\\img\\player.png", Vector2(500,500), True)






        #test = Object(self, self.camera_group, "metal_block.png", Vector2(0,0), False, True)


        #self.generate_bytable(self.tilemap_main, Vector2(0,0))



        # Object(self, self.camera_group, "tree.png", Vector2(300, 300), True, False)
        # Object(self, self.camera_group, "tree.png", Vector2(400, 300), True, False)
        # Object(self, self.camera_group, "tree.png", Vector2(332, 400), True, False)
        # Object(self, self.camera_group, "tree.png", Vector2(396, 350), True, False)
        # Object(self, self.camera_group, "tree.png", Vector2(332, 332), True, False)
        # Object(self, self.camera_group, "tree.png", Vector2(319, 321), True, False)
        # Object(self, self.camera_group, "tree.png", Vector2(379, 358), True, False)
        # Object(self, self.camera_group, "tree.png", Vector2(332, 393), True, False)
        # Object(self, self.camera_group, "tree.png", Vector2(321, 372), True, False)
        #self.editor_deltile(0, 0, self.tiles_main)
        self.editor_LoadMapFromFile("map")