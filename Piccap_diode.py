import cv2
import os
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

tempX, tempY = [], []  # массивы для 30 кадров, потом усредняются и добавляются в словарь
X_folder, Y_folder = [], []  # Массивы для координат каждой точки в папке
X_all_folders, Y_all_folders = [], []
n = 0  # Счётчик кадров

for folder in os.listdir('metka_active'):
    path = 'metka_active' + '/' + folder
    print(path)
    for file in os.listdir(path):
        img = cv2.imread(os.path.join(path, file), cv2.IMREAD_UNCHANGED)
        img = cv2.medianBlur(img, 9)
        # img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # for c in contours:
        #     # calculate moments for each contour
        #     M = cv2.moments(c)
        M = cv2.moments(img)
        # print(M)
        cX = (M["m10"] / M["m00"])  # Центры меток без округлений
        cY = (M["m01"] / M["m00"])
        tempX.append(cX)
        tempY.append(cY)
        n += 1
        if n == 30:
            X_folder.append(sum(tempX)/30)  # Добавились все иксы из одной папки
            Y_folder.append(sum(tempY)/30)
            # Xs[mark_number] = sum(tempX)/30
            # Ys[mark_number] = sum(tempY)/30
            tempX, tempY = [], []
            n = 0

    X_all_folders.append(X_folder)
    Y_all_folders.append(Y_folder)
    X_folder, Y_folder = [], []

for i in range(len(X_all_folders)):
    X_all_folders[i] = sorted(X_all_folders[i])
for i in range(len(Y_all_folders)):
    Y_all_folders[i] = sorted(Y_all_folders[i])
print(np.around(X_all_folders, 2))

# Координаты одной точки в разных папках
Xs = dict()  # dictionary with centroid positions of each frame
Ys = dict()
tempX, tempY = [], []
for mark_number in range(10):
    for folder_number in range(5):
        tempX.append(X_all_folders[folder_number][mark_number])
        tempY.append(Y_all_folders[folder_number][mark_number])
    Xs[mark_number] = tempX
    Ys[mark_number] = tempY
    tempX, tempY = [], []

# СКО
STD_X, STD_Y = [], []
for i in range(10):
    STD_X.append(np.std(Xs[i]))
    STD_Y.append(np.std(Ys[i]))
print('СКО х', STD_X)
print('СКО y', STD_Y)
# print('СКО х', np.around(STD_X, 2))
# print('СКО y', np.around(STD_Y, 2))

# Массивы со средними значениями координат
mean_Xs, mean_Ys = [], []
for i in range(len(X_all_folders[0])):
    mean_Xs.append(mean(Xs[i]))
    mean_Ys.append(mean(Ys[i]))

print('mean x', mean_Xs)
print('mean y', mean_Ys)
pix_mm = []
# print()
for i in range(1, len(mean_Xs)):
    pix_mm.append(mean_Xs[i] - mean_Xs[i-1])
pix_mm = sum(pix_mm)/len(pix_mm)  # В среднем на 1мм приходится столько пикселов
print('пикселей на мм', pix_mm)
print('Смещение по у:', 4*round((mean_Ys[-1] - mean_Ys[0])/pix_mm, 3), 'мм')  # Это без учета сжатия фото по у

# Аппроксимация
def straight_line(x, a, b):
    #  Эта функция задается, чтобы вставить в curve_fit
    return(a*x + b)

ab, cov = curve_fit(straight_line, mean_Xs, mean_Ys)
a, b = ab[0], ab[1]

approx_Ys = [a*mean_X + b for mean_X in mean_Xs]

plt.scatter(mean_Xs, mean_Ys, label='Вычисленные координаты')
plt.plot(mean_Xs, approx_Ys, label='Аппроксимирующая прямая y = ax + b')
plt.legend()
plt.title('Координаты активной метки, усреднённые по сериям')
plt.grid(visible='1', which='major', linewidth=0.5, c='black')
plt.grid(visible='1', which='minor', linewidth=0.1, c='black')
min_Y = int(min(mean_Ys))
max_Y = int(max(mean_Ys))
plt.yticks(np.arange(min_Y, max_Y+1, 0.5))
plt.show()





        # cv2.circle(img, (cX, cY), 3, (100, 0, 255), -1)
        # cv2.putText(img, "centroid", (cX - 25, cY - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        # centers[file] = (cX, cY)

