import cv2
import numpy as np

# show video
# len(frames) = 404, CAP_PROP_FRAME_COUNT = 448
cap = cv2.VideoCapture('nomarks.avi')
fps = int(cap.get(cv2.CAP_PROP_FPS))
wkey = 1000//fps  # waitKey in ms

frames = []
# frame = массив [[[ /// ]]]. 1 массив ([[ ... ]]) - 1 строка
while cap.isOpened():
    flag, frame = cap.read()
    if flag:
        cv2.imshow('Frame', frame)
        frames.append(frame)
    if cv2.waitKey(wkey) == ord('q'):
        break
print(len(frames))
print('count', cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(frames[0])

'''
cv2.namedWindow("result")  # создаем главное окно
cv2.namedWindow("settings")  # создаем окно настроек

def nothing(*args):
    pass

# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('v1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)
crange = [0, 0, 0, 0, 0, 0]

frame_counter = 1
n = 1
print('count', cap.get(cv2.CAP_PROP_FRAME_COUNT))
flag = True
while True:
    if not flag:
        print(frame_counter)
        frame_counter = 1
        cap = cv2.VideoCapture('ctestavi.avi')
    flag, img = cap.read()
    if flag:
        print(n)
        print(img)
        # print(img)   # тут можно увидеть, что видео цветное
        # print('frame_counter', frame_counter)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # считываем значения бегунков
        h1 = cv2.getTrackbarPos('h1', 'settings')
        s1 = cv2.getTrackbarPos('s1', 'settings')
        v1 = cv2.getTrackbarPos('v1', 'settings')
        h2 = cv2.getTrackbarPos('h2', 'settings')
        s2 = cv2.getTrackbarPos('s2', 'settings')
        v2 = cv2.getTrackbarPos('v2', 'settings')

        # формируем начальный и конечный цвет фильтра
        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        # накладываем фильтр на кадр в модели HSV
        thresh = cv2.inRange(hsv, h_min, h_max)
        cv2.imshow('Origin', img)
        cv2.imshow('result', thresh)

        n += 1
        if cv2.waitKey(wkey) == ord('q'):
            break
    else:
        print(img)

'''
'''        
M = cv2.moments(thresh)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
cv2.circle(thresh, (cX, cY), 10, (100, 0, 255), -1)
cv2.putText(thresh, "centroid", (cX - 25, cY - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
# Moment
image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    # calculate moments for each contour
    M = cv2.moments(thresh)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
cv2.circle(thresh, (cX, cY), 10, (0, 0, 255), -1)
cv2.putText(thresh, "centroid", (cX - 25, cY - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#print(frame_counter)
'''