import argparse
from ImageProcess.image_creat import PixelWork


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_name", help='input file name')
    parser.add_argument("output_file_name", help='output file name')
    args = parser.parse_args()
    print("Input file name: ", args.input_file_name, ", Output file name: ", args.output_file_name)
    new_pic = PixelWork()
    new_pic.output_file_name = args.output_file_name
    new_pic.input_file_name = args.input_file_name
    new_pic.add_image()
    new_pic.draw()


main()