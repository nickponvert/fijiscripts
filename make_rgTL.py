import ij
from ij import IJ
import os
from ij import ImagePlus
from ij import ImageStack
from ij.plugin import RGBStackMerge
from ij.plugin import RGBStackConverter
from ij.io import FileSaver

'''This script will take a directory of files containing alphabetical section names followed by _TL, _G, and _R for light, GFP, and tdTomato images. The end result will be a stack of composite images, with all three channels merged for each section

This is a jython script, and is intended to be used by fiji
'''

class Stack(ImageStack):
    def __init__(self, title, imp):
            ImageStack.__init__(self, imp.width, imp.height)
            self.title = title
            self.addSlice(imp.title, imp.getProcessor())

    def __add__(self, imp):
            if imp.width == self.width and imp.height == self.height:
                    self.addSlice(imp.title, imp.getProcessor())
            else:
                    print "image", imp.title, "has different dimensions. Ignoring."
            return self

    def show(self):
            ImagePlus(self.title, self).show()

path='/home/nick/Desktop/041715_HTR2A1B11LT/Export/5'
analysisPath='/home/nick/Desktop/041715_HTR2A1B11LT/Analysis/'

filenames=os.listdir(path)
sortedFilenames=sorted(filenames)

#Make an iterator from the sorted list, then zip it three items at a time into a new list that we can take items from
itfn=iter(sortedFilenames)
zippedFn=zip(itfn, itfn, itfn)

stack=None

for i in range(1, len(zippedFn)):
    # for i in [1]:
    fnGroup=zippedFn[i]


    gFn=os.path.join(path, fnGroup[0])
    rFn=os.path.join(path, fnGroup[1])
    tlFn=os.path.join(path, fnGroup[2])

    imGreen=IJ.openImage(gFn)
    imRed=IJ.openImage(rFn)
    imTL=IJ.openImage(tlFn)

    # imGreen.show()
    # imRed.show()
    # imTL.show()

    # stack=ij.ImageStack(imRed.width, imRed.height)

    # stack.addSlice("red", imRed.getProcessor())
    # stack.addSlice("green", imGreen.getProcessor())
    # stack.addSlice("tl", imTL.getProcessor())

    # imstack=ij.ImagePlus("Stack", stack)

    imMerge=RGBStackMerge.mergeChannels([imRed, imGreen, None, imTL], True)

    #The merged image is a composite with three seperate channels. For now, we just want to convert the thing to RGB and save it out. 

    RGBStackConverter.convertToRGB(imMerge)

    saveFn=os.path.join(analysisPath, tlFn[-9:-7], 'Merge.jpg'
    #imMerge.show()

    if stack==None:
        stack=Stack("MergedChannels", imMerge)
    else:fiji
        stack+=imMerge
    
    FileSaver(imMerge).saveAsJpeg(saveFn)

stack.show()


