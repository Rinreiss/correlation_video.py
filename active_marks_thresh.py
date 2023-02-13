import cv2
import os
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Вообще каждые 30 кадров заменяются одним средним, с которым
tempX, tempY = [], []  # массивы для 30 кадров, потом усредняются и добавляются в словарь
X_folder, Y_folder = [], []  # Массивы для координат каждой точки в папке
X_all_folders, Y_all_folders = [], []
n = 0  # Счётчик кадров
max_I = 0
STD_X_thresh, STD_Y_thresh = {}, {}

plt.figure(1)
thresholds = [int(2.55*perc) for perc in range(20, 92, 10)]
# thresholds = [i for i in range(50, 226, 25)]
# print(len(thresholds))
# thresholds.insert(0, 0)
for thresh in thresholds:
    print(thresh)
    for folder in os.listdir('metka_active'):
        path = 'metka_active' + '/' + folder
        print(path)
        for file in os.listdir(path):
            img = cv2.imread(os.path.join(path, file), cv2.IMREAD_UNCHANGED)
            # img = cv2.medianBlur(img, 9)  # Медианный фильтр
            # img = cv2.bilateralFilter(img, 30, 75, 75)

            # img = cv2.GaussianBlur(img, (51, 51), 0)
            ret, img_thresh = cv2.threshold(img, thresh, 255, cv2.THRESH_TOZERO)
            # cv2.imshow('dfvdfv', img_thresh)
            # cv2.waitKey(0)



            # img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # for c in contours:
            #     # calculate moments for each contour
            #     M = cv2.moments(c)
            M = cv2.moments(img_thresh)
            # print(M)
            cX = M["m10"] / M["m00"]
            cY = M["m01"] / M["m00"]
            tempX.append(cX)  # Добавляются по 30 кадров - для одного положения
            tempY.append(cY)
            n += 1
            if n == 30:
                X_folder.append(sum(tempX)/30)  # Добавилось усредненное значение для всех иксов из одной папки поточечно
                Y_folder.append(sum(tempY)/30)
                # Xs[mark_number] = sum(tempX)/30
                # Ys[mark_number] = sum(tempY)/30
                tempX, tempY = [], []
                n = 0
        # Прошлись по всей папке, теперь общий сборник
        X_all_folders.append(X_folder)
        Y_all_folders.append(Y_folder)
        X_folder, Y_folder = [], []

    for i in range(len(X_all_folders)):
        X_all_folders[i] = sorted(X_all_folders[i])
    for i in range(len(Y_all_folders)):
        Y_all_folders[i] = sorted(Y_all_folders[i])
    print('X_all_folders', np.around(X_all_folders, 2))

    # Координаты одной точки в разных папках
    Xs = dict()  # dictionary with centroid positions of each frame
    Ys = dict()
    tempX, tempY = [], []
    for mark_number in range(10):
        for folder_number in range(5):  # Из каждой папки достается значение n-ой метки
            tempX.append(X_all_folders[folder_number][mark_number])
            tempY.append(Y_all_folders[folder_number][mark_number])
        Xs[mark_number] = tempX
        Ys[mark_number] = tempY
        tempX, tempY = [], []

    # СКО. Считается для каждой координаты из разных папок
    STD_X, STD_Y = [], []
    for i in range(10):  # 10 координат
        STD_X.append(np.std(Xs[i]))
        STD_Y.append(np.std(Ys[i]))
    STD_X_thresh[thresh] = STD_X
    STD_Y_thresh[thresh] = STD_Y

    # Xs, Ys = {}, {}
    X_all_folders = []
thresholds.insert(0, 0)
STD_X_thresh[0] = [0.015055383830618004, 0.027795254561446138, 0.03304292156840758, 0.029247340166277967, 0.033835769834850926, 0.03385982367012705, 0.045525931526352516, 0.049062441879831456, 0.04937288547625391, 0.05242210385551735]
STD_Y_thresh[0] = [0.008465548848292342, 0.006630594678192402, 0.009437706489021853, 0.007814473774173191, 0.01263316405395542, 0.01594316586688053, 0.018403170650300067, 0.02114866785403351, 0.022634783855666325, 0.022593605327779306]

#
# def gamma_f(x, g):
#     return exp(x)**g
# g_apr, cov = curve_fit(gamma_f, v11, v0451, p0=0)
# g = g_apr

# Аппроксимация
def straight_line(x, a, b):
    #  Эта функция задается, чтобы вставить в curve_fit
    return(a*x + b)

# Для порога thresh есть 10 пизиций метки (из каждой папки) и СКО (по координате для всех папок)
x = range(0, 10)  # Смещение
x = [x for x in x]
for thresh in thresholds:
    ab, cov = curve_fit(straight_line, x, STD_X_thresh[thresh])
    a, b = ab[0], ab[1]
    approx_Ys = [a * x + b for x in x]
    fig1 = plt.scatter(x, STD_X_thresh[thresh], label=str(int(thresh/255*100))+'%', linewidth=1)
    fig1 = plt.plot(x, approx_Ys)
# plt.legend(bbox_to_anchor=(1, 1))
plt.legend()
plt.xticks(x)
plt.xlabel('Смещение, мм')
plt.ylabel('СКО, пкс')
plt.ylim((0, 0.07))
plt.xlim((0, 9))
# plt.title('СКО в зависимости от порога')
plt.grid(visible='1', which='major', linewidth=0.5, c='black')
plt.grid(visible='1', which='minor', linewidth=0.1, c='black')
# plt.savefig('СКО от порога.jpg')
plt.show()


    # print('СКО х', STD_X)
    # print('СКО y', STD_Y)
'''
# Массивы со средними значениями координат
mean_Xs, mean_Ys = [], []
for i in range(len(X_all_folders[0])):
    mean_Xs.append(mean(Xs[i]))
    mean_Ys.append(mean(Ys[i]))

plt.scatter(mean_Xs, mean_Ys)
title = 'Координаты активной метки, усреднённые по сериям ' + thresh
plt.title(title)
plt.grid(visible='1', which='major', linewidth=0.5, c='black')
plt.grid(visible='1', which='minor', linewidth=0.1, c='black')
min_Y = int(min(mean_Ys))
max_Y = int(max(mean_Ys))
plt.yticks(np.arange(min_Y, max_Y+1, 0.5))
plt.show()
'''