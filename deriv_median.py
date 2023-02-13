import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

cap = cv2.VideoCapture('nomark.avi')
fps = int(cap.get(cv2.CAP_PROP_FPS))
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
wkey = 1000//fps  # waitKey in ms
deriv_ = []
#f = open('skleyka.txt', 'w')
fr_n = -1  # frame number

while cap.isOpened():
    flag, frame = cap.read()
    try:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fr_n += 1
    except:
        break
    frameIds = [fr_n - 1, fr_n - 2, fr_n, (fr_n + 1) // length, (fr_n + 2) // length]
    # sum_frame = [[0]*len(frame[0])]*len(frame)     # Значение каждого пикселя = сумма яркостей (R+G+B)
    # for i in range(len(frame)-1):
    #     for j in range(len(frame[0])-1):
    #         sum_frame[i][j] = sum(frame[i][j])
    frames = []  # Случайные 25 кадров записываются в массив
    for fid in frameIds:
        cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
        ret, frameForMed = cap.read()
        frames.append(frameForMed)
    medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)  # Кадр = медиана из 5
    if flag:
    #     deriv = []
    #     #cv2.imshow('Frame', frame)
    #     for i in range(len(frame[0])-2):
    #         # print(grey[240][i])
    #         # print(grey[240][i+1] - grey[240][i])
    #         deriv.append(int(grey[240][i+1]) - int(grey[240][i]))
    #         #deriv.append(sum(frame[120][i+1]) - sum(frame[120][i]))
    #         f.write(str(deriv[i])+' ')
    #     deriv_.append(deriv)
    #
    #     f.write('\n')
        cv2.imshow('Frame', medianFrame)
    if cv2.waitKey(wkey) == ord('q'):
    #    f.close()
        break
# print(len(deriv_))

# fig, ax = plt.subplots()
# line, = ax.plot(range(len(deriv_[0])), deriv_[0])
# def animate(i):
#     line.set_ydata(deriv_[i])  # update the data.
#     return line,
# ani = animation.FuncAnimation(
#     fig, animate, interval=wkey, blit=True, save_count=len(deriv_))
# ani.save('derivativesskleyka.gif', writer='pillow', fps=15)
