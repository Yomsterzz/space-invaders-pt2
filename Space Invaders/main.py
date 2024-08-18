import pygame
import pygame.locals
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0
YELLOW = 255,255,0
border = pygame.Rect((WIDTH//2,0), 10, HEIGHT)

health_font = pygame.font.SysFont("comicsans", 45)
winner_font = pygame.font.SysFont("futura", 75)

fps = 60
vel = 5
bullet_vel = 7
max_bullets = 5
player_width = 55
player_height = 40
yellow_hit = pygame.USEREVENT+1
red_hit = pygame.USEREVENT+2

enemy_red_img = pygame.image.load("./images/spaceship_red.png")
enemy_red_scale = pygame.transform.scale(enemy_red_img, (player_width, player_height))
enemy_red = pygame.transform.rotate(enemy_red_scale, 270)

enemy_yellow_img = pygame.image.load("./images/spaceship_yellow.png")
enemy_yellow_scale = pygame.transform.scale(enemy_yellow_img, (player_width, player_height))
enemy_yellow = pygame.transform.rotate(enemy_yellow_scale, 90)

bg = pygame.image.load("./images/spacebg.png")
bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))

def draw_screen(red,yellow,red_bullet,yellow_bullet,red_health,yellow_health,bg):
    screen.blit(bg_scaled, (0,0))
    pygame.draw.rect(screen, WHITE, border)
    red_health_text = health_font.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = health_font.render("Health: " + str(yellow_health), 1, WHITE)
    screen.blit(red_health_text, (WIDTH-red_health_text.get_width()-10, 20))
    screen.blit(yellow_health_text, (10, 20))
    screen.blit(enemy_yellow, (yellow.x,yellow.y))
    screen.blit(enemy_red, (red.x, red.y))

    for bullet in red_bullet:
        pygame.draw.rect(screen, RED, bullet)
    
    for bullet in yellow_bullet:
        pygame.draw.rect(screen, YELLOW, bullet)
    
def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0:
        yellow.x -=  vel
    elif keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < border.x:
        yellow.x += vel
    elif keys_pressed[pygame.K_w] and yellow.y - vel > 0:
        yellow.y -=  vel
    elif keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height < HEIGHT - 15:
        yellow.y += vel
    
def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - vel > border.x + border.width:
        red.x -=  vel
    elif keys_pressed[pygame.K_RIGHT] and red.x + vel + red.width < WIDTH:
        red.x += vel
    elif keys_pressed[pygame.K_UP] and red.y - vel > 0:
        red.y -=  vel
    elif keys_pressed[pygame.K_DOWN] and red.y + vel + red.height < HEIGHT - 15:
        red.y += vel

def handle_bullets(yellow_bullets, yellow, red_bullets, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(red_hit))
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(yellow_hit))
        elif bullet.x < 0:
            red_bullets.remove(bullet)

