import math
import random
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background.png')

mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Star Wars")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0
best_score = 0  # Variable to store the best score
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

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_best_score(x, y):
    best_score_text = font.render("Best Score : " + str(best_score), True, (255, 255, 255))
    screen.blit(best_score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    
    # Display best score at the bottom of the screen
    show_best_score(250, 350)

def level_text():
    level_msg = font.render(f"Level {level}", True, (255, 255, 255))
    screen.blit(level_msg, (650, 10))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def main_menu():
    screen.fill((0, 0, 0))
    
    title = menu_font.render("The Beka Wars Game", True, (255, 255, 255))
    start_button = menu_font.render("Start Game", True, (255, 255, 255))
    quit_button = menu_font.render("Quit", True, (255, 255, 255))
    
    title_x = (800 - title.get_width()) // 2
    start_button_x = (800 - start_button.get_width()) // 2
    quit_button_x = (800 - quit_button.get_width()) // 2
    title_y = 150
    start_button_y = 250
    quit_button_y = 350

    screen.blit(title, (title_x, title_y))
    screen.blit(start_button, (start_button_x, start_button_y))
    screen.blit(quit_button, (quit_button_x, quit_button_y))
    
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

def restart_game():
    global score_value, level, num_of_enemies, best_score
    score_value = 0
    level = 1
    num_of_enemies = 6
    initialize_enemies()
    start_ticks = pygame.time.get_ticks()
    best_score = max(best_score, score_value) 

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
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

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
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)
        level_text()
        show_timer()

        if score_value >= level * 10:
            level += 1
            num_of_enemies += 2
            initialize_enemies()
            show_level_up_text()

            start_ticks = pygame.time.get_ticks()

            for i in range(num_of_enemies):
                enemyX_change[i] += 1

        if pygame.time.get_ticks() - start_ticks >= max_time:
            game_over_text()
            restart_button = menu_font.render("Restart Game", True, (255, 255, 255))
            restart_button_x = (800 - restart_button.get_width()) // 2
            restart_button_y = 450
            screen.blit(restart_button, (restart_button_x, restart_button_y))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if restart_button_x <= mouseX <= restart_button_x + restart_button.get_width() and restart_button_y <= mouseY <= restart_button_y + restart_button.get_height():
                        restart_game()
                        in_game = False
                        break

        clock.tick(60)

        pygame.display.update()

pygame.quit()
