# numpy 배열만을 이용해 신경망 구축, 순수파이썬으로 라이브러리 없이 인공지능 구현
import pygame as py
import time
import os
import random as rd
import numpy as np

py.font.init()
py.display.set_caption("FLAPPY_BIRD_AI")

WIN_WIDTH = 512
WIN_HEIGHT = 800  #화면 크기 설정

GEN = 0
BIRD_IMGS = [py.transform.scale2x(py.image.load(os.path.join("imgs", "bird1.png"))),
            py.transform.scale2x(py.image.load(os.path.join("imgs", "bird2.png"))),
            py.transform.scale2x(py.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "base.png")))
BG_IMG = py.transform.scale2x(py.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = py.font.SysFont("comicsans", 25)


NUM_OF_BIRD = 100
MUTATERATE = 20  # n%

high_score = 0

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
    GAP = 200
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
        self.height = rd.randrange(50, 450)
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

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        
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


def tanh(x):
    return np.tanh(x)

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score :" + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    text = STAT_FONT.render("Gen : " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))
    text = STAT_FONT.render("Bird : " + str(len(birds)), 1, (0, 0, 0))
    win.blit(text, (10, 500))
    text = STAT_FONT.render("High Score : " + str(high_score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 500))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    py.display.update()

def main(genomes):  # fitness function에 해당
    global GEN
    global high_score 
    GEN += 1

    birds = []

    for i in range(NUM_OF_BIRD):
        birds.append(Bird(90, 200))
        
    base = Base(730)
    pipes = [Pipe(700)]
    win = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = py.time.Clock()
    score = 0
    run = True
    top_ten = []

    while run:
        clock.tick (30)
        add_pipe = False

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                quit()  # x를 눌렀을 때 종료되도록

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_BOTTOM.get_width() +10:
                pipe_ind = 1
        else:
            run = False
            break 
        
        rem = []
        # 새가 점프할지 말지 결정
        for i, _ in enumerate(birds):  # i번째 새와 새의 유전자 이용
            birds[i].move()
            
            inp = np.array([birds[i].y,
            abs(birds[i].y - pipes[pipe_ind].height), 
            abs(birds[i].y - pipes[pipe_ind].bottom)])  # 입력층에 해당하는 정보들
            t1 = []
            t2 = []
            t3 = []
            t4 = []
            t5 = []
            for j in range(5):
                t1.append(birds_gene[i][j])
                t2.append(birds_gene[i][j+5])
                t3.append(birds_gene[i][j+10])
                t4.append(birds_gene[i][j+15])
                t5.append(birds_gene[i][j+20])

            w1 = np.array([t1, t2, t3])
            b1 = np.array(t4)
            x = np.dot(inp, w1) + b1

            w2 = np.array(t5)
            b2 = np.array(birds_gene[i][-1])
            output = tanh(np.dot(x, w2) + b2)
            if output > 0.35:
                birds[i].jump()

        # 새의 수가 20마리 이하라면 죽는 새들의 인덱스 기억
        if len(birds) > 20:
            #print(len(birds))
            # 새가 파이프와 충돌했는지 판단
            for pipe in pipes:
                for i, bird in enumerate(birds):
                    if pipe.collide(birds[i]):
                        birds.pop(i) # 삭제해야함
                        birds_gene.pop(i)
                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True
                
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)
                pipe.move()

            # 새가 바닥에 닿았거나 위로 올라갔는지 판단
            for i, _ in enumerate(birds):
                if birds[i].y + birds[i].img.get_height() >= 800 or birds[i].y < 0:
                    birds.pop(i)
                    birds_gene.pop(i)

        else:  # 남은 새가 10마리 이하, 새가 꼭 한마리씩 죽는 것은 아님, 고로 top_ten이 10마리가 아님
            # 죽는 새들의 유전자 저장
            for pipe in pipes:
                for i, bird in enumerate(birds):
                    if pipe.collide(bird):
                        top_ten.append(birds_gene[i])
                        birds.pop(i) # 삭제해야함
                        birds_gene.pop(i)

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True
                
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)
                pipe.move()

            # 새가 바닥에 닿았거나 위로 올라갔는지 판단
            for i, _ in enumerate(birds):
                if birds[i].y + birds[i].img.get_height() >= 800 or birds[i].y < 0:
                    top_ten.append(birds_gene[i])
                    birds.pop(i)
                    birds_gene.pop(i)
        if add_pipe:
            score += 1
            if high_score < score:
                high_score = score
            pipes.append(Pipe(700))
        for r in rem:
            pipes.remove(r)

        base.move()
        
        draw_window(win, birds, pipes, base, score, GEN)

    nc(top_ten)
    print("Gen :", GEN, ", Score :", score, ", High score :", high_score)
        
def roulette():
    p = rd.randrange(100)
    if p < 20:
        return 0
    elif 20 <= p < 37:
        return 1
    elif 37 <= p < 50:
        return 2
    elif 50 <= p < 62:
        return 3
    elif 62 <= p < 74:
        return 4
    elif 74 <= p < 82:
        return 5
    elif 82 <= p < 90:
        return 6
    elif 90 <= p < 95:
        return 7
    elif 95 <= p < 98:
        return 8
    else:
        return 9

def nc(top_ten):
    # 10개의 gene을 가지고 복제 및 돌연변이 발생
    gene = [top_ten[-1], top_ten[-2], top_ten[-3], top_ten[-4], top_ten[-5],
    top_ten[-6], top_ten[-7], top_ten[-8], top_ten[-9], top_ten[-10]]
    global birds_gene

    birds_gene = [0 for i in range(NUM_OF_BIRD)]
    for i in range(5):
        birds_gene[i] = gene[i]
        birds_gene[i+5] = gene[i]
    for i in range(5):
        birds_gene[i+10] = gene[i+5]

    for i in range(NUM_OF_BIRD - 15):
        # 교배
        # 부모 설정 -> 구분할 지점 선정 -> 자식 유전자에 추가 -> birds_gene에 추가(append)
        p1 = roulette()
        while True:
            p2 = roulette()
            if p1 != p2:
                break  # p1과 p2가 항상 다른 값이 되도록
        point = rd.randrange(1, 25)

        baby = []
        for j in range(0, point):
            baby.append(gene[p1][j])
        for j in range(point, 26):
            baby.append(gene[p2][j])
        birds_gene[i + 15] = baby

    for i in range(15, NUM_OF_BIRD):  # 앞에 15개는 (0 ~ 14) 전세대와 변함이 없도록 -> 점수 향상
        mutant = rd.randrange(100)
        if mutant < MUTATERATE:  # 돌연변이 발생
            g1 = rd.randrange(26)
            g2 = rd.randrange(26)
            if mutant % 2 == 0:
                birds_gene[i][g1] = rd.uniform(-1, 1)
                birds_gene[i][g2] = rd.uniform(-1, 1)
            else:
                birds_gene[i][g1], birds_gene[i][g2] = birds_gene[i][g2], birds_gene[i][g1]

    # 최종적으로 birds_gene의 재생성

# 새의 초기 값들 설정
birds_gene = []  
birds_gene = [0 for i in range(NUM_OF_BIRD)]
for i in range(NUM_OF_BIRD):
    temp = []
    for j in range(26):
        temp.append(rd.uniform(-1, 1))
    birds_gene[i] = temp


if __name__ == '__main__':
    for i in range(50):
        main(birds_gene)
