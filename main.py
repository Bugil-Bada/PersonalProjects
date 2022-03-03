import gym
import numpy as np
import random as rd
import math

env = gym.make('CartPole-v0')

env._max_episode_steps = 50000
GOAL = 10000  # 목표 점수. 넘으면 종료
LEN_OF_GEN = 300  # 개체수
MUTATE_RATE = 25  # 퍼센트
LEN_OF_ARR = 33

score = list()  # 개체 별 성적표

cnt = 0
best_score = 0

gene = []


def relu(x):
    return np.maximum(0, x)


def softmax(x):
    x = np.exp(x)/np.sum(np.exp(x))
    return x


def sigmoid(x):
    sig = 1 / (1 + math.exp(-x))
    return sig


def decide_action(i, input_observation):
    X = np.array(input_observation)  # X.shape = (4,)

    W1 = np.array([[gene[i][0], gene[i][1], gene[i][2], gene[i][3]], [gene[i][4], gene[i][5], gene[i][6], gene[i][7]], [gene[i][8], gene[i][9], gene[i][10], gene[i][11]], [gene[i][12], gene[i][13], gene[i][14], gene[i][15]]])  # (4, 4)
    B1 = np.array([gene[i][16], gene[i][17], gene[i][18], gene[i][19]])  # (4,)

    W2 = np.array([[gene[i][20], gene[i][21]], [gene[i][22], gene[i][23]], [gene[i][24], gene[i][25]], [gene[i][26], gene[i][27]]])  # (4, 2)
    B2 = np.array([gene[i][28], gene[i][29]])  # (2,)

    W3 = np.array([[gene[i][30]], [gene[i][31]]])  # (2, 1)
    B3 = np.array([gene[i][32]])

    A1 = np.dot(X, W1) + B1  # (4, 4)
    Z1 = np.tanh(A1)
    A2 = np.dot(Z1, W2) + B2  # (4, 2)
    Z2 = np.tanh(A2)
    output = np.dot(Z2, W3) + B3

    output = np.tanh(output)

    if output > 0.5:
        return 1
    else:
        return 0


# 유전자 초기값 설정
gene = [0 for i in range(LEN_OF_GEN)]
for i in range(LEN_OF_GEN):
    temp1 = []
    for j in range(LEN_OF_ARR):
        temp1.append(rd.uniform(-1, 1))
    gene[i] = temp1


while True:
    score = list()
    top_five = list()
    cnt += 1
    print('Gen {0} - best_score = '.format(cnt), end='')
    # 실행 후 성적순으로 나열
    for i in range(LEN_OF_GEN):
        observation = env.reset()
        award = 0
        for t in range(50000):
            # env.render()

            action = decide_action(i, observation)

            observation, reward, done, info = env.step(action)
            award += reward

            if done:
                score.append((award, i))
                break

    score.sort()
    best_score = score[-1]
    top_five = [score[-1][1], score[-2][1], score[-3][1], score[-4][1], score[-5][1]]

    new_gene = list()
    for i in range(20):
        new_gene.append(gene[top_five[i % 5]])  # 상위 5개의 개체는 그대로 다음세대 보존 -> 기록이 나빠질 순 없음

    # spend_time 이 가장 큰 10개의 유전자 선택하여 조합
    for i in range(20, LEN_OF_GEN):  # 10마리는 이미 만들었고, 나머지 수의 gene 을 새로 만든다
        m = rd.randrange(100)
        p1 = rd.randrange(5)  # 동등하게 확률 부여
        temp = list()  # 1차원 리스트. gene[i] = temp -> 2차원 리스트인 gene 재생성
        while True:
            p2 = rd.randrange(5)
            if p1 != p2:
                break  # p1과 p2가 항상 다른 값이 되도록
        point = rd.randrange(0, LEN_OF_ARR)

        for j in range(0, point):
            if m < MUTATE_RATE:
                temp.append(rd.uniform(-1, 1))
                continue
            temp.append(gene[p1][j])

        for j in range(point, LEN_OF_ARR):
            if m < MUTATE_RATE:
                temp.append(rd.uniform(-1, 1))
                continue
            temp.append(gene[p2][j])

        new_gene.append(temp)

    print('{0}, top_five = {1}'.format(int(best_score[0]), top_five))
    if int(best_score[0]) >= GOAL:
        print('gene : ', gene[top_five[0]])
        break
    gene = new_gene

env.close()
