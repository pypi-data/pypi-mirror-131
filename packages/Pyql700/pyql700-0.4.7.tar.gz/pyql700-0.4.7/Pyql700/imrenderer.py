#!/usr/bin/env python3

#  FOR COLORS:  pip3 install ansicolors

# https://raw.githubusercontent.com/djentleman/imgrender/master/imgrender/main.py
print("D... pip3 install ansicolors")
from colors import color
from PIL import Image
import numpy as np
import argparse

from fire import Fire
import os


class Renderer():

    def get_pixel(self, col):
        return color('  ', bg=f'rgb({int(col[0])}, {int(col[1])}, {int(col[2])})')

    def render_image(self, pixels, scale):
        # first of all scale the image to the scale 'tuple'

        # JM
        image_size = pixels.shape[:2]

        if isinstance(scale,int):
            scale= ( int(scale/image_size[1]*image_size[0]),scale)

        print("D...    imagesize ", image_size)
        print("D...    imagesize2", scale)
        rows, columns = os.popen('stty size', 'r').read().split()

        #  adapt to imrenderer....
        rows, columns = int(rows)-1, int((int(columns)-1)/2) # I MUST DIVIDE TERMINAL WIDTH BY 2; TIV was OK /1
        tivsize = columns
        if tivsize <= 1:
            tivsize = 2
        print("D...    terminal", rows, columns, " tiv -w",tivsize)


        if (scale[0]>rows) or (scale[1]>columns) or (scale[0]==0) or (scale[1]==0):

            scale1= ( int(columns/image_size[1]*image_size[0]), columns)

            scale2= ( rows, int(rows/image_size[0]*image_size[1]))
            print("D...    compeeting sizes:",scale1,scale2)
            if scale1[0]>scale2[0]:
                scale=scale2
            else:
                scale=scale1

            #scale=(rows,columns)

        print("D...    imagesize3", scale)

        block_size = (image_size[0]/scale[0], image_size[1]/scale[1])
        blocks = []
        y = 0
        while y < image_size[0]:
            x = 0
            block_col = []
            while x < image_size[1]:
                # get a block, reshape in into an Nx3 matrix and then get average of each column
                block_col.append(pixels[int(y):int(y+block_size[0]), int(x):int(x+block_size[1])].reshape(-1, 3).mean(axis=0))
                x += block_size[1]
            blocks.append(block_col)
            y += block_size[0]
        output = [[self.get_pixel(block) for block in row] for row in blocks]
        return output



def img2numpy(img):
    print("D...    img.shape", img.shape)

    if len(img.shape)==2:
        print("D...    special GRAY/B+W image", type(img[0,0]))
        if isinstance(img[0,0], np.bool_):
            print("D...    Boolean colors: B+W image ")
            npar = np.array([[ [255,255,255] if pixel else [0,0,0] for pixel in row] for row in img])
            #print(npar)
            return npar
        #print(img)
        #npar = np.array([[pixel for pixel in row] for row in img])
        #print(npar)
        return np.array([[ [pixel,pixel,pixel] for pixel in row] for row in img])
    if img.shape[2] > 3:
        return np.array([[pixel[:3] for pixel in row] for row in img])
    return img


def get_image(path):
    img = np.asarray(Image.open(path))
    return img2numpy(img)


def image_render(image, scale=(0, 0)):
    """
    takes image
    """
    renderer = Renderer()
    #image = get_image(path)
    image = img2numpy(image)

    output = renderer.render_image(image, scale)
    print('\n'.join([''.join(row) for row in output]))



def render(path, scale=(0, 0)):
    """
    ORIGINAL PART FROM FILE
    """
    renderer = Renderer()
    image = get_image(path)

    output = renderer.render_image(image, scale)
    print('\n'.join([''.join(row) for row in output]))

if __name__=="__main__":
    Fire()
