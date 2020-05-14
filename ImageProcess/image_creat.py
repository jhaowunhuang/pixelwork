import cv2
import numpy as np
from scipy.stats import multivariate_normal as mn 
from scipy.stats import skewnorm
import datetime

class PixelWork:
    def __init__(self):
        self.input_file_name = ''
        self.input_img_arr = None
        self.output_file_name = ''
        self.output_img_arr = None
        self.img_height = 0 #default height
        self.img_width = 0 #default width
        self.spot_size = 10 #equivalent to spot size
        self.edge_factor = 0 #near edge effect
        self.signals = 200 #number of signals in each pixel


    # get input image array 
    def add_image(self):
        # allow the file name from arguments
        current_input_file_name = self.input_file_name if self.input_file_name else 'sample/input.jpg'
        print('current_input_file_name: ', current_input_file_name)
        self.input_img_arr = cv2.imread(current_input_file_name, cv2.IMREAD_GRAYSCALE)
        self.output_img_arr = np.zeros(self.input_img_arr.shape)
        self.img_width, self.img_height = self.input_img_arr.shape


    # draw the simulated image
    def draw(self):
        time1 = datetime.datetime.now()
        it = np.nditer(self.input_img_arr, flags=['multi_index'])
        for elem in it:
            if elem < 128:
                pos = mn.rvs(it.multi_index, [[self.spot_size, 0], [0, self.spot_size]], size=self.signals)
                extra = np.array([[-1, -1]])
                for item in pos:
                    if all([0 <= int(round(x, 0)) < 512 for x in item]) and self.input_img_arr[int(round(item[0], 0)), int(round(item[1], 0))] >= 128:
                        for _ in range(3):
                            extra = np.concatenate((extra, [it.multi_index]))
                pos = np.concatenate((pos, extra))
                x_pos, y_pos = pos.T
                hist, xedges, yedges = np.histogram2d(x_pos, y_pos, bins=512, range=[[0, 512], [0, 512]])
                self.output_img_arr += hist 
            else:
                pos = mn.rvs(it.multi_index, [[self.spot_size, 0], [0, self.spot_size]], size=self.signals//2)
                for item in pos:
                    if all([0 <= int(round(x, 0)) < 512 for x in item]) and self.input_img_arr[int(round(item[0], 0)), int(round(item[1], 0))] < 128:
                       pos = pos 
                x_pos, y_pos = pos.T
                hist, xedges, yedges = np.histogram2d(x_pos, y_pos, bins=512, range=[[0, 512], [0, 512]])
                self.output_img_arr += hist 
        # allow the file name from arguments
        current_output_file_name = self.output_file_name if self.output_file_name else 'sample/output.jpg'
        print('current_output_file_name: ', current_output_file_name)
        cv2.imwrite(current_output_file_name, self.output_img_arr)
        print(datetime.datetime.now() - time1)
