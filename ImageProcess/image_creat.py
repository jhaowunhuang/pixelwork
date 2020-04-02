import cv2
import numpy as np


class PixelWork:
    def __init__(self):
        self.pix_map = {}  # output image info
        self.img_height = 512  # default height
        self.img_width = 512  # default width
        self.sigma = 16  # equivalent to spot size
        self.cov = [[self.sigma, 0], [0, self.sigma]]  # spot shape
        self.signals = 100  # number of signals in each pixel
        self.input_file_name = ''
        self.output_file_name = ''

    # add individual pixels
    def add_pixel(self, x, y):
        self.pix_map[(x, y)] = np.random.multivariate_normal([x, y], self.cov, self.signals).T

    # get coordinates of black pixels in an image
    def add_image(self):
        # allow the file name from arguments
        current_input_file_name = self.input_file_name if self.input_file_name != "" else 'sample/input.jpg'
        print('current_input_file_name: ', current_input_file_name)
        img_arr = cv2.imread(current_input_file_name, cv2.IMREAD_GRAYSCALE)
        self.img_width, self.img_height = img_arr.shape
        for x in range(self.img_width):
            for y in range(self.img_height):
                if img_arr[x, y] == 0:
                    self.add_pixel(x, y)

    # draw the simulated image
    def draw(self):
        x_sum = np.concatenate([self.pix_map[item][0] for item in self.pix_map])
        y_sum = np.concatenate([self.pix_map[item][1] for item in self.pix_map])
        xedges = range(self.img_width + 1)
        yedges = range(self.img_height + 1)
        H, xedges, yedges = np.histogram2d(x_sum, y_sum, bins=(xedges, yedges))
        # allow the file name from arguments
        current_output_file_name = self.output_file_name if self.output_file_name != "" else 'sample/output.jpg'
        print('current_output_file_name: ', current_output_file_name)
        cv2.imwrite(current_output_file_name, H)
