import pygame

class InGameClock():
    # adds
    def gametime_addday(self):
        pass

    def gametime_addhour(self):
        self.gametime['hour'] += 1
        if self.gametime['hour'] > 23:
            self.gametime['hour'] -= 0
            self.gametime_addday()

    def gametime_addmin(self):
        self.gametime['minute'] += 1
        if self.gametime['minute'] > 59:
            self.gametime['minute'] -= 60
            self.gametime_addhour()

    def gametime_addsec(self):
        self.gametime['second'] += 1
        if self.gametime['second'] > 59:
            self.gametime['second'] -= 60
            self.gametime_addmin()

    def normalupdate(self):
        self.gametime_addsec()
        self.update()

    def fastfix(self, string):
        string = str(string)
        if int(string) < 10:
            string = "0" + string
        return string


    def update(self):
        temp_hour = self.fastfix(self.gametime['hour'])
        temp_minute = self.fastfix(self.gametime['minute'])

        self.maintime_img = self.font.render(temp_hour+" "+temp_minute, False, (51, 41, 41)).convert_alpha()
        self.maintime_rect = self.maintime_img.get_rect(y = self.game.height * 0.05, x = self.game.width * 0.9)

    def draw(self):
        self.game.screen.blit(self.maintime_img, self.maintime_rect)

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(game.wherefonts + "Segment16C_Italic.ttf", 40)
        self.gametime = {
            "second":0,
            "minute":0,
            "hour":9,
            "day":0,
            "week":0,
            "month":0,
            "year":2359,
        }
