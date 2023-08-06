# Project: pyql700

## Module: stripes


 Uses **imagemagick** now for short texts,

 ` ./stripes.py textline 62 "Toto je text" `

 when print is needed directly:

 ` ./stripes.py textline 62 "Toto je text" -p `


 Prints an image file:
 ` ./stripes.py print_it 62 imagefile `


 Games with an image file - prototype for dither/pattern:
 ` ./stripes.py image 62 imagefile `


## Module multextimg

 Based on PIL and uses
  - WIDTH
  - maxchars_per_line,
it creates multiline text image with exact HEIGHT dimension. Prototype now.

`./image_ut.py mk  640 "Mnohokrát děkuji."  60
`
