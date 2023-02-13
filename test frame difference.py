import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

cap = cv2.VideoCapture('nomark.avi')
fps = int(cap.get(cv2.CAP_PROP_FPS))
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 501
wkey = 1000//fps  # waitKey in ms
deriv_ = []
#f = open('skleyka.txt', 'w')
fr_n = -1  # frame number
n = 0
ret, prev_frame = cap.read()
prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
deriv = []

while cap.isOpened():
    flag, frame = cap.read()
    try:
        curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fr_n += 1
    except:
        break
    if flag:
        dframe = cv2.absdiff(curr_frame, prev_frame)
        #cv2.imshow('frame', dframe)
        prev_frame = curr_frame

        tempder = []
        for i in range(len(curr_frame[0])-2):
            tempder.append(int(dframe[240][i + 1]) - int(dframe[240][i]))
        deriv.append(tempder)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break

fig, ax = plt.subplots()
line, = ax.plot(range(len(deriv[0])), deriv[0])
plt.ylim((-50, 50))
def animate(i):
    line.set_ydata(deriv[i])  # update the data.
    return line,
ani = animation.FuncAnimation(
    fig, animate, interval=wkey, blit=True, save_count=len(deriv))
ani.save('deriv difference.gif', writer='pillow', fps=15)

