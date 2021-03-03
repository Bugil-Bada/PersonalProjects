import pygame as py
import time
import os
import random as rd

py.font.init()
py.display.set_caption("PLAY_FLAPPY_BIRD")


WIN_WIDTH = 600
WIN_HEIGHT = 800  #화면 크기 설정

GEN = 0
BIRD_IMGS = [py.transform.scale2x(py.image.load(os.path.join("imgs", "bird1.png"))),
            py.transform.scale2x(py.image.load(os.path.join("imgs", "bird2.png"))),
            py.transform.scale2x(py.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "base.png")))
BG_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = py.font.SysFont("comicsans", 25)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 30
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):  # 새가 올라가는 것 계산, 가중치에 따라 얘가 올라감
        self.vel = -8.2
        self.tick_count = 0
        self.height = self.y

    def move(self):  # 떨어지는 것 계산
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 10:
            d = 10
        if d < 0:
            d -= 1.7
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -80:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -70:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = py.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return py.mask.from_surface(self.img)

class Pipe:
    GAP = 90
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = py.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = rd.randrange(30, 220)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = py.mask.from_surface(self.PIPE_TOP)
        bottom_mask = py.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))



high_score = 0

def draw_window(win, bird, pipes, base, score, game_active):
    win.blit(BG_IMG, (0,0))
    if game_active:
        for pipe in pipes:
            pipe.draw(win)

        text = STAT_FONT.render("Score :" + str(score), 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
        bird.draw(win)

    text = STAT_FONT.render("High Score : " + str(high_score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 370))

    base.draw(win)
 
    py.display.update()

base = Base(400)
pipes = [Pipe(300)]
bird = Bird(90, 200)
win = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = py.time.Clock()
score = 0
run = True
game_active = True

while run:
    clock.tick(30)
    bird.move()
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
            quit()
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE and game_active:
                bird.jump()
            if event.key == py.K_SPACE and not game_active:
                game_active = True
                bird = Bird(90,140)

    add_pipe = False

    rm = []
    for pipe in pipes:
        if not pipe.passed and pipe.x < bird.x:
            pipe.passed = True
            add_pipe = True
        if pipe.x < -52 and pipe.passed:    
            rm.append(pipe)

        pipe.move()
    for r in rm:
        pipes.remove(r)

    if add_pipe:
        score += 1
        if high_score < score:
            high_score = score

        pipes.append(Pipe(300))

    if bird.y + bird.img.get_height() >= 400 or bird.y < 0 or pipe.collide(bird):
        game_active = False
        score = 0
        pipes = [Pipe(400)]

    base.move()
    draw_window(win, bird, pipes, base, score, game_active)
