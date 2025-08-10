
from pygame import *
from random import randint
from time import time as timer

#background music
mixer.init()
mixer.music.load('fire.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#font and label
font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
kalah = font1.render('Coba Lagi!', True, (255, 50, 10))


#we need the following images:
img_back = "galaxy.jpg" #game background
img_hero = "rocket.png" #hero
img_enemy = "ufo.png" # enemy

lost = 0
score = 0
max_lost = 10
goals = 10
life = 3
reload_time = False
num_fire = 0

#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)


        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#enemy sprite class  
class Enemy(GameSprite):
   #enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        #disappears upon reaching the screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #peluru akan hilang ketika di posisi y < 0
        if self.rect.y < 0:
            self.kill()

#create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

#create bullet
bullets = sprite.Group()

#create Enemy
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

for i in range(1, 3):
    asteroid = Enemy("asteroid.png", randint(80, win_width - 80), -40, 70, 60, randint(1, 5))
    asteroids.add(asteroid)

#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
while run:
   #"Close" button press event
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reload_time == False:
                    num_fire = num_fire +1
                    fire_sound = mixer.Sound('fire.ogg')
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and reload_time == False:
                    last_time = timer()
                    reload_time = True



    if not finish:
        #update the background
        window.blit(background,(0,0))

        text = font2.render("Score:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))



        #launch sprite movements
        ship.update()


        #update them in a new location in each loop iteration
        ship.reset()

 #launch sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        #update them in a new location in each loop iteration
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if reload_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait reload...', False, (150, 0, 0))
                window.blit(reload, (260, 460))

            else:
                num_fire = 0
                reload_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        
        for i in collides:
                score = score + 1

                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= max_lost:
                finish = True
                window.blit(kalah, (200, 200))

        if score >= goals:
            finish = True
            window.blit(menang, (1 ,0, 200))       

        display.update()
    else:
        # reset ke awal
        finish = False
        score = 0
        lose = 0
        life = 3 # nyawa
        reload_time = False 
        num_fire = 0
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        for i in asteroids:
            i.kill()
        time.delay(3000)
        for i in range (1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy("asteroid.png", randint(80, win_width - 80), -40, 70, 60, randint(1, 5))
            asteroids.add(asteroid)

    time.delay(50)