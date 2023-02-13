import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

cap = cv2.VideoCapture('nomark.avi')
fps = int(cap.get(cv2.CAP_PROP_FPS))
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
wkey = 1000//fps  # waitKey in ms
deriv_ = []
f = open('skleyka.txt', 'w')


while cap.isOpened():
    flag, frame = cap.read()
    try:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        break
    if flag:
        deriv = []
        #cv2.imshow('Frame', frame)
        for i in range(len(frame[0])-2):
            # print(grey[240][i])
            # print(grey[240][i+1] - grey[240][i])
            deriv.append(int(grey[240][i+1]) - int(grey[240][i]))
            f.write(str(deriv[i])+' ')
        deriv_.append(deriv)

        f.write('\n')
        cv2.imshow('Frame', medianFrame)
    if cv2.waitKey(wkey) == ord('q'):
        f.close()
        break
print(len(deriv_))

fig, ax = plt.subplots()
line, = ax.plot(range(len(deriv_[0])), deriv_[0])
def animate(i):
    line.set_ydata(deriv_[i])  # update the data.
    return line,
ani = animation.FuncAnimation(
    fig, animate, interval=wkey, blit=True, save_count=len(deriv_))
ani.save('derivativesskleyka.gif', writer='pillow', fps=15)
