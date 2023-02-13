import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('active.avi')
fps = int(cap.get(cv2.CAP_PROP_FPS))
wkey = 1000//fps  # waitKey in ms
centers = dict()
tempX, tempY = [], []
Xs, Ys = [], []
avXs, avYs = [], []  # Среднее
n = 0
t = 0
sec = 0


while cap.isOpened:
    flag, frame = cap.read()
    if flag:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, grey = cv2.threshold(grey, 150, 255, 0)
        M = cv2.moments(grey)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # cv2.circle(grey, (cX, cY), 3, (80, 0, 255), -1)
        # cv2.putText(grey, "centroid", (cX - 25, cY - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        # cv2.imshow('pic', grey)
        # cv2.moveWindow('pic', 0, 150)
        # cv2.waitKey(0)
        # cv2.destroyWindow('pic')
        tempX.append(cX)
        tempY.append(cY)
        Xs.append(cX)
        Ys.append(cY)
        n += 1
        t += 1
        if n == 30:
            avcX = sum(tempX)/30
            avcY = sum(tempY)/30
            centers[sec] = (avcX, avcY)
            avXs.append(avcX)
            avYs.append(avcY)
            n = 0
            sec += 1
            tempX, tempY = [], []
    if t == 1650:
        break

print(centers)
print(avXs)

plt.plot(avXs)
plt.title('Координаты метки по оси X')
plt.xlabel('Время, с')
plt.ylabel('Координата, пкс')
plt.grid(visible='1', which='major', linewidth=0.5, c='black')
plt.grid(visible='1', which='minor', linewidth=0.1, c='black')
plt.figure(2)
plt.plot(avYs)
plt.title('Координаты метки по оси Y')
plt.xlabel('Время, с')
plt.ylabel('Координата, пкс')
plt.show()
# plt.plot(Xs)
# plt.figure(2)
# plt.plot(Ys)
# plt.show()
