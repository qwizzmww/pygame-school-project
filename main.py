import math
import random
import pygame
from pygame import mixer
import json
import os

pygame.init()

def load_best_score():
    try:
        with open('best_score.json', 'r') as f:
            data = json.load(f)
            return data.get('best_score', 0)
    except FileNotFoundError:
        return 0

def save_best_score(score):
    with open('best_score.json', 'w') as f:
        json.dump({'best_score': score}, f)

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')
mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

bulletImg = pygame.image.load('bullet.png')
bulletY_change = 10
bullets = []

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

max_time = 30000
start_ticks = pygame.time.get_ticks()

over_font = pygame.font.Font('freesansbold.ttf', 64)

menu_font = pygame.font.Font('freesansbold.ttf', 50)

level = 1
num_of_enemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

clock = pygame.time.Clock()

best_score = load_best_score()

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def level_text():
    level_msg = font.render(f"Level {level}", True, (255, 255, 255))
    screen.blit(level_msg, (650, 10))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def main_menu():
    screen.fill((0, 0, 0))

    mouseX, mouseY = pygame.mouse.get_pos()
    start_button_rect = pygame.Rect(300, 250, 200, 50)
    quit_button_rect = pygame.Rect(320, 350, 160, 50)
    if start_button_rect.collidepoint(mouseX, mouseY):
        start_button_color = (255, 0, 0)
    else:
        start_button_color = (255, 255, 255) 

    if quit_button_rect.collidepoint(mouseX, mouseY):
        quit_button_color = (255, 0, 0) 
    else:
        quit_button_color = (255, 255, 255)

    title = menu_font.render("NIS GAME", True, (255, 255, 255))
    start_button = menu_font.render("Start Game", True, start_button_color)
    quit_button = menu_font.render("Quit", True, quit_button_color)

    screen.blit(title, (250, 150))
    screen.blit(start_button, (300, 250))
    screen.blit(quit_button, (320, 350))

    pygame.display.update()

def show_level_up_text():
    level_up_text = font.render("Level Up!", True, (255, 255, 255))
    screen.blit(level_up_text, (300, 250))
    pygame.display.update()
    pygame.time.delay(1000)

def initialize_enemies():
    global enemyImg, enemyX, enemyY, enemyX_change, enemyY_change, num_of_enemies
    enemyImg.clear()
    enemyX.clear()
    enemyY.clear()
    enemyX_change.clear()
    enemyY_change.clear()

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

def show_timer():
    elapsed_time = pygame.time.get_ticks() - start_ticks
    remaining_time = max(0, max_time - elapsed_time)
    minutes = (remaining_time // 1000) // 60
    seconds = (remaining_time // 1000) % 60
    timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (255, 255, 255))
    screen.blit(timer_text, (10, 50))

def restart_menu():
    screen.fill((0, 0, 0))
    title = menu_font.render("Game Over", True, (255, 255, 255))
    score_text = font.render(f"Score: {score_value}", True, (255, 255, 255))
    best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
    restart_button = menu_font.render("Restart", True, (255, 255, 255))
    quit_button = menu_font.render("Quit", True, (255, 255, 255))

    screen.blit(title, (300, 150))
    screen.blit(score_text, (300, 250))
    screen.blit(best_score_text, (300, 350))
    screen.blit(restart_button, (300, 450))
    screen.blit(quit_button, (320, 550))

    pygame.display.update()

running = True
in_game = False

while running:
    if not in_game:
        main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 300 <= mouseX <= 500 and 250 <= mouseY <= 300:
                    in_game = True
                    score_value = 0
                    level = 1
                    num_of_enemies = 6
                    initialize_enemies()
                    start_ticks = pygame.time.get_ticks()
                elif 320 <= mouseX <= 480 and 350 <= mouseY <= 400:
                    running = False

    else:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if len(bullets) == 0:
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                    for i in range(3): 
                        bulletX_offset = i * 20
                        bullets.append([playerX + 16 + bulletX_offset, playerY])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                restart_menu()  
                if score_value > best_score:
                    best_score = score_value
                    save_best_score(best_score)
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            for bullet in bullets[:]:
                collision = isCollision(enemyX[i], enemyY[i], bullet[0], bullet[1])
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    bullets.remove(bullet)
                    score_value += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        for bullet in bullets[:]:
            bullet[1] -= bulletY_change
            if bullet[1] <= 0:
                bullets.remove(bullet)
            else:
                fire_bullet(bullet[0], bullet[1])

        player(playerX, playerY)
        show_score(textX, testY)
        level_text()

        show_timer()

        if score_value >= level * 30:
            level += 1
            num_of_enemies += 2
            initialize_enemies()
            show_level_up_text()

            start_ticks = pygame.time.get_ticks()

            for i in range(num_of_enemies):
                enemyX_change[i] += 1

        if pygame.time.get_ticks() - start_ticks >= max_time:
            game_over_text()
            restart_menu()  
            if score_value > best_score:
                best_score = score_value
                save_best_score(best_score)
            pygame.display.update()
            pygame.time.delay(2000)
            running = False

        clock.tick(60)

        pygame.display.update()

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouseX, mouseY = pygame.mouse.get_pos()
        if 300 <= mouseX <= 500 and 450 <= mouseY <= 500: 
            in_game = True
            score_value = 0
            level = 1
            num_of_enemies = 6
            initialize_enemies()
            start_ticks = pygame.time.get_ticks()

        elif 320 <= mouseX <= 480 and 550 <= mouseY <= 600:
            running = False

pygame.quit()
