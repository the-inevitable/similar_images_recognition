""" 
A module to determine similar images in a given folder.
""" 

import argparse
import glob
import time

import numpy as np
from PIL import Image
from PIL import ImageFilter

parser = argparse.ArgumentParser(description='finds similar images in given folder')
parser.add_argument('-p', '--path', help='input path to folder with images, e.g. ./dev_dataset', type=str)
args = parser.parse_args()

filepathes = glob.glob(args.path + '*' if args.path.endswith('/') else args.path + '/*')

DIFFERENTIATION_LIMIT = 6000

def compare_all(filepaths): 
	"""
	A function to calculate difference between
	two images, presented as np arrays.
	Takes 2 image paths as parameters (string).
	Prints a message if given images have 
	difference within the limit.
	How it works: 
	- each image from the input gets greyscaled, resized (i.e. normalized)
	and converted to an array of integers,
	- calculate difference between both image arrays and reduce it to a summation
	- if calculated difference is less than above defined Limit,
	then the images are quite similar.
	""" 
	tstart_compare = time.time() 
	for filepath in filepaths: 
		for filepath_to_compare in filepathes: 
			if filepath == filepath_to_compare:
				break 
			else:
				compare_two(filepath, filepath_to_compare)  
	print('comparing all files in folder took : ', time.time() - tstart_compare)

def compare_two(path1, path2):
	"""
	A function to calculate difference between
	two images, presented as np arrays.
	Takes 2 image paths as parameters (string).
	Prints a message if given images are differenct enough.
	""" 
	images_container = [np.array(Image.open(f).convert('L').resize((16,16), resample=Image.BICUBIC)).astype(np.int) for f in [path1,path2]]
	difference = np.abs(images_container[0] - images_container[1]).sum()
	if difference <= DIFFERENTIATION_LIMIT:
		print('{0} and {1}'.format(path1.split('/')[-1], path2.split('/')[-1]))

if __name__ == '__main__': 
	compare_all(filepathes)
