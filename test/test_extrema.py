import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from src.sift import SIFT
from time import time

import sys
import cv2
import numpy as np
import math


def parse_arguments(argv):
    n = len(argv)
    sigma, k = 1.6, math.sqrt(2)
    if n < 2:
        print("Usage: python {} image_path [-s value] [-k value]".format(argv[0]))
        sys.exit(1)
    if n > 6:
        if argv[2] == '-s' and argv[4] == '-k':
            sigma = float(argv[3])
            k = float(argv[5])
        if argv[2] == '-k' and argv[4] == 's':
            k = float(argv[3])
            sigma = float(argv[5])
    if n > 4:
        if argv[2] == '-s':
            sigma = float(argv[3])
        if argv[2] == '-k':
            k = float(argv[3])
    return sigma, k

def test(argv):
    sigma, k = parse_arguments(argv)
    sift = SIFT(sigma, k)
    img = cv2.imread(argv[1], 0)
    t = time()
    pyramid = sift.build_pyramid(img)
    octaves = sift.build_octaves(pyramid)
    DoGs = sift.build_DoGs(octaves)
    sift.precompute_params(DoGs)
    print('every thing before extrema: {:.2f}'.format(time() - t))
    t = time()
    extrema = sift.compute_extrema(DoGs)
    print('extrema: {:.2f}s'.format(time() - t))
    t = time()
    extrema1 = sift.remove_low_contrast(DoGs, extrema)
    print('low contrast: {:.2f}s'.format(time() - t))
    t = time()
    extrema2 = sift.remove_curvature(DoGs, extrema1)
    print('curvatures: {:.2f}s'.format(time() - t))
    t = time()
    keypoints = sift.get_keypoints(extrema2)
    print('key_points: {:.2f}s'.format(time() - t))
    t = time()
    descriptors = sift.get_descriptors(keypoints)
    print('descriptors: {:.2f}s'.format(time() - t))
    for i in range (sift.octaveLvl):
<<<<<<< HEAD
      print(descriptors[i].shape)
=======
        print(descriptors[i].shape)

>>>>>>> a4fa68e3a27ff5228d175ce9e91246ecc7a016f9
if __name__ == "__main__" :
    test(sys.argv[:])

