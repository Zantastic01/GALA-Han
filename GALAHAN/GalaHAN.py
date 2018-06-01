
# Imports
import pygame
import random 
import xbox360_controller

# Initialize game engine
pygame.init()



# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "GALA-HAN"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Controller
my_controller = xbox360_controller.Controller(0)

# Stages
START = 0
PLAYING = 1
WIN = 2
LOSE = 3
BEAT = 4

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
GREEN = (0, 150, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 200)
BLUE = (75, 200, 255)
GREY = (110, 112, 117)
GREYbLUE = (177, 185, 206)
RED = (237, 40, 40)
star_colors = [YELLOW, BLUE, RED, WHITE]

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacebar/SPACEBAR.ttf", 96)
SCORE = pygame.font.Font("assets/fonts/spacebar/SPACEBAR.ttf", 75)
ENDSCORE = pygame.font.Font("assets/fonts/spacebar/SPACEBAR.ttf", 75)

# Images
Ship_img = pygame.image.load('assets/images/help.png')
mob_img = pygame.image.load('assets/images/bad.png')
laser_img = pygame.image.load('assets/images/laser1.png')
bomb_img = pygame.image.load('assets/images/laser.png')
ai_img = pygame.image.load('assets/images/help.png')
icon_img = pygame.image.load('assets/images/icon.png')
mob_img2 = pygame.image.load('assets/images/bad3.png')
mob_img3 = pygame.image.load('assets/images/bad4.png')
# sounds
laser_sound = pygame.mixer.Sound('assets/sounds/laser.ogg')
pygame.mixer.music.load('assets/sounds/background.ogg')
explosion = pygame.mixer.Sound('assets/sounds/Explosion.ogg')

# Make stars #
stars = []
for i in range(200):
    x = random.randrange(800, 1600)
    y = random.randrange(-100, 800)
    r = random.randrange(1, 5)
    s = [x, y, r, r]
    stars.append(s)

     

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.shield = 10
        shiphealth = self.shield
        
        self.shot_timer = 0

    def move(self, stick_x):
        self.rect.x += self.speed * stick_x

    def shoot(self):
        if self.shot_timer <= 0:
            laser = Laser(laser_img)
            laser.rect.centerx = self.rect.centerx
            laser.rect.centery = self.rect.top
            lasers.add(laser)
            laser_sound.play()
            self.shot_timer = 30
        
    def update(self, bombs, all_mobs):
    
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            # play hit sound
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, all_mobs, False, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield = 0
        
        if self.shield <= 0:
            self.kill()
            stage = LOSE
                
        self.shot_timer -= 1
        
        #Check The Edges
        if self.rect.right > WIDTH:
            self.rect.right =  WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

class Laser(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 2

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
            
            
class Mob(pygame.sprite.Sprite):

    def __init__(self, x, y, image, shield):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = shield 

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        
    def update(self, lasers):
        hit_list2 = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        for hit in hit_list2:
            if len(hit_list2) > 0:
                self.shield -= 1
                player.score += 150

            if self.shield <= 0:
                explosion.play()
                self.kill()
                player.score += 150
            
class Bomb(pygame.sprite.Sprite):

    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
    
    

class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 120

        
    def move(self):
      
        reverse = False
        
        for m in self.mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True


        if reverse == True:
            self.moving_right = not self.moving_right
            for m in self.mobs:
                m.rect.y += 32


    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

    


# Draw Box
location = (0, 0, 202, 77)
pygame.draw.rect(screen, WHITE, location)
location = (1, 1, 200, 75)
pygame.draw.rect(screen, BLACK, location)
location = (202, 0, 50, 38)
pygame.draw.rect(screen, WHITE, location)
location = (200, 1, 50, 36)
pygame.draw.rect(screen, BLACK, location)


# set stage
stage = START

# Game helper functions
def setup():
    global player,ship, mobs, mobs2 , bombs, lasers, fleet1, fleet2, all_mobs, stage, high_score

    player = pygame.sprite.GroupSingle()
    
    # set level
    player.level = 1

    # sprite groups
    mobs = pygame.sprite.Group()
    mobs2 = pygame.sprite.Group()
    
    # Make game objects
    ship = Ship(384, 536, Ship_img)
    mob1 = Mob(128, 55, mob_img,player.level)
    mob2 = Mob(256, 55, mob_img,player.level)
    mob3 = Mob(384, 55, mob_img,player.level)
    mob4 = Mob(512, 55, mob_img,player.level)
    mob5 = Mob(128, 128, mob_img2,player.level)
    mob6 = Mob(256, 128, mob_img2,player.level)
    mob7 = Mob(384, 128, mob_img2,player.level)
    mob8 = Mob(512, 128, mob_img2,player.level)
    mob9 = Mob(128, 192, mob_img3,player.level)
    mob10 = Mob(256, 192, mob_img3,player.level)
    mob11 = Mob(384, 192, mob_img3,player.level)
    mob12 = Mob(512, 192, mob_img3,player.level)

    with open('high_score.txt') as high_score_file:
        high_score = int(high_score_file.read())
    
    player.add(ship)
    player.score = 0


    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob9, mob10, mob11, mob12)

    mobs2 = pygame.sprite.Group()
    mobs2.add(mob5, mob6, mob7, mob8)

    bombs = pygame.sprite.Group()

    all_mobs = pygame.sprite.Group()
    all_mobs.add(mobs, mobs2)

    fleet1 = Fleet(mobs)
    fleet2 = Fleet(mobs2)
    fleet2.moving_right = False

    

    # set stage
    stage = START

def level_change():
    global player,ship, mobs, mobs2 , bombs, lasers, fleet1, fleet2, all_mobs, stage

    # sprite groups
    mobs = pygame.sprite.Group()
    mobs2 = pygame.sprite.Group()

    # Make game objects
    
    mob1 = Mob(128, 55, mob_img,player.level)
    mob2 = Mob(256, 55, mob_img,player.level)
    mob3 = Mob(384, 55, mob_img,player.level)
    mob4 = Mob(512, 55, mob_img,player.level)
    mob5 = Mob(128, 128, mob_img2,player.level)
    mob6 = Mob(256, 128, mob_img2,player.level)
    mob7 = Mob(384, 128, mob_img2,player.level)
    mob8 = Mob(512, 128, mob_img2,player.level)
    mob9 = Mob(128, 192, mob_img3,player.level)
    mob10 = Mob(256, 192, mob_img3,player.level)
    mob11 = Mob(384, 192, mob_img3,player.level)
    mob12 = Mob(512, 192, mob_img3,player.level)

    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob9, mob10, mob11, mob12)

    mobs2 = pygame.sprite.Group()
    mobs2.add(mob5, mob6, mob7, mob8)

    bombs = pygame.sprite.Group()

    all_mobs = pygame.sprite.Group()
    all_mobs.add(mobs, mobs2)

    fleet1 = Fleet(mobs)
    fleet2 = Fleet(mobs2)
    fleet2.moving_right = False

    stage = PLAYING
    
    
def show_title_screen():
    title_text = FONT_XL.render("GALA-HAN", 1, WHITE)
    screen.blit(title_text, [100, 200])
    restart = ENDSCORE.render("     Press Start ", 1, RED)
    
    
    text_rect = restart.get_rect(center=(WIDTH/4 + 100, HEIGHT/4 + 275))
    screen.blit(restart, text_rect)

def show_end_screen1():
    title_text = FONT_XL.render("YOU WIN" , 1, WHITE)
    screen.blit(title_text, [86, 92])

def show_end_screen2():
    title_text = FONT_XL.render("YOU Lose", 1, WHITE)
    screen.blit(title_text, [86, 92])
            
def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])

    my_ship = player.sprite.rect
    
    barX= my_ship.left
    barY = my_ship.bottom + 16
    barW= my_ship.width
    barH = 16

    percent = ship.shield / 10
    health_width = int(barW * percent)
    
    pygame.draw.rect(screen, WHITE, [barX, barY, barW, barH])
    pygame.draw.rect(screen, BLUE, [barX, barY, health_width, barH])

    high_score_text = FONT_MD.render("High Score: " + str(high_score), 1, WHITE)
    screen.blit(high_score_text, [32, 64])

    level_text = FONT_MD.render("LEVEL: " + str(player.level), 1, WHITE)
    screen.blit(level_text, [32, 96])

# Game loop
setup()
pygame.mixer.music.play(-1)
done = False
triggers = my_controller.get_triggers()
left_x_ = my_controller.get_left_stick()
right_x_ = my_controller.get_right_stick()

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.JOYBUTTONDOWN:
            if stage == START:
                if event.button == xbox360_controller.START:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.button == xbox360_controller.A:
                    ship.shoot()
            elif stage == LOSE:
                if event.button == xbox360_controller.BACK:
                    setup()
                    
    if stage == PLAYING:
        left_x, _  = my_controller.get_left_stick()
        ship.move(left_x)
        
        # Game logic (Check for collisions, update points, etc.)
        for s in stars: 
                    s[1] += 3
                    
                    if s[1] > 1000:
                       s[0] = random.randrange(0, 1000)
                       s[1] = random.randrange(-100, 0)

        ship.update(bombs, all_mobs)
        lasers.update()   
        mobs.update(lasers)
        bombs.update()
        fleet1.update()
        fleet2.update()
        mobs2.update(lasers)

        for s in stars: 
                s[1] += 3
                    
                if s[1] > 1000:
                    s[0] = random.randrange(0, 1000)
                    s[1] = random.randrange(-100, 0)

    

        if len(all_mobs)== 0:
            player.level += 1
            stage = BEAT
            level_change()
            
        elif len(player)== 0:
            stage = LOSE
                   
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == PLAYING:
        screen.fill(BLACK)
        for s in stars:
            color = random.choice(star_colors)
            pygame.draw.ellipse(screen, color, s)

        lasers.draw(screen)
        player.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)
        show_stats(player)
        mobs2.draw(screen)

    
    if stage == START:
        show_title_screen()

    if stage == WIN:
        show_end_screen1()

    if stage == LOSE:
        show_end_screen2()
        if player.score > high_score:
            writehighscore = open("high_score.txt", "w")
            writehighscore.write(str(player.score))

    for s in stars:
            color = random.choice(star_colors)
            pygame.draw.ellipse(screen, color, s)

    
    
            
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()

