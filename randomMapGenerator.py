from PIL import Image
import argparse
import random




args = argparse.ArgumentParser(description='receives slider Value from humpTool.py')
args.add_argument('--perVal', dest='percentageValue', type=int)
args.add_argument('--mapFile', dest = 'savedMapFile')
parser = args.parse_args()



def mapGenerator(sliderValue = 99):
    """this function generates the noise map using the python PIL library
    it takes one argument *noisePercentage and uses it to calculate how dense
    the noise map is.
    """


    width = 1000
    height = 1000
    pixelCordList = []

    #Creates an image object and grants access to its pixels
    image = Image.new('RGB',(width, height), 'black')
    pixels = image.load()

    #Loop through every pixel of image and set it to black based on the
    #Noise percentage value provided

    for wPixel in range(width ):
        for hPixel in range(height ):
            pixelList = [wPixel,hPixel]
            pixelCords = tuple(pixelList)
            pixelCordList.append(pixelCords)


    #the changedPixel count stores the number of pixels to be influenced based on
    #the slider Value. it takes the slider Value, uses it as a percentage and gets the
    #percentage number of the pixels to be affected

    changedPixelCount = int((float(sliderValue)/ 100) * float(len(pixelCordList)))
    randomPixelCount = len(range(changedPixelCount))

    #select number of pixels based on the changedPixelCount and assign black to them
    randomList = random.sample(pixelCordList, randomPixelCount)

    #set random Pixels to color black
    for randPixels in randomList:
        pixels[randPixels] = (255,255,255)

    # image.show()

    image.save(parser.savedMapFile)


mapGenerator(parser.percentageValue)

