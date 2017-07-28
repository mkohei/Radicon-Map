import cv2
import numpy as np
import matplotlib.pyplot as plt

SH, SW = 900-45, 1600

CORNER = [[174, 118], [668, 117], [217, 340], [620, 345]]
SCREEN = [[0, 0], [SW, 0], [0, SH], [SW, SH]]
pts1 = np.float32(CORNER)
pts2 = np.float32(SCREEN)


CAR = ['0', '1', '2']
COLOR = ['W', 'R', 'G', 'B', 'M', 'C', 'Y']
FILENAMES = []
for car in CAR:
    for color in COLOR:
        FILENAMES.append('./colors/' + car + color + '.png')

bins_range = range(0, 256)

for file in FILENAMES:
    img = cv2.imread(file)

    M = cv2.getPerspectiveTransform(pts1,pts2)
    scn = cv2.warpPerspective(img , M, (SW, SH))

    #cv2.imshow('img', scn)
    #cv2.waitKey(0)
    B, G, R = scn[:, :, 0], scn[:, :, 1], scn[:, :, 2]
    #B, G, R = B.flatten(), G.flatten(), R.flatten()

    """
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=False)
    ax0.hist(R, bins=bins_range, color='r')
    ax1.hist(G, bins=bins_range, color='g')
    ax2.hist(B, bins=bins_range, color='b')
    plt.setp((ax0, ax1, ax2))
    ax0.grid(True)
    ax1.grid(True)
    ax2.grid(True)
    """

    plt.figure("screen")
    plt.imshow(scn[:, :, ::-1])
    '''
    plt.figure("R")
    plt.gray()
    plt.imshow(R)
    plt.figure("G")
    plt.gray()
    plt.imshow(G)
    plt.figure("B")
    plt.gray()
    plt.imshow(B)
    '''
    '''
    plt.figure("R")
    plt.gray()
    plt.imshow(R < 130)
    plt.figure("G")
    plt.gray()
    plt.imshow(G < 130)
    plt.figure("B")
    plt.gray()
    plt.imshow(B < 130)
    '''

    det = (R<130)*(G<130)*(B<130)
    detY, detX = np.where(det)
    meanX = int(round(np.average(detX)))
    meanY = int(round(np.average(detY)))

    out = np.zeros((SH, SW, 3))*255

    cv2.circle(out, (meanX, meanY), 100, (0, 255, 0), -1)
    out[:, :, 0][det] = 255
    out[:, :, 1][det] = 255
    out[:, :, 2][det] = 255

    print(meanX, meanY)

    #plt.figure('R*G*B')
    #plt.gray()
    #plt.imshow(out)

    cv2.imshow("a", out)
    cv2.waitKey(0)


