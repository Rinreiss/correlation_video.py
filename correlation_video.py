import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

cap = cv2.VideoCapture('nomark.avi')
fps = int(cap.get(cv2.CAP_PROP_FPS))
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
wkey = 1000//fps  # waitKey in ms
fr_n = -1  # frame number


# a = np.array([[3.], [5.]])
# b = np.array([[7], [11]])
# print(a**2)
# print(b)
# print(a*b)

# Берем кадр из видео, чтобы вырезать из него столбец - фильтр
# cv2.set(cv2.CAP_PROP_POS_MSEC, )
_, template_frame = cap.read()  # Первый кадр, вырезаем столбец 370
template_frame = cv2.cvtColor(template_frame, cv2.COLOR_BGR2GRAY)
template = template_frame[170:311, 365:375].astype(np.float32)
# cv2.imshow('template', template)
# cv2.waitKey(0)
hei, wid = template_frame.shape
xh = range(hei)
x = range(wid)



output = cv2.VideoWriter('correlation_mark_crop_contr.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, (wid, hei))
minU = 55  # коэффициенты для линейного контрастирования
maxU = 200
k = 255/(maxU - minU)
b = k*minU
corrs = []  # Массив для сумм произведений по столбцам

index_max = []  # Массив номеров столбцов, которые совпадают с template
while cap.isOpened():
    flag, frame = cap.read()
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fr_n += 1
    except:
        break

    for i in range(150, 320):
        for j in range(wid):
            if gray[i][j] > minU and gray[i][j] < maxU:
                gray[i][j] = gray[i][j] * k - b
    # gray = cv2.medianBlur(gray, 9)
    # gray = cv2.bilateralFilter(gray, 15, 75, 75)


    for j in range(5, wid-5):
        corr = gray[170:311, j-5:j+5].astype(np.float32) * template
        corr = abs(corr - template**2)  # Вычитаю квадрат фильтра, чтобы узнать, насколько проивзедение близко к фильтру
        # print(type(corr[0][0]), corr[210][8])
        # corr /= np.max(corr)
        # print(type(np.sum(corr)))
        corrs = np.append(corrs, np.sum(corr))

    corrs /= max(corrs)
    corrs = -corrs  # Нормировала и перевернула, чтобы можно было искать максимум - совпадающий столбец, а не минимум
    # plt.plot(x, corrs)
    # plt.show()
    ind = np.where(corrs == max(corrs))

    index = ind[0][0] + 5 # Индекс максимума по кадру - совпадающего столбца

    color_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    cv2.circle(color_frame, (index, 200), 5, (0, 0, 255), -1)
    # cv2.imshow('myvideo', color_frame)
    output.write(color_frame)
    # cv2.waitKey(wkey)
    if cv2.waitKey(wkey) == ord('q'):
        break
    index_max.append(index)
    corrs = []

cap.release()
output.release()
'''
x_fr = range(fr_n+1)  # Ось абсисс для максимумов корреляций по кадрам
fig1 = plt.figure()
plt.plot(x_fr, index_max)
# plt.title('Координаты максимумов корреляции кадров с маской')
plt.xlabel('Номер кадра, N', fontsize=16)
plt.ylabel('Координата максимума корреляции, пкс', fontsize=16)
# plt.show()
fig1.savefig('коорд максимумов корреляции crop contr.jpg')
print(index_max)
'''
