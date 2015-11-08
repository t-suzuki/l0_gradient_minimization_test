#!env python
# utilities for demo

import sys
import os
import argparse
import skimage.data
import skimage.transform
import skimage.color
import numpy as np

def clip_img(img):
    return np.clip(img, 0, 1)

def add_noise(img, sigma):
    return  clip_img(img + np.random.randn(*img.shape) * sigma)

def get_configuration(add_arguments_func=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--lambda', default=0.02, type=float,
            help='lambda parameter (larger: preference to smoother images)')
    parser.add_argument('--beta-max', default=1.0e5, type=float,
            help='beta max (larger: accurate result at the cost of complexity)')
    parser.add_argument('--beta-rate', default=2.0, type=float,
            help='beta multiplying rate (smaller: accurate result at the cost of complexity)')
    parser.add_argument('--resize', default=128, type=float,
            help='resize input image to')
    parser.add_argument('file_path', type=str, nargs='?',
            help='input file path (default: lena)')
    if add_arguments_func is not None:
        add_arguments_func(parser)
    args = parser.parse_args()

    if args.file_path is None:
        img_name = 'Lena'
        img = skimage.data.lena()
    else:
        img_name = os.path.basename(args.file_path)
        img = skimage.io.imread(args.file_path)

    # resize
    size = args.resize
    org_h, org_w = img.shape[:2]
    if org_h < org_w:
        w, h = (size, size*org_h/org_w)
    else:
        w, h = (size*org_w/org_h, size)
    print('{}: {}x{} -> {}x{}'.format(img_name, org_w, org_h, w, h))
    img = skimage.transform.resize(img, (h, w))

    # access to commonly used arguments
    lmd = getattr(args, 'lambda')
    beta_max = args.beta_max
    beta_rate = args.beta_rate
    return img, (lmd, beta_max, beta_rate), args

