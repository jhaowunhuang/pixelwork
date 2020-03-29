import cv2
import numpy as np

class pixelwork:
    def __init__(self):
        self.pix_map = {}
        self.img_size = 512
        self.sigma = 8 
        self.cov = [[self.sigma, 0], [0, self.sigma]]
        self.signals = 100

    def add_pixel(self, x, y):
        self.pix_map[(x, y)] = np.random.multivariate_normal([x, y], self.cov, self.signals).T

    def draw(self):
        x_sum = np.concatenate([self.pix_map[item][1] for item in self.pix_map])
        y_sum = np.concatenate([self.pix_map[item][0] for item in self.pix_map])
        xedges = range(self.img_size)
        yedges = range(self.img_size)
        H, xedges, yedges = np.histogram2d(x_sum, y_sum, bins = (xedges, yedges))
        print(H.max())
        cv2.imwrite('test.jpg', H)

new_pic = pixelwork()
for x in range(100, 250):
    for y in range(50, 200):
        new_pic.add_pixel(x, y)

for x in range(512):
    for y in range(512):
        if (x - 350) * (x - 350) + (y - 250) * (y - 250) <= 2500:
            new_pic.add_pixel(x, y)

new_pic.draw()
