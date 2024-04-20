import pygame
import random
import math
import time

import RPi.GPIO as GPIO

pygame.init()


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robin In Space")

#images
title_page = pygame.image.load("title_page.bmp").convert()
tutorial_page = pygame.image.load("tutorial_page.bmp").convert()
background = pygame.image.load("custom_space_background.bmp").convert()

robin_spaceship = pygame.image.load("robin_spaceship.bmp").convert()
small_enemy_ship = pygame.image.load("small_enemy_ship.bmp").convert()
#boss_enemy = pygame.image.load("boss_enemy.png")

game_over_screen_pic = pygame.image.load("game_over_screen.bmp")

planet_1 = pygame.image.load("planet1.bmp").convert()
planet_2 = pygame.image.load("planet2.bmp").convert()
planet_3 = pygame.image.load("planet3.bmp").convert()
planet_4 = pygame.image.load("planet4.bmp").convert()
planet_5 = pygame.image.load("planet5.bmp").convert()
planet_6 = pygame.image.load("planet6.bmp").convert()
#sun = pygame.image.load("sun.bmp").convert()

asteroid_1 = pygame.image.load("asteroid_1.bmp").convert()
asteroid_2 = pygame.image.load("asteroid_2.bmp").convert()
asteroid_3 = pygame.image.load("asteroid_3.bmp").convert()

fast_asteroid = pygame.image.load("flying_asteroid.bmp").convert()

fuel = pygame.image.load("fuel.bmp").convert()
health_kit = pygame.image.load("health_kit.bmp").convert()
#bullet_pack = pygame.image.load("bullet_pack.png")

bullet = pygame.image.load("bullet_shot.bmp").convert()
#enemy_bullet = pygame.image.load("enemy_bullet.png")

play_button_pic = pygame.image.load("play_button.bmp").convert()
start_button_pic = pygame.image.load("start_button.bmp").convert()
try_again_button_pic = pygame.image.load("try_again_button.bmp").convert()
quit_button_pic = pygame.image.load("quit.bmp").convert()


robin_spaceship.set_colorkey((0, 0, 0))
small_enemy_ship.set_colorkey((0,0,0))
#game_over_screen_pic.set_colorkey((0,0,0))

planet_1.set_colorkey((255,255,255))
planet_2.set_colorkey((255,255,255))
planet_3.set_colorkey((255,255,255))
planet_4.set_colorkey((255,255,255))
planet_5.set_colorkey((255,255,255))
planet_6.set_colorkey((255,255,255))

asteroid_1.set_colorkey((0,0,0))
asteroid_2.set_colorkey((0,0,0))
asteroid_3.set_colorkey((0,0,0))
fast_asteroid.set_colorkey((0,0,0))

bullet.set_colorkey((0,0,0))

fuel.set_colorkey((0,0,0))
health_kit.set_colorkey((0,00,0))

red_button = 11
blue_button = 13
green_button = 15
yellow_button = 19
black_button = 21

def setup():
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
  
    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set buttonPin to PULL UP
    GPIO.setup(blue_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(black_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)




def destroy():

    GPIO.cleanup() # Release GPIO resource

#game variables
clock = pygame.time.Clock()



score = 0

asteroid_list = [asteroid_2]
background_planets = [planet_1, planet_2, planet_3,planet_4, planet_5, planet_6]

bg_width = background.get_width()
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
scroll = 0
text_font = pygame.font.SysFont("Comic Sans", 60)

game_over = False




def displayed_text(text, font, text_col, x, y):

    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))



def scrolling_background():

    global scroll

    #scrolling background
    for i in range (0, tiles):

        screen.blit(background,(i * bg_width + scroll, 0))

    scroll -= 4

    #reset scroll
    if abs(scroll) > bg_width:

        scroll = 0


#planets that scroll in the background. Purely aesthetic
class Scrolling_planets(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(background_planets)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):

       screen.blit(self.image, self.rect)

    def update(self):

       self.rect.x -= 2

       if self.rect.right < 0:

           self.kill()


class Button():
    
    def __init__ (self, x, y, image):

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        #get mouse positions
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


#gas tank class
class Gas:

    def __init__ (self, x, y, width, height, max_gas):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gas = 300
        self.max_gas = max_gas


    def draw(self, surface):
        
        ratio = self.gas / self.max_gas
        
        pygame.draw.rect(surface, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.width * ratio, self.height))


class Health_bar:

    def __init__(self, x, y, width, height, max_health):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = 300
        self.max_health = max_health

    def draw(self, surface):
        
        ratio = self.hp / self.max_health
        
        pygame.draw.rect(surface, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.width * ratio, self.height))




class Asteroids(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(asteroid_list)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self):

       screen.blit(self.image, self.rect)

    def update(self):

       self.rect.x -= random.randint(5,15)

       if self.rect.colliderect(robin):

           spaceship_health.hp -= 30
           spaceship_health.draw(screen)
           self.kill()

       if self.rect.right < 0:

           self.kill()


class Flying_asteroid(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = fast_asteroid
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self):

       screen.blit(self.image, self.rect)

    def update(self):

       self.rect.x -= random.randint(10,15)

       if self.rect.colliderect(robin):

           spaceship_health.hp -= 100
           spaceship_health.draw(screen)
           self.kill()

        


       if self.rect.right < 0:

           self.kill()



class Fuel(pygame.sprite.Sprite):

    def __init__ (self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = fuel
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):

        screen.blit(self.image, self.rect)

    def update(self):

        self.rect.x -= 3

        if self.rect.right < 0:

            self.kill()


        if self.rect.colliderect(robin):

            gas_tank.gas += 100
            self.kill()

            if gas_tank.gas > 300:
                gas_tank.gas = 300


class Health_kit(pygame.sprite.Sprite):

    def __init__ (self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = health_kit
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):

        screen.blit(self.image, self.rect)

    def update(self):

        self.rect.x -= 3

        if self.rect.right < 0:

            self.kill()

        if self.rect.colliderect(robin):

            spaceship_health.hp += 100
            self.kill()

            if spaceship_health.hp > 300:
                spaceship_health.hp = 300


class Small_enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(small_enemy_ship,(250,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self):
        
        screen.blit(self.image, self.rect)

    def update(self):

        self.rect.x -= 15

        if self.rect.right < 0:

            self.kill()

        if self.rect.colliderect(robin):

            spaceship_health.hp -=100
            self.kill()



class Player_bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.on_screen = False


    def draw(self):

        screen.blit(self.image, self.rect)
        
    
    def update(self):

        self.rect.x += 12
        self.on_screen = True

        if self.rect.left > 1600:

            self.kill()
            self.on_screen = False
      


class Player:


    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
  
    GPIO.setup(red_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(blue_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(green_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(yellow_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __init__(self, x, y):
  
        self.image = pygame.transform.scale(robin_spaceship,(250, 200))
        self.rect = self.image.get_rect()



        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        
        self.width = 100
        self.height = 100
		
    def draw(self):

        screen.blit(self.image, self.rect)

    def move(self):

        scroll = 0
        dx = 0
        dy = 0

        #movement
        key = pygame.key.get_pressed()

        red_button = 11

        #right

        if GPIO.input(yellow_button)==GPIO.LOW:

            dx += 10

        #left
        if GPIO.input(green_button)==GPIO.LOW:

            dx -= 10

        #Down
        if GPIO.input(blue_button)==GPIO.LOW:

            dy += 5

        #up
        if GPIO.input(red_button)==GPIO.LOW:

            dy -=5

        #bounderies

        if self.rect.x < 0:

            self.rect.x = 0

        if self.rect.x > 1200:

            self.rect.x = 1200


        if self.rect.y < 0:

            self.rect.y = 0

        if self.rect.y > 550:
            self.rect.y = 550

        self.rect.x += dx       
        self.rect.y += dy


#health and gass instances
spaceship_health = Health_bar(900,750,180,80,300)
gas_tank = Gas(300,750,180,80,300)

#gas depletion
gas_depletion = pygame.USEREVENT + 0
pygame.time.set_timer(gas_depletion, 2500)

#player instance
robin = Player(400,400)

#asteroid instance
asteroid_group = pygame.sprite.Group()
space_rocks = Asteroids(1600,random.randint(0,600))
asteroid_group.add(space_rocks)

#spawn random asteroid
asteroid_spawner = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_spawner, random.randint(500,1000))

#spawn fast random asteroid
fast_asteroid_spawner = pygame.USEREVENT + 2
pygame.time.set_timer(fast_asteroid_spawner, random.randint(10000,30000))

#fast random asteroid instance
fast_asteroid_group = pygame.sprite.Group()
fast_space_rock = Flying_asteroid(1600,random.randint(0,600))
fast_asteroid_group.add(fast_space_rock)

#button instances
start_button = Button(550,550, start_button_pic)
play_button = Button(1000,600, play_button_pic)
try_again_button = Button(500,500, try_again_button_pic)
quit_button = Button(800,500, quit_button_pic)

#fuel instance
fuel_tank_group = pygame.sprite.Group()
fuel_tank = Fuel(1600,random.randint(0,650))
fuel_tank_group.add(fuel_tank)

#spawn fuel tanks
fuel_tank_spawner = pygame.USEREVENT + 3
pygame.time.set_timer(fuel_tank_spawner,  15000)

#health kit instance
health_kit_group = pygame.sprite.Group()
health_kit_box = Health_kit(1600,random.randint(0,700))
health_kit_group.add(health_kit_box)

#spawn health kits
health_kit_spawner = pygame.USEREVENT + 4
pygame.time.set_timer(health_kit_spawner, random.randint(10000, 15000))

#scrolling planets instance
scrolling_planets_group = pygame.sprite.Group()
planets = Scrolling_planets(1600, random.randint(0,700))
scrolling_planets_group.add(planets)

#scrolling planets spawner
scrolling_planets_spawner = pygame.USEREVENT + 5
pygame.time.set_timer(scrolling_planets_spawner, 25000)

#small enemy ship spawner
scrolling_enemy_spawner = pygame.USEREVENT + 6
pygame.time.set_timer(scrolling_enemy_spawner, 10000)

#small enemy ship instance
small_enemy_group = pygame.sprite.Group()
tiny_spaceship = Small_enemy(1600,0)
small_enemy_group.add(tiny_spaceship)

#player bullet instance
player_bullet_group = pygame.sprite.Group()
bullets_shot = Player_bullet(robin.rect.x, robin.rect.x)
player_bullet_group.add(bullets_shot)

#start menu
def start_menu():


    GPIO.setup(black_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 


    run = True

    while run:

        screen.blit(title_page,(0,0))
        if start_button.draw() == GPIO.input(black_button)==GPIO.LOW:

            tutorial()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    

    pygame.quit()

def tutorial():

    GPIO.setup(black_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    run = True

    while run:


        screen.blit(tutorial_page,(0,0))

        if play_button.draw() == GPIO.input(black_button)==GPIO.LOW:

            game()
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    

    pygame.quit()


def game_over_pop_up():

    GPIO.setup(black_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    run = True

    while run:


        screen.blit(game_over_screen_pic,(350,0))
        
        if try_again_button.draw() == GPIO.input(black_button)==GPIO.LOW:

            game()



        if quit_button.draw() == True:


            pygame.quit()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    
    pygame.quit()

def game():


    GPIO.setup(black_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    global bullets_shot
    global game_over

    run = True

    #time
    clock.tick(30)
    start_time = time.time()
    elasped_time = 0
    spaceship_health.hp = 300
    gas_tank.gas = 300
    
    game_over = False      

    while run:


        while game_over == False:

            score = 0
        
            scrolling_background()

            elasped_time = round(time.time() - start_time)

            for space_rocks in asteroid_group:


                if pygame.sprite.groupcollide(player_bullet_group, asteroid_group, True, True, collided = None):

                    bullets_shot.on_screen = False

            if GPIO.input(black_button)==GPIO.LOW and bullets_shot.on_screen == False:

                bullets_shot = Player_bullet(robin.rect.x + 200, robin.rect.y + 80)
                player_bullet_group.add(bullets_shot)



            for event in pygame.event.get():

                if event.type == gas_depletion:

                    gas_tank.gas -= 20
                    gas_tank.draw(screen)

                if event.type == asteroid_spawner:
                
                    space_rocks = Asteroids(1600,random.randint(0,600))
                    asteroid_group.add(space_rocks)


                            
                if event.type == fast_asteroid_spawner:

                    fast_space_rock = Flying_asteroid(1600,random.randint(0,600))
                    fast_asteroid_group.add(fast_space_rock)
                
                if event.type == fuel_tank_spawner:

                    fuel_tank = Fuel(1600,random.randint(0,800))
                    fuel_tank_group.add(fuel_tank)

                if event.type == health_kit_spawner:
                
                    health_kit_box = Health_kit(1600,random.randint(0,200))
                    health_kit_group.add(health_kit_box)           
                
                if event.type == scrolling_planets_spawner:

                    planets = Scrolling_planets(1600, random.randint(0,800))
                    scrolling_planets_group.add(planets)

                if event.type == scrolling_enemy_spawner:

                    tiny_spaceship = Small_enemy(1600,0)
                    small_enemy_group.add(tiny_spaceship)


                if event.type == pygame.QUIT:
                    run = False



            scrolling_planets_group.draw(screen)
            scrolling_planets_group.update()

            fuel_tank_group.draw(screen)
            fuel_tank_group.update()

            player_bullet_group.draw(screen)
            player_bullet_group.update()

            robin.draw()
            robin.move()

            gas_tank.draw(screen)

            spaceship_health.draw(screen)

            asteroid_group.draw(screen)
            asteroid_group.update()

            fast_asteroid_group.draw(screen)
            fast_asteroid_group.update()

            health_kit_group.draw(screen)
            health_kit_group.update()

            small_enemy_group.draw(screen)
            small_enemy_group.update()

        
            displayed_text("Time: {} ".format(elasped_time), text_font, "white", 0,0)
            displayed_text("Gas", text_font, "white", 50, 740)
            displayed_text("Health", text_font, "white", 600, 740)

            if spaceship_health.hp <= 0:

                game_over = True
                game_over_pop_up()


            setup()
            #try:
                #loop()
            #except KeyboardInterrupt: # Press ctrl-c to end the program.
                #destroy()   


            pygame.display.update()
    

    pygame.quit()


run = True

while run:


    start_menu()
    clock.tick(60)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()
    

pygame.quit()

