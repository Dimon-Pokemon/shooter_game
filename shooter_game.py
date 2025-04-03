#Создай собственный Шутер!
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
            super().__init__()
            self.image = transform.scale(image.load(player_image), (65, 65))    
            self.speed = player_speed
            self.rect = self.image.get_rect()
            self.rect.x = player_x
            self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


window = display.set_mode((700, 500))

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    # Нарисовать на window задний фон (background) в координате x=0, y=0
    window.blit(background, (0, 0))

    # Отрисовка экрана
    display.update() 