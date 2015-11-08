#!env python
# enhance detail in images by L0 gradient minimization.
# NOTE: "Edge Adjustment" (Eq.(15)) is not incorporated. blurrey edges may cause artifacts.
import numpy as np
import matplotlib.pyplot as plt

from l0_gradient_minimization import l0_gradient_minimization_2d
from demo_util import *

def enhance_detail_demo():
    def add_arguments(parser):
        parser.add_argument('--enhancement', default=1.5, type=float,
                help='detail enhancement strength (>1.0)')

    img, (lmd, beta_max, beta_rate), args = get_configuration(add_arguments)
    img_base = l0_gradient_minimization_2d(img, lmd, beta_max, beta_rate)
    img_diff = img - img_base
    img_enhance = clip_img(img_base + img_diff*args.enhancement)

    fig, axs = plt.subplots(1, 3, figsize=(12, 6))
    fig.suptitle((r'Detail Enhancement Demo by $L_0$ Gradient Minimization. power={:.2}' + '\n'
        + r'$\lambda={:.3}, \beta_{{max}}={:.2e}, \kappa={:.3f}$').format(args.enhancement, lmd, beta_max, beta_rate),
        fontsize=16)
    axs[0].imshow(img)
    axs[0].set_title('original')
    axs[1].imshow(clip_img(img_base))
    axs[1].set_title('S: $L_0$ minimization')
    axs[2].imshow(clip_img(img_enhance))
    axs[2].set_title('Enhanced')
    fig.tight_layout()
    fig.subplots_adjust(top=0.8)

if __name__=='__main__':
    enhance_detail_demo()
    plt.show()
