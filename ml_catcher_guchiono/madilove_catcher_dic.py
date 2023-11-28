"""
落ちてくる野田シロクマと村上オットセイをひろって仕分ける、という動きにしたい

10/19　拾って仕分ける動きが書けないので、まずは簡単に落ちてくるものを取る、にする(参考「ねこの一日」)
何がどうなればゲームクリアになるか、ゲームオーバーになるか考えること
アイテムを辞書型に(マッチョvs車内販売を参考に)

【10/26問題点】
198行目にどうしてエラーが出るのかわからない

"""
import pygame
import sys
import random
from pygame.locals import*

img_bg = pygame.image.load("aurora_3.png")
img_icon = pygam.image.load("ml_icon.png")
img_title = pygame.image.load("opening_2.png")
img_gameover = pygame.image.load("gameover.png")
img_gameclear = pygame.image.load("gameclear.png")

img_ryogoku = pygame.image.load("ryogoku_dot_s.png")

img_item = {
    "n":pygame.image.load("noda_dot_s.png"), #正しい野田さん
    "nf":pygame.image.load("noda_fake_s.png"), #フェイク野田さん
    "m":pygame.image.load("murakami_dot_s.png"), #正しい村上さん
    "mf":pygame.image.load("murakami_fake_s.png") #フェイク村上さん
}

STEP_READY = 0
STEP_PLAY = 1
STEP_GAMEOVER = 2
STEP_GAMECLEAR = 3

SURFACE_WIDTH = 960
SURFACE_HEIGHT = 600

PLAYER_WIDTH = 250
PLAYER_HEIGHT = 250

ITEM_TYPE_NUM = 4
ITEM_WIDTH = 150
ITEM_HEIGHT = 150

ITEM_MAX = 50
POWER_MAX = 150

WHITE = (255, 255, 255)

step = STEP_READY
timer = 0
px = (SURFACE_WIDTH / 2) 
py = 550

power = POWER_MAX
item_hit = [False] * ITEM_MAX
item_x = [0] * ITEM_MAX
item_y = [0] * ITEM_MAX
item_type = [""] * ITEM_MAX
item_num = 10

flg_turn = False
last_key = pygame.K_LEFT

def move_player(key):
    global px, py, flg_turn, last_key

    if key[pygame.K_UP] == 1:
        py -= 20
        if py < 0:
            py = 500

    elif key[pygame.K_DOWN] == 1:
        py += 20
        if py > 500:
            py = 0

    elif key[pygame.K_LEFT] == 1:
        px -= 20
        if px < 0:
            px = 700
        if last_key == pygame.K_RIGHT:
            flg_turn = True
            last_key = pygame.K_LEFT

    elif key[pygame.K_RIGHT] == 1:
        px += 20
        if px > 700:
            px = 0
        if last_key == pygame.K_LEFT:
            flg_turn = True
            last_key = pygame.K_RIGHT

def locate_item():
    for i in range(ITEM_MAX):
        item_x[i] = random.randint(50, SURFACE_WIDTH - 50 - ITEM_WIDTH / 2)
        item_y[i] = random.randint(-400, 0)

        if (i + 1) % ITEM_TYPE_NUM == 0:
            item_type[i] = "n"
        elif (i + 1)  % ITEM_TYPE_NUM == 1:
            item_type[i] = "nf"
        elif (i + 1)  % ITEM_TYPE_NUM == 2:
            item_type[i] = "m"
        elif (i + 1)  % ITEM_TYPE_NUM == 3:
            item_type[i] = "mf"

def move_item():
    for i in range(item_num):
        item_y[i] += 4 + i / 4
        if item_y[i] > SURFACE_HEIGHT:
            item_hit[i] = False
            item_x[i] = random.randint(50, SURFACE_WIDTH - 50 - ITEM_WIDTH / 2)

        if item_hit[i] == False:
            if is_hit(px, py, item_x[i], item_y[i]) == True:
                item_hit[i] = True
                get_item(item_type[i])

def is_hit(x1, y1, x2, y2):
    if (abs(x1 - x2) <= ITEM_WIDTH / 2 + PLAYER_WIDTH / 2
        and abs(y1 - y2) <= ITEM_HEIGHT / 2 + PLAYER_HEIGHT / 2):
        return True
    return False

def get_item(category):
    global power

    if category == "n" and "m":
        power += 10
        if power > POWER_MAX:
            power = POWER_MAX
    elif category == "nf" and "mf":
        power -= 5
        if power == 0:
            power = 0
            
def draw_text(surface, x, y, text, size, col):
    font = pygame.font.Font(None, size)
    s = font.render(text, True, col)
    x = x - s.get_width() / 2
    y = y - s.get_height() / 2
    surface.blit(s, [x, y])

def main():
    global step, timer, power, px, item_num, img_bg, img_ryogoku, flg_turn
       
    pygame.init()
    pygame.display.set_caption("マヂラブキャッチャー")
    pygame.display.set_icon(img_icon)
    img_bg = pygame.transform.smoothscale(img_bg, [SURFACE_WIDTH, SURFACE_HEIGHT])
    surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    category = item_type
    clock = pygame.time.Clock()
    locate_item()

    while True:
        timer += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()

        if step == STEP_READY:
            if key[pygame.K_SPACE] == 1:
                step = STEP_PLAY
                timer = 0
            
            surface.blit(img_bg, [0, 0])
            surface.blit(img_title, [155, 264])
            draw_text(surface, 480, 380, "PRESS SPACE to START!", 60, WHITE)
            power = POWER_MAX
            px = SURFACE_WIDTH / 2
            item_num = 10
            locate_item()
            get_item(category)

        elif step == STEP_PLAY:
            if power <= 0:
                step = STEP_GAMEOVER
                timer = 0
            if item_num != ITEM_MAX and timer % 100 == 0:
                item_num += 5

            power -= 1
            move_player(key)
            move_item()

        elif step == STEP_GAMEOVER:
            if timer == 50:
                step = STEP_READY
                timer = 0
                surface.blit(img_gameover, [300, 300])

        surface.blit(img_bg, [0, 0])
        surface.blit(img_item[item_type[i]], [0, 0])

        if flg_turn == True:
            img_ryogoku = pygame.transform.flip(img_ryogoku, True, False)
            flg_turn = False

        surface.blit(img_ryogoku, [px - PLAYER_WIDTH / 2, py - PLAYER_HEIGHT / 2])
        surface.fill((250, 237, 240), (50, 30, POWER_MAX, 40))
        surface.fill((236, 37, 90), (50, 30, power, 40))

        if step == STEP_GAMEOVER:
           surface.blit(img_gameover, [146, 224])
            
        pygame.display.update()
        clock.tick(20)        
        
main()
