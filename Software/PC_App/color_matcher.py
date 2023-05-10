import cv2
import matplotlib.pyplot as plt
from typing import Dict, Tuple, Type

class ColorImage:    
    def __init__(self, path) -> None:
        self.img = cv2.imread(path)

    ########### Public methods ##########
    def matchResolutions(imgA, imgB) -> None:
        """ Resize both images to a standard resolution preserving the Aspect 
            ratio of imgB
             
            @param imgA: ColorImage - Instance of ColorImage
            @param imgB: ColorImage - Instance of Color Image
        """
        STANDARD_WIDTH = 60
        ASPECT_RATIO = (imgB.img.shape[0]/imgB.img.shape[1])
        RES = (STANDARD_WIDTH, int(STANDARD_WIDTH*ASPECT_RATIO))
        imgA.img = cv2.resize(imgA.img, RES)
        imgB.img = cv2.resize(imgB.img, RES)
        return

    def preprocess(self) -> None:
        """" Preprocess image taken from a camera to better match its 
             reference unnoised counterpart """
        self.__CLAHE()
        self.__setContrast(1.25)
        self.__darken(gain=0.5, cutoff=50)
        return

    def compareColors(self, ref_img) -> float:
        """ Compare color content of two ColorImages
        @param ref_img: ColorImage - Image against which to compare
        @return wIoU: float - Weighted Intersection over Union metric
        """
        dict_s = self.getColors()
        dict_r = ref_img.getColors()
        return self.__weightedIoU(dict_s, dict_r)

    def getColors(self) -> Dict[str, int]:
        """ Get the main colors of the current ColorImage
        @return color_hist: Color Histogram with pixel frequency\
                for each color defined in self.__colors
        """
        color_hist = {key: 0 for key in self.__colors.values()}

        for pixel_row in self.img:
            for (b,g,r) in pixel_row:
                pixel_rgb = (r,g,b)
                cname = self.__closestColor(pixel_rgb)
                if self.__is_pixelGrayScale(pixel_rgb):
                    # Dont take any gray scale pixel into account
                    continue
                else:
                    color_hist[cname] += 1
        return color_hist
        
    
    ########## Private methods ##########
    def __CLAHE(self, Limit=2.0) -> None:
        """ Contrast-Limited Adaptive Histogram Equalization (CLAHE) Algorithm.
        This helps to enhance features of the image by stretching the histogram
        across the entire color space """

        # converting to LAB color space
        lab = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)
        (l_channel, a, b) = cv2.split(lab)
        # Applying CLAHE to L-channel
        clahe = cv2.createCLAHE(clipLimit=Limit, tileGridSize=(4,4))
        cl = clahe.apply(l_channel)
        # merge the CLAHE enhanced L-channel with the a and b channel
        limg = cv2.merge((cl,a,b))
        # Converting image from LAB Color model to BGR color spcae
        self.img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return

    def __setContrast(self, contrast: float) -> None:
        """ Changes image contrast to value specified """
        self.img = cv2.convertScaleAbs(self.img, alpha=contrast)
        return

    def __setBrightness(self, brightness: int) -> None:
        """ Changes image brightness to value specified """
        self.img = cv2.convertScaleAbs(self.img, beta=brightness)
        return

    def __darken(self, gain: float, cutoff: int) -> None:
        """ Darkens all colors under cutoff by downscaling pixel\
            brightness through the gain parameter
        @param gain: float - Gain from 0 to 1 to downscale brightness
        @param cutoff: int - Cutoff threshold intensity from which to\
                             begin downscaling
        """
        for pixel_row in self.img:
            for pixel in pixel_row:
                if (pixel[0] < cutoff) and (pixel[1] < cutoff) and (pixel[2] < cutoff):
                    pixel[0] = int(pixel[0] * gain)
                    pixel[1] = int(pixel[1] * gain)
                    pixel[2] = int(pixel[2] * gain)
        return

    def __closestColor(self, pixel_rgb: Tuple[int, int, int]) -> str:
        """ Returns the closest color defined in self.__colors based
            on given rgb value"""
        differences = {}
        for (r,g,b), color_name in self.__colors.items():
            if self.__is_pixelGrayScale(pixel_rgb):
                return 'gray'
            else:
                differences[sum([(r - pixel_rgb[0]) ** 2,
                                 (g - pixel_rgb[1]) ** 2,
                                 (b - pixel_rgb[2]) ** 2])] = color_name
        return differences[min(differences.keys())]

    def __is_pixelGrayScale(self, pixel_rgb: Tuple[int, int, int]) -> bool:
        """ Returns whether or not a given pixel belongs to the grayscale\
            family"""
        max_deviation = 10
        return (max(pixel_rgb) - min(pixel_rgb)) < max_deviation

    def __weightedIoU(self, hist1: Dict[str, Tuple], hist2: Dict[str, Tuple]) -> float:
        normHist1 = {k: v/max(hist1.values()) for (k,v) in hist1.items() if v != 0}
        normHist2 = {k: v/max(hist2.values()) for (k,v) in hist2.items() if v != 0}

        # Calculate the intersection between the two sets
        intersection = normHist1.keys() & normHist2.keys()
        intersection_sum = sum([normHist1[i] + normHist2[i] for i in intersection])

        # Calculate the symmetric difference
        sym_diff = {k: normHist1[k] if k in normHist1 else normHist2[k] 
                    for k in set(normHist1.keys()).symmetric_difference(normHist2.keys())}
        
        # Union is intersection + symmetric difference
        union_sum = intersection_sum + sum(sym_diff.values())

        return (intersection_sum/union_sum)

    ########## Private variables ##########
    __colors = {
        (0, 0, 255): 'blue',
        (150, 75, 0): 'brown',
        (0, 255, 0): 'green',
        (173, 216, 230): 'light blue',
        (0, 0, 128): 'navy blue',
        (255, 165, 0): 'orange',
        (255, 192, 203): 'pink',
        (128, 0, 128): 'purple',
        (255, 0, 0): 'red',
        (0, 128, 128): 'teal',
        (143, 0, 255): 'violet',
        (255, 255, 0): 'yellow'
    }
# END OF CLASS ColorImage
