import pygame
import sys
from random import randint

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = text_font.render(f'Time: {current_time//1000}', False, (64,64,64))
    score_rec = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rec)
    return current_time//1000

def obstacle_movement(obstacle_list):
    """
    Manages the movement of the obstacles in the game by cheking
    each rectangle in the obstacle_list and changing its x-pos by 
    certain number

    Inputs:
        obstacle_list[list[Rectangle]]: A list of rectangles that are
        the obstacles in the game
    Returns [list[Rectangle]]: A list of new rectangles that are still 
        on the screen
    """
    if obstacle_list:
        for rect in obstacle_list:
            rect.x -= 5
            if rect.bottom == 300:
                screen.blit(snail_surface,rect)
            else:
                screen.blit(fly_surface,rect)
        #This makes sure it only puts rectangles that are on screen in the list
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >-100]
        return obstacle_list
    else:
        return []
    
def collisions(player,obstacles):
    """
    This checks if there are collsions between the player and the
    enemies.

    Inputs:
        player[Rect]: The player rectangle
        obstacles[list[Rectangle]:The list of obstacles we are checking
    
    Returns [bool]: True if there is a collision. False otherwise.

    """
    if obstacles:
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle): 
                return False
    
    return True

def player_animation():
    """
    This takes care of the player animation. 
    """
    
    global player_surface,player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        # We want to slowly increment to the next image
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        
        player_surface = player_walk[int(player_index)]

### Initializes pygame
pygame.init()
screen = pygame.display.set_mode((800,400))

pygame.display.set_caption("Ninja Runner")
clock = pygame.time.Clock()
text_font = pygame.font.Font("Font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()

### Obstacles

## Snail
snail_frame1 = pygame.image.load('Graphics/Snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('Graphics/Snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1,snail_frame2]
snail_index = 0
# Default value for the snail surface. This changes in the event loop
snail_surface = snail_frames[snail_index]
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

## Fly
fly_frame1 = pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('Graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_index = 0
# Default value for the fly surface. This changes in the event loop
fly_surface = fly_frames[fly_index]
snail_rect = fly_surface.get_rect(midbottom = (600, 300))


obstacle_rect_list = []

### Player
player_walk1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()
player_index = 0
player_walk = [player_walk1, player_walk2]
player_jump = pygame.image.load('Graphics/Player/jump.png').convert_alpha()
# Default value for the player surface. This changes in player_animation()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (200,300))
player_grav = 0



# Intro screen
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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(pygame.mouse.get_pos()): 
                    player_grav = -20
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE) and (player_rect.bottom == 300):
                    player_grav = -20
        else:
            if event.type == pygame.KEYDOWN:
                game_active = True
                start_time = pygame.time.get_ticks()
        
        if game_active:
            ## This controls how often enemies spawn in
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900,1100), 100)))
            ## This controls how often the image of the snail changes frames
            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surface = snail_frames[snail_index]
            ## This controls how often the image of the fly changes frames          
            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surface = fly_frames[fly_index]



    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        
        ### Player
        player_grav += 1
        player_rect.y += player_grav
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        # The player_surface variable is updated by player_animation
        screen.blit(player_surface,player_rect) 
        
        ### Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        ### Collisions

        # The game_active vairable is redifined with collisions()
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,162)) 
        screen.blit(player_stand, player_stand_rec)
        screen.blit(title_surface, title_rec)
        obstacle_rect_list.clear()
        player_rect.midbottom = (200,300)
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