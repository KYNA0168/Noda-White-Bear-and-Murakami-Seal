#https://algorithm.joho.info/programming/python/pygame-mouse-click/
#クリックした場所にキャラクターを移動

# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

#画像読み込み
img_bg = pygame.image.load("room_washitsu.png")
img_icon = pygame.image.load("ml_icon.png")
img_title = pygame.image.load("opening_shiwake.png")
img_gameclear = pygame.image.load("gameclear.png")
img_gameover = pygame.image.load("gameover.png")

img_ml == {
    "n" : pygame.image.load("noda_dot_s.png"),
    "nf" : pygame.image.load("noda_fake_s.png"),
    "m" : pygame.image.load("murakami_dot_s.png"),
    "mf" : pygame.image.load("murakami_fake_s.png")
}

#固定値を設定
SURFACE_WIDTH = 900
SURFACE_HEIGHT = 500

ML_MAX = 50

#初期値を設定
score = 0
timer = 0
ml_num = ML_MAX

def locate_ml():
    for i in range
    

def main():
    global img_bg

    pygame.init()       # pygame初期化
    pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))  # 画面設定
    img_bg = pygame.transform.smoothscale(img_bg, [SURFACE_WIDTH, SURFACE_HEIGHT])
    surface.blit(img_bg)
    player = pygame.image.load("ryogoku_dot_s.png").convert_alpha()    # プレイヤー画像の取得

    (x, y) = (300, 200)

    while (1):
        pygame.display.update()             # 画面更新
        pygame.time.wait(30)                # 更新時間間隔
        #screen.fill((0, 20, 0, 0))          # 画面の背景色
        screen.blit(player, (x, y))    # プレイヤー画像の描画
        screen.blit(img_bg, [0, 0])
        
        for event in pygame.event.get():
            # マウスクリックで画像移動
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                x -= player.get_width() / 2
                y -= player.get_height() / 2
        # 終了用のイベント処理
            if event.type == QUIT:          # 閉じるボタンが押されたとき
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_ESCAPE:   # Escキーが押されたとき
                    pygame.quit()
                    sys.exit()

        #screen.blit(img_bg, [0, 0])
        pygame.display.update()

if __name__ == "__main__":
        main()


#①「pygame」モジュールをインポートする。
#②画面のサイズを設定する。
#③円の中心座標を画面の中心に設定する。
#④Pygameを初期化する。[pygame.init]
#⑤主人公キャラの画像を取得する。(表示位置はx=300, y=100)
#⑥画面を更新する。
#⑦更新時間の間隔を設定する。
#⑧画面の背景色を黒に設定する。
#⑨キャラクターを指定した座標(x, y)に描画する。
#⑩イベント処理をする。
#・マウスが左クリックされたら、クリックした座標を(x, y)に格納する。
#・画面の閉じるボタンが押されたら終了する。
#⑪6-10の処理を繰り返す。
