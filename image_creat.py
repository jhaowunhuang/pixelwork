import cv2
import numpy as np

def func():
    radius = 512
    position = [256, 256]
    signals = int(1000000)
    cov = [[radius, 0], [0, radius]]
    x, y = np.random.multivariate_normal(position, cov, signals).T
    xedges = range(512)
    yedges = range(512)
    H, xedges, yedges = np.histogram2d(x, y, bins = (xedges, yedges))
    H = H.T
    print(H.max())
    print(H.min())
    cv2.imwrite('test.jpg', H)

func()
