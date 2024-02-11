import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import random

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 500
WIDTH = 900
# player_size = (100, 100)

FONT = pygame.font.SysFont('Roboto', 36)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GOLD = (225, 199, 33)
COLOR_RED = (231, 9, 9)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
# player = pygame.Surface(player_size)
player = pygame.image.load('ufo_.png').convert_alpha()
# player.fill(COLOR_WHITE)
player_rect = player.get_rect()
# player_speed = [1, 1]
player_move_down = [0, 1]
player_move_up = [0, -1]
player_move_right = [1, 0]
player_move_left = [-1, 0]

bg = pygame.transform.scale(pygame.image.load('space.jpg'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 0.1

def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load('alien.png').convert_alpha()
    # enemy = pygame.Surface(enemy_size)
    # enemy.fill(COLOR_BLUE)
    enemy_rect = enemy.get_rect()
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_move = [random.randint(-1, -1), 0]
    return [enemy, enemy_rect, enemy_move]


def make_bonus():
    bonus_size = (50, 50)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    # bonus = pygame.Surface(bonus_size)
    # bonus.fill(COLOR_GOLD)
    bonus_rect = bonus.get_rect()
    # bonus_rect = pygame.Rect(0, random.randint(0, WIDTH), *bonus.get_size())
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus.get_size())
    bonus_move = [0, random.randint(1, 1)]
    return [bonus, bonus_rect, bonus_move]

CREAT_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREAT_ENEMY, 2500)
enemies = []

MAKE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(MAKE_BONUS, 3000)
bonuses = []

score = 0

playing = True
FPS.tick(120)
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            
        elif event.type == CREAT_ENEMY:
            enemies.append(create_enemy())
            
        elif event.type == MAKE_BONUS:
            bonuses.append(make_bonus())
        
    # main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    bg_X2 -= bg_move
    
    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
        
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()
        
    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    
    elif keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
        
    elif keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
        
    elif keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)
        
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        
        if player_rect.colliderect(enemy[1]):
            playing = False
            enemies.pop(enemies.index(enemy))
        
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        
        if player_rect.colliderect(bonus[1]):
            score+=1
            bonuses.pop(bonuses.index(bonus))
        
    # enemy_rect = enemy_rect.move(create_enemy())
        
    # if player_rect.bottom >= HEIGHT:
    #     player_speed=random.choice(([1, -1], [-1, -1]))
        
    # if player_rect.right >= WIDTH:
    #     player_speed=random.choice(([-1, -1], [-1, 1]))

    # if player_rect.top <= 0:
    #     player_speed=random.choice(([-1, 1], [1, 1]))
        
    # if player_rect.left <= 0:
    #     player_speed=random.choice(([1, 1], [1, -1]))
    main_display.blit(FONT.render(str(score), True, COLOR_RED), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    # main_display.blit(enemy, enemy_rect)
    pygame.display.flip()
    # player_rect = player_rect.move(player_speed)
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
        