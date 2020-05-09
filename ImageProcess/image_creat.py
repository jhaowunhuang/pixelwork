import cv2
import numpy as np
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
        self.spot_size = 5 #equivalent to spot size
        self.edge_factor = 0 #near edge effect
        self.signals = 100 #number of signals in each pixel


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
                x_pos = skewnorm.rvs(a=self.edge_factor, loc=it.multi_index[0], scale=self.spot_size, size=self.signals)
                y_pos = skewnorm.rvs(a=self.edge_factor, loc=it.multi_index[1], scale=self.spot_size, size=self.signals)
                hist, xedges, yedges = np.histogram2d(x_pos, y_pos, bins=512, range=[[0, 512], [0, 512]])
                self.output_img_arr += hist
        print(self.input_img_arr.size)
        # allow the file name from arguments
        current_output_file_name = self.output_file_name if self.output_file_name else 'sample/output.jpg'
        print('current_output_file_name: ', current_output_file_name)
        cv2.imwrite(current_output_file_name, self.output_img_arr)
        print(datetime.datetime.now() - time1)
