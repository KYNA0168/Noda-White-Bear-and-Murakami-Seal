''' 
野田さんの「スクランブルを超えろ」を参考に

10/25
「マッチョvs車内販売」をベースにしてみた

【10/26問題点】
①両國さんがびくともしない
②体力ゲージが表示されない(青いゲージはタイマー)
③野田・村上は表示され、動くが途中で止まる(当たり判定か?)

'''
import pygame
import random
import sys
import math
from pygame.locals import *

#画像読み込み
img_bg = pygame.image.load('aurora_3.png')
img_icon = pygame.image.load('ml_icon.png')

#プレイヤー画像
img_ryogoku = pygame.image.load('ryogoku_dot_s.png')

#アイテム画像
img_item= {
    'n':pygame.image.load('noda_dot_s.png'), #正しい野田さん
    'nf':pygame.image.load('noda_fake_s.png'), #フェイク野田さん
    'm':pygame.image.load('murakami_dot_s.png'), #正しい村上さん
    'mf':pygame.image.load('murakami_fake_s.png'), #フェイク村上さん
 }

img_gauge = pygame.image.load('hp.png')#体力ゲージ
img_title = pygame.image.load('opening_2.png')
img_gameover = pygame.image.load('gameover.png')

#固定値
STEP_READY = 0 #ゲームのステップ(ゲーム開始準備) 
STEP_PLAY = 1 #ゲームのステップ(ゲームプレイ)
STEP_GAMEOVER = 2 #ゲームのステップ(ゲームオーバー)    

SURFACE_WIDTH = 960 #サーフェスの幅
SURFACE_HEIGHT = 600 #サーフェスの高さ

PLAYER_WIDTH = 100 #プレイヤーの幅
PLAYER_HEIGHT = 250 #プレイヤーの高さ

ITEM_TYPE_NUM = 4
ITEM_WIDTH = 100
ITEM_HEIGHT = 150
ITEM_MAX = 30
POWER_MAX = 30

LINE_T = 50 #上側スタート座標補正数値
LINE_B =SURFACE_HEIGHT - 50 #下側スタート座標補正数値
LINE_R = SURFACE_WIDTH - 200 #右側スタート座標補正数値

SIGNAL_MAX = 220 #信号ゲージの最大値(いらなければコメントアウト)
START_PX = (SURFACE_WIDTH / 2-50 )#プレイヤーのスタートX座標
START_PY = 500 #プレイヤーのスタートY座標

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#各種初期値を設定
step = 0
timer = 0 #タイマー変数
px = START_PX
py = START_PY
signal = SIGNAL_MAX

best_score = 0
score = 0
power = POWER_MAX
p_gauge = 100 #HP
p_invincible = 0 #無敵状態を管理する

item_position = [''] * ITEM_MAX #アイテムの配置場所
item_angle = [0]  * ITEM_MAX
item_x = [0] * ITEM_MAX #アイテムのx座標(画像の中央)
item_y = [0] * ITEM_MAX #アイテムのy座標(画像の中央)
item_type = [''] * ITEM_MAX #アイテムのタイプ
item_speed = [0] * ITEM_MAX
item_period = [0] * ITEM_MAX

jump_up = 0
jump_status = 0

#flg_turn = False #プレイヤーの反転フラグ
#last_key = pygame.K_LEFT #最後に押したキー

#プレイヤーの移動
def move_player(key):
    global px, py, flg_turn, last_key, jump_up, jump_status

    if key[pygame.K_RIGHT] == 1:
        px += 20
        if px > 1200:
            px = 0
        #if last_key == [pygame.K_LEFT]:
            #flg_turn = True
            #last_key = pygame.K_RIGHT
    
    if key[pygame.K_LEFT] == 1:
        px -= 20
        if px <0:
            px = 1200
        #if last_key == pygame.K_RIGHT:
            #flg_turn = True
            #last_key = pygame.K_LEFT
            
    if key[pygame.K_SPACE] == 0 and jump_status == 1:
        jump_status = 2

    if key[pygame.K_SPACE] and jump_status < 2: #ジャンプ準備
        jump_status = 1
        jump_up += 2
        if jump_up < 16:
            jump_up = 16
        elif jump_up > 36:
            jump_up = 36
                        
    if key[pygame.K_SPACE] == 0 and jump_status == 1: #ジャンプ開始
        jump_status = 2

    if jump_status == 2: #ジャンプ中
        py -= jump_up
        jump_up -= 1
        if py > 500: #ジャンプ終了
            py = 500
            jump_status = 0        

#アイテム初期座標と座標を設定 
def locate_item():
    for i in range(ITEM_MAX):
        #初期座標を設定
        position_random_number = random.randint(0, 2)
        if position_random_number == 0:
            item_position[i] = 'T' #上側に配置
        elif position_random_number == 1:
            item_position[i] = 'B'
        elif position_random_number == 2:
            item_position[i] = 'R'

        angle_random_number = random.randint(0, 2)
        if item_position[i] == 'T':
            if angle_random_number == 0:
                item_angle[i] = 45
            elif angle_random_number == 1:
                item_angle[i] = 90
            elif angle_random_number == 2:
                item_angle[i] = 135
            item_x[i] = random.randint(960, 600)
            item_y[i] = LINE_T + random.randint(-20, 20)

        elif item_position[i] == 'B' :
            if angle_random_number == 0:
                item_angle[i] = -135
            elif angle_random_number == 1:
                item_angle[i] = -90
            elif angle_random_number == 2:
                item_angle[i] = -45
            item_x[i] = random.randint(960, 600)
            item_y[i] = LINE_B + random.randint(-20, 20)

        elif item_position[i] == 'R':
            if angle_random_number == 0:
                item_angle[i] = -135
            elif angle_random_number == 1:
                item_angle[i] = 135
            elif angle_random_number == 2:
                item_angle[i] = 180
            item_x[i] = LINE_R + random.randint(-20, 20)
            item_y[i] = random.randint(400, 630)

        #タイプを設定
        if (i + 1) % ITEM_TYPE_NUM == 0:
            item_type[i] = 'n' #正しい野田さん
        elif (i + 1) % ITEM_TYPE_NUM == 1:
            item_type[i] = 'nf' #フェイク野田さん 
        elif (i + 1) % ITEM_TYPE_NUM == 2:
             item_type[i] = 'm' #正しい村上さん
        elif (i + 1) % ITEM_TYPE_NUM == 3:
            item_type[i] = 'mf'  #フェイク村上さん
        
        if item_type[i] == 'nf':
            item_speed[i] = 15
        elif item_type[i] == 'mf':
            item_speed[i] = 3
        else:
            item_speed[i] = ITEM_TYPE_NUM +i/ITEM_TYPE_NUM

        if (item_type[i] == 'n') or (item_type[i] == 'm'):
            item_period[i] = random.randint(30, 100)

#アイテムの移動と当たり判定
def is_hit_item():
    global index, timer
   
    for i in range(ITEM_MAX):
        if item_type[i] == 'n':
            if timer == item_period[i]:
                item_angle[i] -= 45
            if (timer > item_period[i]
                and timer % 20 == 0):
                item_angle[i] -= 90
            elif (timer > item_period[i]
                  and timer % 10 == 0):
                item_angle[i] += 90

        if (item_type[i] != 'm'
            or timer < item_period[i]
            or item_period[i] + 50 < timer):
            cos = math.cos(math.radians(item_angle[i]))
            sin = math.sin(math.radians(item_angle[i]))
            item_x[i] += item_speed[i] * cos
            item_y[i] += item_speed[i] * sin

        if is_hit(px, py, item_x[i], item_y[i]):
            return True
    return False 

#当たり判定
def is_hit(x1, x2, y1, y2):
    if math.sqrt((x1-x2)**2 + (y1-y2) ** 2) < 40:
        return True
    return False

#アイテムにあたった時の処理
def get_item(category):
    global power

    if category ==  'n' and 'm' :
        power += 5
    elif category == 'nf' and 'mf':
        power -= 15
        if power < 0:
            power = 0

#文字表示の関数
def draw_text(screen,x,y,text,size,col):
    font = pygame.font.Font(None,size)
    s = font.render(text,True,col)
    x = x - s.get_width()/2
    y = y - s.get_height()/2
    screen.blit(s,[x,y])

#main関数
def main():
    global step, timer, px, py, p_gauge, p_invincible, power, score, signal, category
    global idx, img_player, flg_turn, jump_status, jump_up

    pygame.init()
    pygame.display.set_caption('マヂラブキャッチャー')
    pygame.display.set_icon(img_icon)
    surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    category = item_type
    clock = pygame.time.Clock()                           
   
    #無限ループ
    while True:
        timer += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
         
    #ステップごとの処理
        if step == STEP_READY:
            if key[pygame.K_SPACE] == 1:
                step = STEP_PLAY
                timer = 0
            surface.blit(img_bg, [0, 0])
            surface.blit(img_title, [155, 264])
            draw_text(surface, 480, 380, 'PRESS SPACE to START!', 60, WHITE) #スペースキー押下でゲームスタート
                   
            locate_item()
            get_item(category)
            
        elif step == STEP_PLAY:            
            move_player(pygame.key.get_pressed())
            signal -= 1
            if jump_status == 0:
                surface.blit(img_ryogoku,(px, py))
            elif jump_status == 1:
                surface.blit(img_ryogoku,(px, py))
            elif jump_status == 2:
                surface.blit(img_ryogoku, (px, py))
            
            if is_hit_item():
                step = STEP_GAMEOVER
                timer = 0
                surface.blit(img_gameover, [146, 224])
                
            elif signal <= 0: 
                step = STEP_GAMEOVER
                timer = 0
                surface.blit(img_gameover, [146, 224])

            surface.blit(img_bg, [0, 0])
            surface.blit(img_ryogoku, [START_PX, START_PY])

            for i in range(ITEM_MAX):
                x = item_x[i] - PLAYER_WIDTH / 2
                y = item_y[i] - PLAYER_HEIGHT / 2
                surface.blit(img_item[item_type[i]], [x, y])
                
            surface.fill((250, 237, 240), (10, 550, SIGNAL_MAX, 25))
            surface.fill((0, 230, 230), (10, 550, signal, 25))
            surface.blit(img_gauge, (10, 600)) #体力ゲージ
            pygame.draw.rect(surface, (32, 32, 32), [10 + p_gauge*2, 450, (100 - p_gauge)*2, 25]) #ダメージを受けたら矩形で塗りつぶす
            draw_text(surface, 800, 20, 'SCORE' +str(score), 30, BLACK)
            signal = SIGNAL_MAX
            score = 0
            p_gauge = 100
            p_invincible = 0

        elif step == STEP_GAMEOVER:
            if signal == 0:
                step = STEP_READY
                px = START_PX
                py = START_PY  
         
        pygame.display.update()
        clock.tick(30)

main()
