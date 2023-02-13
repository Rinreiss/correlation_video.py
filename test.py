import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

img = cv2.imread('metka_active/2/1_1_s1.bmp', cv2.IMREAD_GRAYSCALE)
ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
cv2.imshow('sdvd', img)
cv2.waitKey(0)

h, w = img.shape

'''
img = cv2.imread('metka_active/3/2_8_s17.bmp', cv2.IMREAD_UNCHANGED)
max_I = 0
for i in range(len(img)):
    for j in range(len(img[0])):
        if img[i][j] > max_I:
            max_I = img[i][j]
print(max_I)'''


'''cap = cv2.VideoCapture('nomark.avi')
fps = int(cap.get(cv2.CAP_PROP_FPS))
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 501
wkey = 1000//fps  # waitKey in ms
deriv_ = []
#f = open('skleyka.txt', 'w')
fr_n = -1  # frame number
n = 0

while cap.isOpened():
    flag, frame = cap.read()
    try:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fr_n += 1
    except:
        break
    frameIds = [fr_n - 1, fr_n - 2, fr_n, (fr_n + 1) // length, (fr_n + 2) // length]
    frames = []  # Случайные 25 кадров записываются в массив
    for fid in frameIds:
        cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
        ret, frameForMed = cap.read()
        frames.append(frameForMed)
    medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)  # Кадр = медиана из 5
    # Reset frame number to 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Convert background to grayscale
    grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)

    # Loop over all frames
    ret = True
    while (ret):
        # Read frame
        ret, frame = cap.read()
        # Convert current frame to grayscale
        try:  #  Если не сделать трай, то после последнего кадра будет ошибка - пустой кадр в грей
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            break
        # Calculate absolute difference of current frame and
        # the median frame
        dframe = cv2.absdiff(frame, grayMedianFrame)
        # Treshold to binarize
        th, dframe = cv2.threshold(dframe, 50, 255, cv2.THRESH_BINARY)
        # Display image
        cv2.imshow('frame', dframe)
        if cv2.waitKey(wkey) == ord('q'):
            break
        n+=1  # ошибка с преобразованием к серому после 452 кадра
        #print(n)

    # Release video object
    cap.release()

    # Destroy all windows
    cv2.destroyAllWindows()
    # if flag:
    #     cv2.imshow('Frame', medianFrame)
    if cv2.waitKey(wkey) == ord('q'):
        break
'''