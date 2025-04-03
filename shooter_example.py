from pygame import *
from random import randint
from time import time as tm

#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg') # Создали звуковой эффект
fire_sound.play() # Воспроизвели звуковой эффект

font.init()
font1 = font.Font(None, 50)
# text1 = font1.render("Пельмени", True, (100, 200, 100))

font_reload = font.Font(None, 33)
text_reload = font_reload.render("ПЕРЕЗАРЯДКА", True, (255, 0, 0))


count = 0 # Подсчет уничтоженных противников
# count_lose = 0 # Подсчет ПРОПУЩЕННЫХ противников


#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)


        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        # Отредактировать на использование класса Bullet и группы bullets
        fire_sound.play()
        bullets.add(Bullet("bullet.png", self.rect.centerx, self.rect.centery, 50, 50, 10))

class Enemy(GameSprite):

    def update(self):
        global count_loss
        global finish
        if self.rect.y + self.speed > 500:
            self.rect.y = 10
            count_loss += 1
            if count_loss > 5:
                finish = True
            
        else:
            self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        if self.rect.y < 0:
            self.kill()
        else:
            self.rect.y -= self.speed

enemy_group = sprite.Group()
for i in range(6):
    enemy_group.add(Enemy("ufo.png", randint(10, 600), 10, 50, 50, 10))

bullets = sprite.Group()
count = 0
#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

fontWin = font.Font(None, 60)
fontLoss = font.Font(None, 75)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
num_fire = 0
begin_reload_time = None # Время начала перезарядки
count_loss = 0 # Пропущенные противники
while run:
   #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
           run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire > 5:
                    time_now = tm()
                    if time_now - begin_reload_time > 2:
                        num_fire = 0
                else:
                    ship.fire()
                    num_fire += 1
                    if num_fire > 5:
                        begin_reload_time = tm()




    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        collides = sprite.groupcollide(enemy_group, bullets, True, True)
        for _ in collides:
            enemy_group.add(Enemy("ufo.png", randint(10, 600), 10, 50, 50, 10))
            count += 1
            if count > 10:
                finish = True

        text1 = font1.render(f"Побежденные: {count}", True, (100, 200, 100))
        text2 = font1.render(f"Пропущенные: {count_loss}", True, (100, 200, 100))
        enemy_group.update()
        enemy_group.draw(window)
        bullets.update()
        bullets.draw(window)
   
        window.blit(text1, (10, 10))
        window.blit(text2, (10, 75))

        #производим движения спрайтов
        ship.update()
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()

        
        if num_fire > 5:
            window.blit(text_reload, (ship.rect.centerx, ship.rect.centery))
    else:
        if count_loss > 5:
            text_loss = fontLoss.render("ВЫ ПРОИГРАЛИ", True, (255, 0, 0))
            window.blit(text_loss, (300, 300))
        else:
            text_win = fontWin.render("ВЫ ВЫЙГРАЛИ", True, (0, 255, 0))
            window.blit(text_win, (300, 300))


    display.update()
    #цикл срабатывает каждые 0.05 секунд
    time.delay(50)