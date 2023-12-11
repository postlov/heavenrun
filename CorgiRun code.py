
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 900
FPS = 60

LEVEL_DURATION = 15
NUM_LEVELS = 3

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Corgi run by 20201091 송민경")
clock = pygame.time.Clock()

###images
start_img = pygame.image.load(path.join(img_dir, "start1.png")).convert()
start_img = pygame.transform.scale(start_img, (WIDTH, HEIGHT))
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background2 = pygame.image.load(path.join(img_dir, "background_lighter.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "corgigi.png")).convert()
player_img.set_colorkey(BLACK)
player_mini_img = pygame.transform.scale(player_img, (25, 30))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
ghosts_img = []
for gst in ["sprite_01.png", "sprite_04.png", "sprite_08.png"]:
    ghosts_img.append(pygame.image.load(path.join(img_dir, gst)).convert())

boss_img = pygame.image.load(path.join(img_dir, "reaper1.png")).convert()
boss_img = pygame.transform.scale(boss_img, (300,300))
boss_img.set_colorkey(BLACK)
end_img = pygame.image.load(path.join(img_dir, "ending3.png")).convert()


explosion_anim =[]
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim.append(img)



###sounds
bark_sounds = []
for snd in ['bark1.mp3', 'bark2.mp3']:
    bark_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'Snowfall.ogg'))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

###screen display
font_name = pygame.font.match_font('congenial black')
def draw_text(surf, text, size, x, y, color=BLACK):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)

def show_notification(message):
    draw_text(screen, message, 50, WIDTH / 2, HEIGHT / 2, BLACK)
    pygame.display.flip()
    pygame.time.delay(1500)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.blit(start_img, background_rect)
    draw_text(screen, "Corgi Run!", 64, WIDTH / 2, HEIGHT / 4 - 20, BLACK)
    draw_text(screen, "Arrow keys to move, Space to fire", 30,
              WIDTH / 2, HEIGHT / 4 + 20)
    draw_text(screen, "Press Space Bar to begin", 30, WIDTH / 2, HEIGHT / 4+50)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                return True
            
def show_game_clear_screen():
    screen.blit(end_img, background_rect)
    draw_text(screen, "Game Clear!", 100, WIDTH/2, HEIGHT/4, WHITE)
    draw_text(screen, "Corgi is happy with his friend :)", 40, WIDTH / 2, HEIGHT / 4+50, WHITE)
    draw_text(screen, f"Final Score: {score}", 43, WIDTH / 2, HEIGHT / 2, WHITE)
    #draw_text(screen, "Press Space Bar to play again", 25, WIDTH / 2, HEIGHT * 3 / 4,WHITE)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting = False

### class main objects

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(player_img, (75, 90))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.hidden = False
        self.life =3

    def update(self):

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        random.choice(bark_sounds).play()

    def hide(self):
        self.life -= 1
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self, is_boss=False):
        pygame.sprite.Sprite.__init__(self)
        if is_boss:
            self.image = pygame.transform.scale(boss_img, (460, 460))
            self.speedy = 0
        else:
            self.image = pygame.transform.scale(random.choice(ghosts_img), (70, 70))
            self.speedy = random.randrange(1, 8)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 30 if is_boss else random.randrange(WIDTH - self.rect.width)
        self.rect.y = 70 if is_boss else random.randrange(-100, -40)
        self.speedx = 0
        self.HP = 2000 if is_boss else random.randrange(5, 15) + (20 * (level-1))
        self.is_boss = is_boss
        self.hp_draw()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if not self.is_boss:
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speedx *= -1

    def killed(self):
        self.kill()
        if not self.is_boss:
            m = Mob()
            if level == 2:
                m.speedx = random.choice([-3,3])
            all_sprites.add(m)
            mobs.add(m)
        if self.is_boss:
            print("boss is killed")
            

    def hp_draw(self):
        draw_text(screen, str(self.HP), 30, self.rect.centerx, self.rect.bottom + 10 if not self.is_boss else self.rect.top - 10, BLACK if not self.is_boss else RED)

class Bullet(pygame.sprite.Sprite):
    power =1

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10,20))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.HP = Bullet.power

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

    @classmethod
    def increase_power(cls, amount):
        cls.power += amount


def reset():
    global game_over, score, level, Bullet, start_time, all_sprites, mobs, bullets, player

    game_over = False
    score, level = 0,1
    Bullet.power = 1
    start_time = pygame.time.get_ticks()
    all_sprites = pygame.sprite.Group()
    # player_sprite = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player() 
    all_sprites.add(player)

    show_go_screen()
    
    for i in range(5):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

def Bulletkillmob(mobs, bullets, score):
    hits=pygame.sprite.groupcollide(mobs, bullets, False, True)
    for mob, bullet_list in hits.items():
        for bullet in bullet_list:
            mob.HP -= bullet.HP
            score += bullet.HP
            if mob.HP<=0:
                mob.killed()
                score += 100
                Bullet.increase_power(1)
            if level ==3:
                expl = Explosion(bullet.rect.center)
                all_sprites.add(expl)           
    return score

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Game loop

def main():
    global game_over, start_time, score, level, timer_start_time

    reset()
    running = True
    timer_start_time = None

    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        if not game_over:
            all_sprites.update()
            score = Bulletkillmob(mobs, bullets, score)

            #check to see if a mob hit the player
            hits = pygame.sprite.spritecollide(player, mobs, False)
            if hits:
                player.hide()

            if player.life == 0:
                game_over = True

            # level 2
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            if elapsed_time == LEVEL_DURATION and level==1:
                level += 1
                show_notification("Level 2: PREPARE")

            if level ==2:
                if mob.rect.bottom > HEIGHT:
                    mob.killed()

            # # level 3
            if elapsed_time == LEVEL_DURATION * 2 and level==2:

                level += 1
                show_notification("Level 3: WARNING")
                for mob in mobs:
                    mob.kill()
                boss = Mob(is_boss=True)
                all_sprites.add(boss)
                mobs.add(boss)
                # print(mobs)

            if level ==3:
                print("elapsed_time", elapsed_time)
                if boss.HP <= 0 :
                    show_game_clear_screen()
                if elapsed_time == LEVEL_DURATION * 2 + 12:
                    boss.speedy = 3


            # Draw / render
            screen.fill(BLACK)
            screen.blit(background2 if level ==3 else background, background_rect)

            for mob in mobs:
                mob.hp_draw()
            for bullet in bullets:
                bullet.update()
            all_sprites.draw(screen)

            draw_text(screen, "score: " + str(score), 40, WIDTH / 2, 30, BLACK)
            draw_text(screen, "level: " + str(level), 20, 25, 15, BLACK)
            draw_lives(screen, WIDTH - 100, 5, player.life, player_mini_img)
            draw_text(screen, f"Bullet Power: {Bullet.power}", 25, WIDTH-80, 53, BLACK)
            if level == 3:
                if timer_start_time is None:
                    timer_start_time = pygame.time.get_ticks()  # Start the timer
                else:
                    elapsed_timer_time = (pygame.time.get_ticks() - timer_start_time) // 1000
                    remaining_time = max(10- elapsed_timer_time, 0)
                    print("remaining time =", remaining_time)
                    draw_text(screen, f"{remaining_time}", 50, WIDTH/2, HEIGHT/2, RED) 

            pygame.display.flip()

        else:
            game_over=True
            show_notification("GAME OVER!")
            reset()
            timer_start_time = None
            pygame.time.delay(1000)          

if __name__ == "__main__":
    main()