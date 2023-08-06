#!/usr/bin/env python3
"""
This is one of two or three modules that contain function to
support brother print
"""
#  FOR COLORS:  pip3 install ansicolors



import textwrap
import subprocess as sp

from PIL import Image, ImageDraw, ImageFont

from fire import Fire
import os


import qrcode
from pyql700 import imrenderer, sticker

import numpy as np
# print("________________________________")

# print("""
# ./multextimg.py mk 640 9 'Žluťoučký kůň úpěl ďábelské ódy.'
# ./multextimg.py mk 640 20 'Žluťoučký
# kůň
# úpěl
# ďábelské
# ódy.'
# """)
# print("________________________________")


def print_tiv_file(pic):
    """
    simple tiv in python : imrenderer : file
    """
    imrenderer.render(pic)
    return


def print_tiv_image(img):
    """
    simple tiv in python : imrenderer : PIL img

    """
    # print("D... trying to render PIL image, convert to numpy", img)
    imrenderer.image_render( np.array(img) )
    return

    # rows, columns = os.popen('stty size', 'r').read().split()
    # tivsize = int(columns)
    # if tivsize <= 1:
    #     tivsize = 2
    # print("D... terminal", rows, columns, tivsize)

    # ok = False
    # try:
    #     res = sp.check_call("which tiv".split())
    #     ok = True
    # except: # pylint: disable=W0702
    #     ok = False
    # if not ok:
    #     print("D... tiv NOT present, do pip3 install tiv")
    #     # print("i... https://github.com/stefanhaustein/TerminalImageViewer")
    #     # pip3 install tiv
    #     return False
    # print("D... tiv present", res)
    # sp.check_call(("tiv -w "+str(tivsize)+" "+pic).split())
    return True


def wraptext(txt="ahoj", nchars=40):
    """
    returns multiline string, max char per line==n
    """
    #    return "\n".join(textwrap.fill(txt, width=n))
    # print("i... prewrap=", txt )
    byline = txt.split("\n")
    final = ""
    j = 0
    for i in byline:
        j += 1
        # print("D...LINE {:2d}/{:2d}==================".format(j,len(byline)) )
        res = "\n".join(textwrap.wrap(i, width=nchars))
        # print("DW... i=",res)
        final += res+"\n"
    # print("i... wrapfinal=",final)
    return final.rstrip()






def deduce_font_size(imgx=640, txt="Ahoj, jak se mas", cover=1.00,
                     fontname='/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'):
    """
    Deduces best font size for ONE textline
    """
    # print("D... deduce font size:________________________________")
    # print("... ", len(txt) )
    if len(txt) == 0:
        txt = "AHOJ"
    # print("... ", len(txt) )
    # txt = "Hello World"
    # FONTNAME="/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf"
    fontsize = 1  # starting font size

    # portion of image width you want text width to be
    img_fraction = cover

    remains = 0

    font = ImageFont.truetype(fontname, fontsize)
    # while font.getsize(txt)[0] < img_fraction*img.size[0]:
    while font.getsize(txt)[0] < img_fraction*imgx:
        # calulate what remains blank
        # remains= img_fraction*img.size[0]-font.getsize(txt)[0]
        remains = img_fraction*imgx-font.getsize(txt)[0]
        # print("D... remains",remains,
        # "     font.getsize(txt)[0]=",font.getsize(txt)[0])
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(fontname, fontsize)
        print(" ... ... fontsize:", fontsize, end="\r")
        if fontsize > 100:
            break

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    if fontsize>20: # f36 total -3 fantastic     f48 -3 in total OK
        fontsize -= 1
    if fontsize>40: # f83 -3 in total works
        fontsize -= 1
    font = ImageFont.truetype(fontname, fontsize)

    print('i... final font size', fontsize)
    # print( 'i... remains blank', remains) #GOOD INFO
    # dx=int(remains/2)+int(  (1-cover)*img.size[0]/2  ) # justified on center
    dx = int(remains/2)+int((1-cover)*imgx/2)# justified on center


    return fontsize, dx, font.getsize(txt)[1]




def deduce_remains_blank(fontsize, imgx=640, txt="Ahoj, jak se mas",
                         cover=1.00,
                         fontname='/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'):
    """
    Checks borders for One line text
    """
    # portion of image width you want text width to be
    img_fraction = cover
    remains = 0
    font = ImageFont.truetype(fontname, fontsize)
    # calulate what remains blank
    # remains= img_fraction*img.size[0]-font.getsize(txt)[0]
    remains = img_fraction*imgx-font.getsize(txt)[0]
    # print( 'i... X=',img_fraction*imgx,
    #  "FontSize=",fontsize,"  TextWidth",font.getsize(txt)[0],
    #  'remains blank', remains)
    dx = int(remains/2)+int((1-cover)*imgx/2)# justified on center
    return dx




def deduce_height(text, smallest, fontname):
    """
    get text, deduce its height
    """
    print("D... deduce height:________________________________")
    # Determine text size using a scratch image.
    nlines = len(text.split("\n"))
    print("D... lines=", nlines)
    img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontname, smallest)
    textsize = draw.textsize(text, font)
    return int(textsize[1]/nlines*1.06)*nlines





def deduce_fontsize2(width, text, wrapchar, cover=1.0,
                     limit=30):
    # ============= get fontsize =========================
    """
    for each textline looks for best font, checks blank-x
    returns fontsize,dx-start,ysizetot-useless
    """
    print("D... deduce font size 2:________________________________")
    smallest = -1
    dx = 0
    ysizetot = 0
    j = 0
    for i in wraptext(text, wrapchar).split("\n"):
        j += 1
        print("i... line {}/{}".format(j, len(wraptext(text, wrapchar).split("\n"))))
        fsize, dx, ysize = deduce_font_size(width, i, cover=cover)
        ysizetot += ysize
        if smallest == -1:
            smallest = fsize
        elif fsize < smallest:
            smallest = fsize

    if smallest > limit:
        smallest = limit
    print("D... recommended smallest fontsize={}".format(smallest),
          " ysize=", ysizetot)

    dxmin = -1
    for i in wraptext(text, wrapchar).split("\n"):
        # print("rem...",i)
        dx = deduce_remains_blank(smallest, width, i, cover=cover)
        if dxmin == -1:
            dxmin = dx
        elif dxmin > dx:
            dxmin = dx
    print("i... minimal found dx=", dxmin)
    return smallest, dxmin, ysizetot





#################################################
#           BEST THING HERE - CENTER OF ALL
#

def create_image_multiline(width, wrapchar, text, cover=1.0, xposition="center",
                           fontname='/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf',
                           limit=140):
    """
    Creates Image from the TEXT given inline, returns real image
    """
    #
    # version None to determine automat (1-40)
    # correction L(7%) H(30%)
    #
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    qrimg = qr.make_image()

    smallest, dx, ysizetot = deduce_fontsize2(width, text, wrapchar, cover=cover, limit=limit)

    #if smallest>10:
    #smallest=10 # really tiny
    #smallest=20 # possible to see well, but can be bigger
    #============ get height ======================
    # nlines=len( wraptext(text, wrapchar).split("\n") )
    # HEIGHT=ysizetot
    # print("i... height multiline         =", HEIGHT , "with",nlines,"lines")
    height = deduce_height(wraptext(text, wrapchar), smallest, fontname)
    # print("i... height from scratch image=", HEIght , "with",nlines,"lines")

    # ===============action===============================
    print("i... creating image", width, "x", height)
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontname, smallest)
    if xposition=="left": # prepare for qw position right
        dx=0
    draw.text((dx, 0), wraptext(text, wrapchar), font=font, fill="#000000")
    outfile = "z_output.png"
    qroutfile = "z_outputqr.png"

    outfile = "just_print707.jpg"
    qroutfile = "just_print707qr.jpg"
    print("")
    img.save(outfile)
    qrimg.save(qroutfile)
    print_tiv_file(qroutfile)
    print_tiv_file(outfile)
    return img, qrimg #
    return outfile



def qr(text, p=False):
    '''
qr sometext -p   ...  makes qrcode and prints it
    '''
    #
    # version None to determine automat (1-40)
    # correction L(7%) H(30%)
    #
    qroutfile = "z_outputqr.png"
    S62=62

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    qrimg = qr.make_image()

    qrimg.save(qroutfile)
    print_tiv_file(qroutfile)
    if p:
        sticker.print_image( S62, qrimg )
    return


if __name__ == "__main__":

    Fire({"mk":create_image_multiline})
    # quit()
    # wrapchar2 = 45 # Characters
    # width2 = 640
    # text2 = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    # cover2 = 1 # full image width
    # fontname2 = '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'

    # create_image_multiline(width2, text2, wrapchar=55)
