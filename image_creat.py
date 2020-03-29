import cv2
import numpy as np

def func():
    radius = 256
    position = [256, 256]
    cov = [[radius // 4, 0], [0, radius // 4]]
    x, y = np.random.multivariate_normal(position, cov, 50000).T
    xedges = range(512)
    yedges = range(512)
    H, xedges, yedges = np.histogram2d(x, y, bins = (xedges, yedges))
    H = H.T
    print(H.max())
    print(H.min())
    cv2.imwrite('test.jpg', H)

func()
