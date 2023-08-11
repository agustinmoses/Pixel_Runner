import pygame
import sys
from random import randint, choice

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0
        self.player_walk = [player_walk1,player_walk2]

        self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3')
    def player_input(self):

        """"
        This checks for the space bar input and redefines the 
        self.gravity var accordingly
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        elif keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        elif keys[pygame.K_w] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()            
    
    def apply_gravity(self):
        """
        This is the logic for the player gravity
        """
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animate(self):
        """
        This animates the player between multiple frames
        """
        if self.rect.bottom < 300:

            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): 
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        """
        This method is used in the game loop to continously
        update the sprite on the screen
        """
        self.player_input()
        self.apply_gravity()
        self.animate()

class Enemies(pygame.sprite.Sprite):
    
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame1 = pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('Graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 100
        else:
            snail_frame1 = pygame.image.load('Graphics/Snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('Graphics/Snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1,snail_frame2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animate(self):
        """
        Takes care of the animation of the fly and snail
        """
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        """
        This is to simply make sure a sprite is deleted once it is
        offscreen.
        """
        if self.rect.x <= -100:
            self.kill() 
    
    def update(self):
        """
        Called in the game loop to continously update sprite
        between frames
        """
        self.animate()
        self.rect.x -=5
        self.destroy()

def display_score():
    """
    This tracks the time the player has spent in one game as well as displaying
    it on screen. This is called at the second state of the screen.
    """
    current_time = pygame.time.get_ticks() - start_time
    score_surface = text_font.render(f'Time: {current_time//1000}', False, (64,64,64))
    score_rec = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rec)
    return current_time//1000

def collision_sprite():
    """
    This take cares of the collision logic of the sprites. Specifically
    it take cares if the player sprite collides with any sprite in the 
    enemy group
    """
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    return True

### Initializes pygame
pygame.init()
screen = pygame.display.set_mode((800,400))

pygame.display.set_caption("Ninja Runner")
clock = pygame.time.Clock()
text_font = pygame.font.Font("Font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('Audio/music.wav')
bg_music.play(loops = - 1)

### Groups

## Player Group
player = pygame.sprite.GroupSingle()
player.add(Player())
## Enemie Group
obstacle_group = pygame.sprite.Group()

### Backgrounds
sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()


### Intro screen
player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rec = player_stand.get_rect(center = (390, 200))

title_surface = text_font.render('Pixel Runner', False, (64,64,64))
title_rec = title_surface.get_rect(center = (400, 80))

instr_surface = text_font.render('Press space to begin', False, (64,64,64))
instr_rec = instr_surface.get_rect(center = (400, 325))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
             if event.type == obstacle_timer:
                obstacle_group.add(Enemies(choice(['fly','snail','snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        
        ### Player
        player.draw(screen)
        player.update()
        ### Enemies
        obstacle_group.draw(screen)
        obstacle_group.update()
        ### Gives bool to let me know if there is a collision
        game_active = collision_sprite()
    else:
        screen.fill((94,129,162)) 
        screen.blit(player_stand, player_stand_rec)
        screen.blit(title_surface, title_rec)
        player_grav = 0
        
        #Score messaging
        score_message = text_font.render(f'Your score: {score}', False, (64,64,64))
        score_message_rect = score_message.get_rect(center = (400,325))
        if score == 0:
            screen.blit(instr_surface, instr_rec)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    # F.P.S
    clock.tick(60)