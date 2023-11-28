"""
落ちてくる野田シロクマと村上ガチラシをひろって仕分ける、という動きをさせたい
↓
10/24　拾って仕分ける動きが書けないので、まずは得点になるアイテム、そうでないアイテムを
落として区別しながら取っていく内容、にする(参考「ねこの一日」)
何がどうなればゲームクリアになるか、ゲームオーバーになるか考えること
ゲージをどうするか/タイムアタック的なものにするか/オープニング画面が出ない
野田、村上が画面下で荒ぶる

【10/26問題点】
①ゲームタイトルと「PRESS SPACE to START!」が表示されない
※スペースキー押下でゲームはスタートします。リスタートもしますがﾋﾄﾞｲです。
②ウィンドウ下方で野田・村上が荒ぶる
③もしかしたら当たり判定も少し怪しいかもしれない

ぐっちーに見てもらった
完成！感謝！

"""
import pygame
import sys
import random

img_bg = pygame.image.load("aurora_3.png")
img_icon = pygame.image.load("ml_icon.png")

img_noda = pygame.image.load("noda_dot_s.png")
img_noda_fake = pygame.image.load("noda_fake_s.png")
img_murakami = pygame.image.load("murakami_dot_s.png")
img_murakami_fake = pygame.image.load("murakami_fake_s.png")
img_ryogoku = pygame.image.load("ryogoku_dot_s.png")
img_title = pygame.image.load("opening_2.png")
img_gameover = pygame.image.load("gameover.png")
#img_gameclear = pygame.image.load("gameclear.png")

#固定値
STEP_READY = 0
STEP_PLAY = 1
STEP_GAMEOVER = 2
STEP_GAMECLEAR = 3

SURFACE_WIDTH = 960
SURFACE_HEIGHT = 600

PLAYER_WIDTH = 100
PLAYER_HEIGHT = 150

ITEM_TYPE_NUM = 4
ITEM_WIDTH = 100
ITEM_HEIGHT = 150

ITEM_MAX = 50
POWER_MAX = 150

WHITE = (255, 255, 255)

step = 0
timer = 0
px = (SURFACE_WIDTH / 2-50 ) 
py = 500

power = POWER_MAX
item_hit = [False] * ITEM_MAX

item_x = [0] * ITEM_MAX
item_y = [0] * ITEM_MAX
item_f_x = [0] * ITEM_MAX
item_f_y = [0] * ITEM_MAX

item_type = [""] * ITEM_MAX
item_num = 10

flg_turn = False
last_key = pygame.K_LEFT

def move_player(key):
    global px, py, flg_turn, last_key

    if key[pygame.K_UP] == 1:
        py -= 20
        if py < 0:
            py = 750

    elif key[pygame.K_DOWN] == 1:
        py += 20
        if py > 600:
            py = 0

    elif key[pygame.K_LEFT] == 1:
        px -= 20
        if px < 0:
            px = 1110
        #if last_key == pygame.K_RIGHT:
            #flg_turn = True
            #last_key = pygame.K_LEFT

    elif key[pygame.K_RIGHT] == 1:
        px += 20
        if px > 1110:
            px = 0
        #if last_key == pygame.K_LEFT:
            #flg_turn = True
            #last_key = pygame.K_RIGHT

def locate_item():
    for i in range(ITEM_MAX):
        item_x[i] = random.randint(0, SURFACE_WIDTH)
        item_y[i] = random.randint(-150, SURFACE_HEIGHT)
        
        if i % ITEM_TYPE_NUM == 0:
            item_type[i] = "n" #正しい野田さん
        elif i % ITEM_TYPE_NUM == 1:
            item_type[i] = "nf" #フェイク野田さん
        elif i % ITEM_TYPE_NUM == 2:
            item_type[i] = "m" #正しい村上さん
        elif i % ITEM_TYPE_NUM == 3:
            item_type[i] = "mf" #フェイク村上さん
            
def move_item():
    for i in range(item_num):
        item_y[i] += 1 + i / 3
        if item_y[i] > SURFACE_HEIGHT:
            item_y[i] = ITEM_HEIGHT
            item_hit[i] = False
            item_x[i] = random.randint(0, SURFACE_WIDTH)
            for j in range(0, i-1):
                if item_x[j] == item_x[i]:
                    item_x[j] = random.randint(0, SURFACE_WIDTH)
                    j = 0
                    
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

    if (category == "n") or (category == "m"):
        power += 10
        if power > POWER_MAX:
            power = POWER_MAX
    elif (category == "nf") or (category == "mf"):
        power -= 15
        if power < 0:
            power = 0

def draw_item(surface):
    for i in range(item_num):
        if item_hit[i] == False and item_type[i] == "n":
            surface.blit(img_noda, [item_x[i] - ITEM_WIDTH / 2, item_y[i] - ITEM_HEIGHT / 2])
        elif item_hit[i] == False and item_type[i] == "nf":
            surface.blit(img_noda_fake, [item_x[i] - ITEM_WIDTH / 2, item_y[i] - ITEM_HEIGHT / 2])
        elif item_hit[i] == False and item_type[i] == "m":
            surface.blit(img_murakami, [item_x[i] - ITEM_WIDTH / 2, item_y[i] - ITEM_HEIGHT / 2])
        elif item_hit[i] == False and item_type[i] == "mf":
            surface.blit(img_murakami_fake, [item_x[i] - ITEM_WIDTH / 2, item_y[i] - ITEM_HEIGHT / 2])

def draw_text(surface, x, y, text, size, col):
    font = pygame.font.Font(None, size)
    s = font.render(text, True, col)
    x = x - s.get_width() / 2
    y = y - s.get_height() / 2
    surface.blit(s, [x, y])

def main():
    global step, timer, power, px, py, item_num, img_bg, img_ryogoku, flg_turn
       
    pygame.init()
    pygame.display.set_caption("マヂラブキャッチャー")
    pygame.display.set_icon(img_icon)
    img_bg = pygame.transform.smoothscale(img_bg, [SURFACE_WIDTH, SURFACE_HEIGHT])
    surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    clock = pygame.time.Clock()
    
    while True:
        timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        surface.blit(img_bg, [0, 0])
        key = pygame.key.get_pressed()
        
        if step == STEP_READY:
            if key[pygame.K_SPACE] == 1:
                step = STEP_PLAY
                timer = 0
                power = POWER_MAX
            surface.blit(img_title, [155, 264])
            draw_text(surface, 480, 380, "PRESS SPACE to START!", 60, WHITE) #スペースキー押下でゲームスタート

            locate_item()
                
        elif step == STEP_PLAY:
            if item_num != ITEM_MAX and timer % 100 == 0:
                item_num += 5
            surface.fill((250, 237, 240), (50, 30, POWER_MAX, 40))
            surface.fill((236, 37, 90), (50, 30, power, 40))
            power -= 0.5
            surface.blit(img_ryogoku, [px - PLAYER_WIDTH / 2, py - PLAYER_HEIGHT / 2])
            move_player(key)
            draw_item(surface)
            move_item()

            if power <= 0:
                step = STEP_GAMEOVER
                timer = 0
                power = 0
                
        elif step == STEP_GAMEOVER:
            if timer == 50:
                step = STEP_READY
                timer = 0
                power = POWER_MAX
                item_num = 10
                px = (SURFACE_WIDTH / 2-50 )
                py = 500

            surface.blit(img_gameover, [146, 224])
            #surface.fill((250, 237, 240), (50, 30, POWER_MAX, 40))
            #surface.fill((236, 37, 90), (50, 30, power, 40))
            
        #if flg_turn == True:
            #img_ryogoku = pygame.transform.flip(img_ryogoku, True, False)
            #flg_turn = False

        #if step == STEP_GAMEOVER: とりあえず置いておく
           #surface.blit(img_gameover, [146, 224]) とりあえず置いておく
           
        pygame.display.update()
        clock.tick(20)        
        
main()
