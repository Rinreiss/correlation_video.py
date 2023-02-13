import cv2
import os
from natsort import natsorted
import numpy as np
import matplotlib.pyplot as plt

template_frame = cv2.imread('passive/1.bmp', cv2.IMREAD_GRAYSCALE)
heigth, width = template_frame.shape
template = template_frame[65:155, 805:840].astype(np.float32)
fr_n = len(os.listdir('passive'))
# cv2.imshow('sdvsdfc', template)
# cv2.waitKey(0)

corrs = []
index_max = []

minU = 55  # коэффициенты для линейного контрастирования
maxU = 200
k = 255/(maxU - minU)
b = k*minU

n = 0  # Для усреднения по 30 кадрам


for file in natsorted(os.listdir('passive')):
    file_path = 'passive/' + file
    frame = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    # Фильтр
    # frame = cv2.medianBlur(frame, 3)
    #  Контраст
    # for i in range(60, 160):
    #     for j in range(width):
    #         if frame[i][j] > minU and frame[i][j] < maxU:
    #             frame[i][j] = frame[i][j] * k - b
    # cv2.imshow('svdf', frame)
    # cv2.waitKey(0)


    for j in range(300, 866):
        corr = frame[65:155, j-17:j+18].astype(np.float32)*template
        corr = abs(corr - template**2)
        corrs = np.append(corrs, np.sum(corr))
    corrs = -corrs
    ind = np.where(corrs == max(corrs))
    index = ind[0][0] + 300
    index_max.append(index)

    color_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    cv2.circle(color_frame, (index, 70), 5, (0, 0, 255), -1)
    # cv2.imshow('itog', color_frame)
    # cv2.waitKey(30)

    corrs = []

print(index_max)



plt.rc('font', size= 16)
x = range(fr_n)
plt.plot(x, index_max)
plt.xlabel('Номер кадра, N')
plt.ylabel('Координата максимума корреляции, пкс')
plt.xlim(left=0)
plt.show()



