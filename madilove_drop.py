"""
落ちてくる野田シロクマと村上ガチラシが積まれると消えるっていうやつ

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
img_gameclear = pygame.image.load("gameclear.png")

#固定値
STEP_READY = 0
STEP_PLAY = 1
STEP_GAMEOVER = 2
STEP_GAMECLEAR = 3

SURFACE_WIDTH = 960
SURFACE_HEIGHT = 600
