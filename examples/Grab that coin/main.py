import time
import random
import pygame as pg
from spritesheet import spritesheet

#Expects a nim instance of len 10 and for each element x: 0 <= x <= 5
def init_rocks(nim_instance: [int]):
    def get_random_rock(rocks_spritesheet):
        row = random.randint(0,5)
        col = random.randint(0,5)
        rock_width = 16
        rock_height = 15
        img = rocks_spritesheet.image_at((row * rock_width,col * rock_height,rock_width,rock_height),colorkey=-1)
        img = pg.transform.scale(img,(32,32))
        return img
    
    rock_sp = spritesheet("assets\\rocks\\rocks.png")
    
    rock_imgs = [[]] * len(nim_instance)
    for i in range(0,len(nim_instance)):
        for j in range(nim_instance[i]):
            rock_imgs[i].append(get_random_rock(rock_sp))
    
    return rock_imgs    

def init_background(screen_width,screen_height):
    # Get the path of a background image.
    def get_random_background():
        background_img_path = "assets\\backgrounds\\bg" + str(random.randint(1,10)) + ".png"
        return background_img_path
    
    # Load a background from an image
    background_img = pg.image.load(get_random_background()).convert()
    
    # Scale the background image to fit the whole screen
    background_img = pg.transform.scale(background_img,(screen_width,screen_height))
    
    return background_img
    
def init_cursor():
    cursor_img = pg.image.load("assets\\cursor\\hand.png").convert()
    cursor_img = pg.transform.rotate(cursor_img,90)
    return cursor_img

def init_sounds():
    main = "assets\\audio\\main.mp3"
    win = "assets\\audio\\win.mp3"
    lose = "assets\\audio\\lose.mp3"
    return main,win,lose
def play_sound(sound):
    pg.mixer.music.load(sound)
    pg.mixer.music.play()


def make_enemy_move(nim_instance: [int]):
    for i in range(len(nim_instance)):
        if nim_instance[i] > 0:
            nim_instance[i] = nim_instance[i] - 1
            break
    return nim_instance

def generate_random_nim_instance(size = 10):
    nim = [0] * size
    for i in range(size):
        nim[i] = random.randint(1,9)
    return nim

nim = generate_random_nim_instance()

# Init pygame library
pg.init()

# Set window size
screen_width = 500
screen_height = 500
screen = pg.display.set_mode([screen_width,screen_height])

# Load sounds
pg.mixer.init()
sound_main,sound_win,sound_lose = init_sounds()

# Load background image
bg_img = init_background(screen_width,screen_height)

# Load rock images
rock_imgs = init_rocks(nim)

# Load cursor image
cursor_img = init_cursor()

# Game Variables
# The position of the cursor
cursor_pos = 0

def check_empty_game(nim_instance: [int]):
    end = True
    for i in nim_instance:
        if i > 0:
            end = False
            break
    return end

# Game loop
play_sound(sound_main)
running = True
win = False
enemy_plays = False
pg.mixer.music.play()
while running:
    # Handle events
    for event in pg.event.get():
        rocks_removed = 0
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                rocks_removed = 1
            elif event.key == pg.K_2:
                rocks_removed = 2
            elif event.key == pg.K_3:
                rocks_removed = 3
            elif event.key == pg.K_4:
                rocks_removed = 4
            elif event.key == pg.K_5:
                rocks_removed = 5
            elif event.key == pg.K_6:
                rocks_removed = 6
            elif event.key == pg.K_7:
                rocks_removed = 7
            elif event.key == pg.K_8:
                rocks_removed = 8
            elif event.key == pg.K_9:
                rocks_removed = 9                    
            elif event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                # Handle moving the cursor
                cursor_pos = cursor_pos + (-1 if event.key == pg.K_LEFT else 1)
                # Stay on the range [0,len(nim))
                cursor_pos = max(0,cursor_pos)
                cursor_pos = min(len(nim) - 1,cursor_pos)
            
            # Remove a rock from the current stack
            if rocks_removed > 0 and nim[cursor_pos] >= rocks_removed:
                nim[cursor_pos] = nim[cursor_pos] - rocks_removed
                if check_empty_game(nim):
                    running = False
                    win = True
                else:
                    # Enemy plays
                    enemy_plays = True

    
    # Draw the background
    screen.blit(bg_img,(0,0))
    
    # Position where rock stacks will be painted
    starx = 100
    starty = 325
    # Draw the rock stacks
    for i in range(0,len(nim)):
        for j in range(0,nim[i]):
            screen.blit(rock_imgs[i][j],(starx + i * 32,starty - j * 32))
    # Position where cursor will be painted 
    startx = 100 + 32 * cursor_pos
    starty = 380
    screen.blit(cursor_img,(startx,starty))
    
    # Render the changes of the screen
    pg.display.flip()
    
    if enemy_plays:
        enemy_plays = False
        time.sleep(1)
    
        #Enemy plays
        nim = make_enemy_move(nim)
        
        if check_empty_game(nim):
            running = False
            win = False
        
        # Draw the background
        screen.blit(bg_img,(0,0))
    
        # Position where rock stacks will be painted
        starx = 100
        starty = 325
        # Draw the rock stacks
        for i in range(0,len(nim)):
            for j in range(0,nim[i]):
                screen.blit(rock_imgs[i][j],(starx + i * 32,starty - j * 32))
        # Position where cursor will be painted 
        startx = 100 + 32 * cursor_pos
        starty = 380
        screen.blit(cursor_img,(startx,starty))
        
        # Render the changes of the screen
        pg.display.flip()

# End of game logic

# Init font for printing messages
pg.font.init() 
my_font = pg.font.SysFont('Comic Sans MS', 30)
message = ""

# Init prizes
def get_random_prize():
    reward = ["Coin.png","Gem.png"]
    reward = reward[random.randint(0,1)]
    reward = "assets\\rewards\\" + reward
    return reward

img_prize = pg.image.load(get_random_prize())
img_prize = pg.transform.scale(img_prize,(64,64))

# Reset backgroud
screen.blit(bg_img,(0,0))

if win:
    play_sound(sound_win)
    message = my_font.render("!!You grabbed a prize!!",True,(0,0,0))
    screen.blit(message,(100,200))
    screen.blit(img_prize,(220,300))
else:
    play_sound(sound_lose)
    message = my_font.render("You grabbed nothing",True,(0,0,0))
    screen.blit(message,(100,200))

pg.display.flip()
time.sleep(7)

# Quit pygame library
pg.quit()