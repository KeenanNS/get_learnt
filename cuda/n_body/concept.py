import numpy as np
import random as rand

G = 6.67e-11

points = []
for _ in range(1000):
    points.append([rand.randint(0,100), rand.randint(0,100), rand.randint(0,100), rand.randint(0,10)])

def norm_and_rhat(points1, points2):
    x = points1[0] - points2[0]
    y = points1[1] - points2[1]
    z = points1[2] - points2[2]
    norm = np.sqrt(x**2 + y**2 + z**2)
    rhat = [x/norm, y/norm, z/norm]
    return norm, rhat

def force(mi, mj, norm, rhat):
    return [G * ((mi * mj)/((norm**2)+0.001)) * hat for hat in rhat]


sum_forces = []
i = 0
for set in points:
    print(i)
    i+=1
    forces = []
    for set2 in points:
        if not set2 == set:
            norm, rhat = norm_and_rhat(set, set2)
            forces.append(force(set[3], set2[3], norm, rhat))
    sum_forces.append([sum(forces[:][i]) for i in range(3)])
