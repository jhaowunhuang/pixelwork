import cv2
import numpy as np
import scipy.stats

class pixelwork:
    def __init__(self):
        self.pix_map = {} #output image info
        self.img_height = 512 #default height
        self.img_width = 512 #default width
        self.sigma = 4 #equivalent to spot size
        self.cov = [[self.sigma, 0], [0, self.sigma]] #spot shape
        self.ax = 0 #x distribution skew
        self.ay = 0 #y distribution skew
        self.signals = 100 #number of signals in each pixel

    #add individual pixels
    def add_pixel(self, x, y):
        self.pix_map[(x, y)] = scipy.stats.skewnorm.rvs([self.ax, self.ay], [x, y], [self.sigma, self.sigma], [self.signals, 2]).T
        
        #self.pix_map[(x, y)] = np.random.multivariate_normal([x, y], self.cov, self.signals).T

    #get coordinates of black pixels in an image
    def add_image(self, input_img):
        img_arr = cv2.imread(input_img, cv2.IMREAD_GRAYSCALE)
        self.img_width, self.img_height = img_arr.shape

        def nearest_edge(x, y):
            left = right = x
            while left > 0 and right < self.img_width - 1:
                left -= 1
                right += 1
                if img_arr[(left, y)] != 0:
                    edge_x = left + 1 - x
                    break
                if img_arr[(right, y)] != 0:
                    edge_x = right - 1 - x
                    break
            up = down = y
            while up > 0 and down < self.img_height - 1:
                up -= 1
                down += 1
                if img_arr[(x, up)] != 0:
                    edge_y = up + 1 - y
                    break
                if img_arr[(x, down)] != 0:
                    edge_y = down - 1 - y
                    break
            return edge_x, edge_y

        for x in range(self.img_width):
            for y in range(self.img_height):
                if img_arr[x, y] == 0:
                    self.ax, self.ay = nearest_edge(x, y)
                    
 #                   self.cov = [[min(self.sigma, near_x_edge), 0], [0, min(self.sigma, near_y_edge), 0]]
                    self.add_pixel(x, y)

    #draw the simulated image
    def draw(self):
        x_sum = np.concatenate([self.pix_map[item][0] for item in self.pix_map])
        y_sum = np.concatenate([self.pix_map[item][1] for item in self.pix_map])
        xedges = range(self.img_width + 1)
        yedges = range(self.img_height + 1)
        H, xedges, yedges = np.histogram2d(x_sum, y_sum, bins = (xedges, yedges))
        cv2.imwrite('../Sample/output.jpg', H)


new_pic = pixelwork()
new_pic.add_image('../Sample/input.jpg')
#new_pic.add_pixel(256, 256)
new_pic.draw()

