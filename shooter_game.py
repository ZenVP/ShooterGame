#Create your own shooter
x = 325
y = 35
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

from pygame import *
from random import *
import time as timer
window_width = 700
window_height = 600
window = display.set_mode((window_width, window_height))

display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (window_width, window_height))

fps = 60
clock = time.Clock()


class Character(sprite.Sprite):
    def __init__(self, filename, size_x, size_y, x, y, speed, hp):
        sprite.Sprite.__init__(self)
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale( image.load(self.filename), (self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.max_hp = hp
        self.hp = hp
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class UFO(Character):
    def update(self):
        global passed_counter
        self.rect.y += self.speed
        if self.rect.y > 590:
            self.rect.y = 0
            passed_counter += 1
    def shot(self):
        global kill_count
        self.hp -= 1
        if (self.hp == 0):
            self.rect.y = 0
            self.rect.x = randint(50, window_width-100)
            self.hp = self.max_hp
            kill_count = kill_count + 1

class Bullet(Character):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > 590:
            self.rect.y = 0

player = Character("bullet.png", 50 , 100, 325, 475, 5, 20)
bullet_group = sprite.Group()
ufo_group = sprite.Group()

ufo = UFO("rocket.png", 100 , 50 , 100 , 50 , 5, 1)
ufo_group.add(ufo)
ufo = UFO("rocket.png", 100 , 50 , 200 , 50 , 5, 1)
ufo_group.add(ufo)
ufo = UFO("rocket.png", 100 , 50 , 300 , 50 , 5, 1)
ufo_group.add(ufo)
ufo = UFO("rocket.png", 100 , 50 , 400 , 50 , 5, 1)
ufo_group.add(ufo)
ufo = UFO("rocket.png", 100 , 50 , 500 , 50 , 5, 1)
ufo_group.add(ufo)

bullet_group = sprite.Group()
total_amount_of_bullet = 1000
bullet_remain = total_amount_of_bullet
last_fire_time = timer.time()
game = True
finish = False
font.init()
style = font.Font(None, 36)
blink_count = 0
kill_count = 0
passed_counter = 0
extra_ufo25 = True
extra_ufo50 = True
extra_ufo75 = True

while game:
    window.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish == False:
        keys_pressed = key.get_pressed()

        if keys_pressed[K_RIGHT] and player.rect.x < window_width-player.size_x:
            player.rect.x += player.speed   
        elif keys_pressed[K_LEFT] and player.rect.x > 0:
            player.rect.x -= player.speed
        if keys_pressed[K_SPACE] and timer.time() - last_fire_time > 0.1 and bullet_remain > 0:
            last_fire_time = timer.time()  
            bullet_remain = bullet_remain - 1
            bullet = Bullet("ufo.png", 20 , 20 , player.rect.x  + 14 , 450 , 2, 0)
            bullet_group.add(bullet)
        if bullet_remain == 0:
            if timer.time() - last_fire_time > 2: 
                bullet_remain = total_amount_of_bullet    
                if (blink_count < 20):
                    text_reload = style.render("Reloading Your Bullets:", 1, (255, 255, 255))
                    blink_count += 1
                elif (blink_count < 40):
                    text_reload = style.render("", 1, (255, 255, 255))
                    blink_count += 1
                else:
                    blink_count = 0
                window.blit(text_reload, (220, 350))
        
        collide_list = sprite.spritecollide( player, ufo_group, False)
        for ufo in collide_list:
            ufo.rect.y = 0
            ufo.rect.x = randint(50, window_width-100)
            player.hp = player.hp - 1

        ufo_group.update()
        bullet_group.update()

        collide_list = sprite.groupcollide(bullet_group, ufo_group, True, False)
        for bullet in collide_list:
            collide_list[bullet][0].shot()
        if kill_count >= 25 and extra_ufo25 == True:
            ufo = UFO("rocket.png", 200 , 100 , 300 , 50 , 3, 5)
            ufo_group.add(ufo)
            extra_ufo25 = False
        if kill_count >= 50 and extra_ufo50 == True:
            ufo = UFO("rocket.png", 200 , 100 , 300 , 50 , 2, 6)
            ufo_group.add(ufo)    
            extra_ufo50 = False
        if kill_count >= 75 and extra_ufo75 == True:
            ufo = UFO("rocket.png", 200 , 100 , 300 , 50 , 1, 7)
            ufo_group.add(ufo)
            extra_ufo75 = False
        if kill_count == 100:
            finish = True
        if player.hp <= 0:
            finish = True
        if passed_counter >= 50:
            finish = True
    else:
        if kill_count == 100:
            text_bullet = style.render("You Win!", 1, (255, 255, 255))
            window.blit(text_bullet, (20, 300))
        if player.hp <= 0:
            text_bullet = style.render("You Lose!", 1, (255, 255, 255))
            window.blit(text_bullet, (320, 300))
        if passed_counter >= 50:
            text_bullet = style.render("You lose!", 1, (255, 255, 255))
            window.blit(text_bullet, (320, 300))

    player.draw()

    ufo_group.draw(window)
    bullet_group.draw(window)

    text_bullet = style.render("Bullet:" + str(bullet_remain), 1, (255, 255, 255))
    window.blit(text_bullet, (20, 20))
    text_hp = style.render("HP:" + str(player.hp), 1, (255, 255, 255))
    window.blit(text_hp, (20, 40))
    text_kill_count = style.render("Kill_count:" + str(kill_count), 1, (255, 255, 255))
    window.blit(text_kill_count, (20, 60))
    text_Passed_count = style.render("Rockets Passed:" + str(passed_counter), 1, (255, 255, 255))
    window.blit(text_Passed_count, (20, 80))
    display.update()
    clock.tick(fps)