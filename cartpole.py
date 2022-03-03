# 학습시키지 않으면 이런 느낌

import numpy as np
import gym
import random as rd

gene = list()
gene = [[0.1171446437122925, 0.16119996248266943, -0.29072675108731505, -0.9804141960892707, 0.6810052567458704, 0.7419818676891858, 0.3318545963458748, -0.7045808682092107, 0.9749335576925251, 0.17551083479308893, -0.5891521884146285, -0.9916922525129293, 0.5746988232449093, 0.6793993936425498, 0.8877353945627822, -0.5958229151356855, -0.5794698469829584, -0.5706637916336001, -0.6462472040420479, -0.5405831716331941, -0.651476480736292, 0.7590369543342768, -0.1086241883187804, 0.08464638658537771, -0.809692199074098, -0.5005691691558583, 0.9849067742428206, -0.4475799071781372, 0.10837701173669756, -0.028835268101087275, -0.7881606849851754, 0.5931421061945361, 0.5658016264869579]]


env = gym.make('CartPole-v0')
env._max_episode_steps = 5000


def decide_action(input_observation):

    i=0
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


def random_decide(obs):
    if obs[3] > 0:
        return 1
    else:
        return 0


observation = env.reset()
for t in range(5003):
    env.render()
    action = random_decide(observation)
    observation, reward, done, info = env.step(action)
    if done:
        break

