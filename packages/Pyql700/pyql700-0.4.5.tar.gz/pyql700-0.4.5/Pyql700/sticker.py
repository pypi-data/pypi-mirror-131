#!/usr/bin/env python3
# -fire CLI
from fire import Fire
from version import __version__

import subprocess as sp

import math
from PIL import Image, ImageDraw, ImageFont



from multextimg import create_image_multiline, print_tiv_image, print_tiv_file

import tempfile

import sys








print("i... module pyql700/stripes is being run")




#======================================================
#      CALLED FROM BINFILE
#
#def mult(S62, text, p=False):
# width I know it must be 707 and -10 +paste on 707
#def mult( S62, text, p=False, qr=False, qd=False):
def txt( S62, text, p=False, qr=False, image=None, qd=False, cover=0.7):
    """
    62 "some text\nmultiline" --qr (qr is autocreated)
    """
    # print("D... -p=", p, type(p) )
    if type(p)!=bool:
        print("X... some problem with -p")
        sys.exit(1)
    #print("D... ",S62,text,"print=",p,qr,qd)
    OUTNAME = "just_print707.jpg"

    qrminimy = 120 # minimal height for QR
    #S62=62
    if S62!=62:
        print("X... problem - only 62")
        sys.exit(1)
    # cover = 1.0
    xposition = "center"
    if (qr) or not (image is None):
        #---------- put text LEFT--------
        #cover = 0.7 # compress text
        xposition = "left"
        #text=text+"\n\n." # add empty line
    elif qd:
        text=text+"\n _" # add empty line
        text=text+"\n _" # add empty line
    else:
        cover = 1.0

    timg,qrimg = create_image_multiline(707, 40, text, cover=cover, xposition=xposition)
    print("D... IMAGE====",image)
    if not (image is None):
        #qrimg = img( S62, image , p=False)
        qrimg = Image.open(image)

    print("D... QRIMG LOADED, TIMG printed")
    print_tiv_image(timg)

    if (qr) or not (image is None):
        print("D... QRIMG LOADED, QRIMG/IMAGE printed")
        print_tiv_image(qrimg)

    if (qr) or not (image is None):
        print("D... attaching T right ", timg.size)
        print("D... attaching QR right", qrimg.size)

        if timg.size[1]<qrminimy: # I dont want smaller heigth than 120...
            print("D... TOO SMALL HEIGHT")
            nimage = Image.new('RGB', (timg.size[0], 120), (255,255,255))
            nimage.paste(timg,(0,0) )
            timg = nimage

        if timg.size[1]<qrimg.size[1]: # height problem, QR is higher
            print("D... QR/IMAGE have TOO BIG HEIGHT down with qrimg ... height",
                  timg.size,
                  qrimg.size
                  )
            #qrimg = qrimg.resize( (qrimg.size[0], img.size[1]) ) # placaty
            if qr:
                qrimg = qrimg.resize( (timg.size[1], timg.size[1]) )
            else:
                print("D... resizing down --image TO", ( int(qrimg.size[0]/qrimg.size[1]* timg.size[1]), timg.size[1]) )
                qrimg = qrimg.resize( ( int(qrimg.size[0]/qrimg.size[1]* timg.size[1]), timg.size[1]) )
                print("D... NEW qrimg --image  SIZE",qrimg.size)
            print("D... QRIMG CORRECT SIZE????")
            print_tiv_image(qrimg)


        if (1-cover)*timg.size[0] < qrimg.size[0]: # width problem, QR too wide
            allow_w = int( (1-cover)*timg.size[0] )
            print("D... qrimg TOO WIDE -down with qrimg ... allowed width=",
                  allow_w)
            if qr:
                qrimg.resize( (allow_w,allow_w ) )
            else:
                print("D... downscaling the WIDTH of qrimg --image alone",qrimg.size[1] )
                temp_h = qrimg.size[0]
                temp_w = qrimg.size[1]
                qrimg = qrimg.resize( (  allow_w , temp_w ) )
            # qrimg = qrimg.resize( (w,w ) )

            print("D... QRIMG CORRECT SIZE????", qrimg.size )
            print_tiv_image(qrimg)



        # img.paste(qrimg,( int(img.size[0]/2),0)) # paste right - stupid center
        timg.paste(qrimg,( timg.size[0] - qrimg.size[0] - 10,0)) # paste right
        print("D... QRIMG pasted on timg; final TIMG printed")
        print_tiv_image(timg)
        # img.save("z_finale.png")
        timg.save( OUTNAME )
    elif qd:
        print("D... attaching qr down")
    print_image( S62, timg , p)









def func():
    print("D... function defined in pyql700:stripes")
    return True

def test_func():
    print("D... test function ... run pytest")
    assert func()==True






#======================================================
#
# need to create 707 and paste 707-10
#
def print_file( media62 , jpgfile, p=False):
    """
    print JPG file with LPR. Core for the  printing. CREATE 707-10. Paste
    """
    print("D... printfile - open image")
    im = Image.open( jpgfile )
    print_image(media62, im, p)



def print_image( media62 , im, p=False):
    """
    print PIL Image. Anyway, saves to disk to LPR
    """
    prnname="just_print707.jpg" # temporaryname
    WIDTH, HEIGHT = im.size
    print("D... old size: w x h", WIDTH, HEIGHT)
    HEIGHT=int(HEIGHT*707/WIDTH)+10+10
    WIDTH=707
    print("D... new size w x h:", WIDTH, HEIGHT)
    imgnew = Image.new('RGB', (WIDTH, HEIGHT ), color = (255,255,255) )
    #imgnew.paste( im, (10,10)  ) #--------THIS I KNOW FROM TESTS
    # seems ok
    print("D... pasting old to new")
    imgnew.paste( im, (10,10)  ) #--------THIS I KNOW FROM TESTS
    print("D... SAVING", prnname )
    imgnew.save( prnname )

    # HERE I decide if to use CUPS or  pip3 brother_ql

    NAME=get_printer_name()

    if NAME is None:
        CMD = "brother_ql -b linux_kernel -p /dev/usb/lp0  -m QL-700 print -l 62 "+prnname
    else:

        CMD="lpr  -o page-left=3 -o page-right=3 -o page-top=0 -o page-bottom=0  -o media="+str(int(media62))+"X1  -o BrCutAtEnd=OFF  -o BrCutLable=0 -o BrTrimtape=ON -o BrPriority=BrQuality  -o  orientation-requested=3  -P "+NAME+" "+prnname


    print( "P...",CMD )
    if p:
        try:
            res=sp.check_output( CMD.split() ).decode("utf8")
            #res=False #sp.check_output( CMD.split() ).decode("utf8")
        except:
            res="!... Probably not installed. Printer name=/"+NAME+"/"
        print(res)
    return










#======================================================

def textline( amedia, text , p=False ):
    """
    say 62 text ; text is created  horizontally
    """
    print("i... amedia == 62" )
    media=amedia/10  # float  MM to  CM

    OUTPUT="z_output.png"
    OUTPUT="just_print707.jpg"
    CMD="convert -background white  -fill black  -font Gecko -pointsize 32          -size x120  label:'"+text+"' "+OUTPUT

    CMD="convert -background white  -fill black  -font Gecko -pointsize 32          -size x120".split()
    CMD.append("label:"+text)
    CMD.append(OUTPUT)
    print( "i...",CMD )
    res=sp.check_output( CMD ).decode("utf8")
    print(res)
    if p:
        print_file( amedia, OUTPUT )



def get_printer_name():
    """
    use lptstat to find the printer name QL700
    """
    CMD="lpstat -a"
    prnname=""
    print( "i...",CMD )
    ok = False
    try:
        res=sp.check_output( CMD.split() ).decode("utf8")
        ok = True
    # except CalledProcessError:
    except Exception as ex:
        print("!... exception - probably no printer installed\n",ex)
    if not ok:
        return None
    a=res.split("\n")
    for i in a:
        if i.find("QL")>=0:
            prnname=i.split()[0]
    print("i... Printer name==", prnname)
    return prnname

#======================================================

#def image( amedia, pic , p=False):
def img( amedia, pic , p=False):
    """
      62 picname.jpg  # picture is printed
    """
    if type(p)!=bool:
        print("X... some problem with -p")
        sys.exit(1)
    if amedia!=62:
        print("X... i know only 62")
        sys.exit(1)
    print("i... amedia == 62" )
    media=amedia/10  # float  MM to  CM
    #inputfile=args.inputpic

    inputfile=pic

    width=0
    width=int(300/2.56*media)
    #
    #===============
    #
    width=707-10
    #
    # this will make 10 border
    if media==6.2:
        print("6.2")
    elif media==2.9:
        print("2.9")
    else:
        print("x... not known media!", amedia)
        sys.exit(1)
    #========== IMAGE CREATE
    #OUTPUT="z_output.png"

    # ERROR ========= OUTPUT=pic
    OUTPUT = "/tmp/ql700_"+next(tempfile._get_candidate_names())+".png"

    #
    CMD="convert "+inputfile+" -auto-level  -scale "+str(width)+"x   -monochrome -dither FloydSteinberg  -remap pattern:gray50  "+OUTPUT


    CMD="-auto-level  -scale "+str(width)+"x   -monochrome -dither FloydSteinberg  -remap pattern:gray50  "+OUTPUT

    CMD = CMD.split()
    CMD.insert(0,inputfile)
    CMD.insert(0,'convert')

 #   CMD="convert "+inputfile+" -auto-level  -scale x"+str(width)+" -colorspace gray -ordered-dither o8x8 "+OUTPUT
 #   CMD="convert "+inputfile+" -auto-level  -scale x"+str(width)+" -colorspace gray -ordered-dither o8x8 "+OUTPUT
#    CMD="convert "+inputfile+" -auto-level  -scale x"+str(width)+" -colorspace gray -remap pattern:gray50 "+OUTPUT

    #
    print( "i...",CMD )
    res=sp.check_output( CMD ).decode("utf8")
    print("r...",res)
    #
    # TEXT
    #    CMD="convert -size x"+str(width)+" -background white  -pointsize 16 -font Courier -fill black -gravity NorthWest caption:"`cat PASKY.txt`"   -flatten  z_output.png"
    #

    print(OUTPUT)

    print_tiv_file(OUTPUT)
    print_file( amedia,  OUTPUT , p )
    return OUTPUT

#======================================================



#
# formerly I created a picture and then I reduced it and pasted
# to a new one.
#
# Now I want to set the tape width and 'variable' length
#
class Ql700Label(object):
    def __init__(self, tapewidth, tapelength=0 ):
        print("i... init")
        self.tapewidth= tapewidth # 62 (x29) OR 2.3 (x1.1),
        self.set_output()


#======================================================

def stripes( to=10, le=10, bo=10, ri=0, wi=707, p=False):
    """
    print/create stripes - test the borders and width
    """
    print("!... 62 can do width 707:300dpi (double is 1414 too much)....!")
    print("!... top,left,bottom,right = 10,10,10,0 .with  -o pl=3 pr=3...!")
    print("!... PIC SIZE= 697 x Height-20" )
    w, h = 640, 480
    w, h = 320,240
    w, h = 160,30
    left,top=20,10

    h=int(h/w*wi)
    fontsize = 12  # starting font size
    fontsize=int(fontsize/w*wi)
    #=================rewrite hard with parameters
    left=le
    top=to
    bottom=bo
    right=ri
    w=wi
    # creating new Image object
    img = Image.new("RGB", (w, h), (255,255,255))

    # create line image
    img1 = ImageDraw.Draw(img)
    FONTNAME='/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'
    font = ImageFont.truetype(FONTNAME, fontsize)
    img1.text( (left,top),   "{}x{}+l{}+t{}-b{}-r{}".format(w,h,
                                                        le,top,
                                                        bottom,right) ,
               font=font, fill="#000000" )

    for i in range(left,w):
        if i%5==0:
            shape = [(i, top), (i , top+h)]
            img1.line(shape, fill ="black", width = 0)
    #img.show()

    #left top bottom right
    #rovna
    shape= [(le, int(top+h/2)  ), (w , int(top+h/2))]
    img1.line(shape, fill ="black", width = 0)
    #dolu
    shape= [(le, int(top+h/2)), (w , int(top+h-bottom))]
    img1.line(shape, fill ="black", width = 0)
    #nahoru
    shape= [(le, int(top+h/2)), (w , int(top))]
    img1.line(shape, fill ="black", width = 0)


    OUTFILE="out.jpg"
    img.save(OUTFILE)
    print("D... print:", OUTFILE)
    if p:
        print_file( 62, OUTFILE)
    else:
        img.show()


#======================================================


#======================================================



#======================================================


if __name__=="__main__":
    print("D... in main of project/module:  pyql700/stripes ")
    print("D... version :", __version__ )
    Fire( {'image':image,
           'file':print_file,
           'textline':textline,
           'stripes':stripes,
           'mult':mult,
           'name':get_printer_name
    })
