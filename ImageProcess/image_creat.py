import cv2
import numpy as np
from scipy.stats import multivariate_normal


class PixelWork:
    def __init__(self):
        self.input_file_name = ''
        self.input_img_arr = None 
        self.output_file_name = ''
        self.output_img_arr = None 
        self.img_height = 512 #default height
        self.img_width = 512 #default width
        self.sigma = 50 #equivalent to spot size
        self.cov = [[self.sigma, 0], [0, self.sigma]] #spot shape
        self.signals = 128 #number of signals in each pixel


    # add individual pixels
    def add_pixel(self, x, y):
        self.output_img_arr[(x, y)] = multivariate_normal([x, y], self.cov, self.signals).T


    # get coordinates of black pixels in an image
    def add_image(self):
        # allow the file name from arguments
        current_input_file_name = self.input_file_name if self.input_file_name else 'sample/input.jpg'
        print('current_input_file_name: ', current_input_file_name)
        self.input_img_arr = cv2.imread(current_input_file_name, cv2.IMREAD_GRAYSCALE)
        self.output_img_arr = np.zeros(self.input_img_arr.shape)
        self.img_width, self.img_height = self.input_img_arr.shape
#        test_input = multivariate_normal(np.zeros(self.input_img_arr.shape), self.cov, self.signals)
        for x in range(self.img_width):
            print(x)
            for y in range(self.img_height):
                temp_input = np.random.multivariate_normal([x, y], self.cov, self.signals)
                temp_sum = 0
                cur_pix_state = self.input_img_arr[x, y]
                for i in temp_input:
                    i_x = int(round(i[0], 0))
                    i_y = int(round(i[1], 0))
                    if 0 <= i_x < self.img_width and 0 <= i_y < self.img_height:
                        if cur_pix_state < 128:
                            if self.input_img_arr[i_x, i_y] < 128:
                                temp_sum += 0.5
                            else:
                                temp_sum += 1
                        else:
                            if self.input_img_arr[i_x, i_y] >= 128:
                                temp_sum += 0.5
                            else:
                                temp_sum += 0
                self.output_img_arr[x, y] = temp_sum


    # draw the simulated image
    def draw(self):
        # x_sum = np.concatenate([self.pix_map[item][0] for item in self.pix_map])
        # y_sum = np.concatenate([self.pix_map[item][1] for item in self.pix_map])
        # xedges = range(self.img_width + 1)
        # yedges = range(self.img_height + 1)
        # H, xedges, yedges = np.histogram2d(x_sum, y_sum, bin = (xedges, yedges))
        # allow the file name from arguments
        current_output_file_name = self.output_file_name if self.output_file_name else 'sample/output.jpg'
        print('current_output_file_name: ', current_output_file_name)
        cv2.imwrite(current_output_file_name, self.output_img_arr)
