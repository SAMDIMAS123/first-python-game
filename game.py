import pygame
import random 
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

player_pos = [400, 500] #begin pos
player_size = 50

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

speed = 5

screen = pygame.display.set_mode( size = (WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, speed):
    if score < 20:
        speed = 10
    elif score < 40:
        speed = 20
    elif score < 60:
        speed = 30
    else:
        speed = 40
    


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0,WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], player_size, player_size))
  


def update_enemy_position(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    set_level(score, speed)
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False


while not game_over: 
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() 

        x = player_pos[0]
        y = player_pos[1]

        if event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                x -= player_size
                # prevent going out of bound
                if x < 0: 
                    x = 0
                    
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                x += player_size
                #prevent going out of bound
                if x >= WIDTH: 
                    x = WIDTH - player_size
                

            player_pos = [x,y]


    screen.fill((0,0,0))

    drop_enemies(enemy_list)
    score = update_enemy_position(enemy_list, score)

    text = f"Score = {score}"
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))


    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    
    
    draw_enemies(enemy_list)

    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    pygame.display.update()