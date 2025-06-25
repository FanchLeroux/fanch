# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 20:57:53 2024

@author: fleroux
"""

import matplotlib.pyplot as plt
#import numpy as np

import matplotlib.animation as animation

def make_gif(path, data, interval=200, repeat_delay=1000):

    fig, ax = plt.subplots()
    
    # ims is a list of lists, each row is a list of artists to draw in the
    # current frame; here we are just animating one artist, the image, in
    # each frame
    ims = []
    for i in range(data.shape[2]):
        im = ax.imshow(data[:,:,i], vmax = data.max())
        if i == 0:
            ax.imshow(data[:,:,i], vmax = data.max())
        ims.append([im])
        
    
    # ax.set_title('2pi rad RMS')
    
    ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True,
                                    repeat_delay=repeat_delay)

# To save the animation, use e.g.
#
    ani.save(path)