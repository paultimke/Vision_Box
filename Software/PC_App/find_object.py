""" Find shapes inside an input image """
# Import Libraries
import cv2
from cv2 import *
import numpy as np
import matplotlib.pyplot as plt
import imutils 
import logging
import constants as cnst
from vbox_logger import logger
import crop_screen as cs

LOG_TAG= 'FICON'

def visualize(img, title:str, figure:int):
    """ Use Matplotlib to show image """
    plt.figure(figure)
    plt.title(title) 
    plt.imshow(img, cmap="gray")
    

def template_init(template_path):
    """ Read template image """
    template= cv2.imread(template_path)
    assert template is not None, "File could not be read, check with os.path.exists()"
    return template


def inputIMG_process(input_image: cv2.Mat) -> cv2.Mat:
    """ Binarize input image, find screen contour and crop image,
        then resize to standard MACRO defeined size""" 
    x, y, j = input_image.shape
    croppy = cs.StraightenAndCrop(input_image, x, y)
    cut_x, cut_y, j = croppy.shape

    (xsize, ysize) = cnst.FOBJ_RESIZE_INPUT_STD
    kernel = np.ones((1,1), np.uint8)

    gray_input_image = cv2.cvtColor(croppy, cv2.COLOR_BGR2GRAY)
    img_thresh = cv2.adaptiveThreshold(gray_input_image,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 105, 5)
    img_erode = cv2.dilate(img_thresh, kernel, iterations=15)

    (tH, tW) = img_erode.shape[:2]
    aspect_ratio = tH/tW

    # Resize input image
    cropped_input_image = cv2.resize(img_erode, (xsize, round(xsize*aspect_ratio)))
    return cropped_input_image, cut_x, cut_y


def template_process(template):
    """ Resize template to standard MACRO defined size and apply Canny filter """
    template_size = cnst.FOBJ_RESIZE_TEMP_STD

    (tH, tW) = template.shape[:2]
    aspect_ratio = tH/tW
    cropped_template = cv2.resize(template, (template_size, round(template_size*aspect_ratio))) 
    (tH, tW) = cropped_template.shape[:2]

    template = cv2.Canny(cropped_template, 50, 150)
    return template
    

def matchTemplate(input_img, template):
    """ Iterate input image with different sizes to match with template """
    mt_iterations = cnst.FOBJ_MT_ITERATIONS

    # Template Height and Width
    (tH, tW) = template.shape[:2]

    # Required variables init
    found = None
    foundList = []
    tempList = [0, 0, 0]

    # Loop over the scales of the image
    for scale in np.linspace(0.01, 1.0, mt_iterations)[::-1]:
        # resize the image according to the scale, and keep track of the ratio of the resizing
        resized = imutils.resize(input_img, width = int(input_img.shape[1] * scale))
        relation = input_img.shape[1] / float(resized.shape[1])
        # If Resized image is smaller than template, then break the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break
        # detect edges in the resized, grayscale image and apply template matching to find template in image
        edged = cv2.Canny(resized, 50, 200) 
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        # if we have found a new maximum correlation value, then update bookkeeping variable
        if found is None or maxVal > found[0]:
            tempList = [maxVal,maxLoc,relation]
            foundList.append(tempList)
            found = (maxVal, maxLoc, relation)
    return foundList


def findObjects(foundList, template, display_image, rating_diff):
    """ Iterate in list of matched objetcs and filter by correlation value and position """
    
    found_treshold = cnst.FOBJ_MATCH_THRESHOLD
    acceptance_diff = cnst.FOBJ_ACCEPTANCE_DIFF

    # Template Height and Width
    (tH, tW) = template.shape[:2]

    # Variables init
    startX_T = startY_T = detected_objs = rejected_objects = first_loop = rating = 0
    detected_list = []
    rejected_list = []
    tmp_detected_list = []
    max_correlated_list = []
    max_correlated_values = []
    init_detected_list = []
    detected_temp = [0,0,0,0,0]
    failed_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2BGR)
    display_image = cv2.cvtColor(display_image, cv2.COLOR_GRAY2BGR)
    
    # Loop to find objects
    for i in foundList:
        (startX, startY) = (int(i[1][0] * i[2]), int(i[1][1] * i[2]))
        (endX, endY) = (int((i[1][0] + tW) * i[2]), int((i[1][1] + tH) * i[2]))
        detected_temp = [startX, endX, startY, endY, i[0]]

        if i[0] > (found_treshold * 100000):###
            if (abs(startX-startX_T) > acceptance_diff) and (abs(startY-startY_T) > acceptance_diff) and first_loop != 0:
                tmp_detected_list.append(init_detected_list)
                init_detected_list = []
            first_loop +=1
            init_detected_list.append(detected_temp)
        else:
            rejected_list.append(detected_temp)
            rejected_objects+=1
        startX_T = startX
        startY_T = startY
    tmp_detected_list.append(init_detected_list)

    tmp_max = 0
    for i in tmp_detected_list: #    [ [(),(),(),()] ; [(),()] ]
        if len(i)>1:
            for j in i:
                if j[4]>tmp_max: 
                    tmp_max = j[4]
            max_correlated_list.append(j)
        elif len(i)==1: max_correlated_list.append(i[0])
        else: max_correlated_list.append(i)

    tmp_max=0
    for i in max_correlated_list:
        if len(i)>1:
            if i[4]>tmp_max: max_correlated_values.append(i[4])
            tmp_max = i[4]

    if len(max_correlated_values)!=0:
        for i in max_correlated_list:
            rating = i[4]/(max(max_correlated_values)/100)
            if rating > rating_diff:
                # save result and draw a bounding box around passed image
                cv2.rectangle(display_image, (i[0], i[2]), (i[1], i[3]), (255, 0, 0), 2)
                detected_temp = [i[0], i[1], i[2], i[3], i[4]]
                detected_objs+=1
                detected_list.append(detected_temp)
            else:
                # save result and draw a bounding box around failed image
                cv2.rectangle(failed_image, (i[0], i[2]), (i[1], i[3]), (255, 0, 0), 2)
                detected_temp = [i[0], i[1], i[2], i[3], i[4]]
                rejected_objects+=1
                rejected_list.append(detected_temp)

    return detected_list, detected_objs, display_image, rejected_list, rejected_objects, failed_image

def img_is_color(img):
    """ Helper function for show_image_list. Return if image is colored """
    if len(img.shape) == 3:
        # Check the color channels to see if they're all the same.
        c1, c2, c3 = img[:, : , 0], img[:, :, 1], img[:, :, 2]
        if (c1 == c2).all() and (c2 == c3).all():
            return True
    return False

def show_image_list(list_images, list_titles=None, list_cmaps=None, grid=True, num_cols=2, figsize=(20, 10), title_fontsize=30):
    """ Display images in a single figure """
    assert isinstance(list_images, list)
    assert len(list_images) > 0
    assert isinstance(list_images[0], np.ndarray)
    if list_titles is not None:
        assert isinstance(list_titles, list)
        assert len(list_images) == len(list_titles), '%d imgs != %d titles' % (len(list_images), len(list_titles))
    if list_cmaps is not None:
        assert isinstance(list_cmaps, list)
        assert len(list_images) == len(list_cmaps), '%d imgs != %d cmaps' % (len(list_images), len(list_cmaps))
    num_images  = len(list_images)
    num_cols    = min(num_images, num_cols)
    num_rows    = int(num_images / num_cols) + (1 if num_images % num_cols != 0 else 0)
    # Create a grid of subplots.
    plt.figure(1)
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize)
    # Create list of axes for easy iteration.
    if isinstance(axes, np.ndarray):
        list_axes = list(axes.flat)
    else:
        list_axes = [axes]
    for i in range(num_images):
        img    = list_images[i]
        title  = list_titles[i] if list_titles is not None else 'Image %d' % (i)
        cmap   = list_cmaps[i] if list_cmaps is not None else (None if img_is_color(img) else 'gray')
        
        list_axes[i].imshow(img, cmap=cmap)
        list_axes[i].set_title(title, fontsize=title_fontsize) 
        list_axes[i].grid(grid)
    for i in range(num_images, len(list_axes)):
        list_axes[i].set_visible(False)
    fig.tight_layout()
    #_ = plt.show()


#--------------------------------------MAIN FUNCTION-------------------------------------------#

def mainly(template_path, raw_input_image):  
    rating_diff = 90

    raw_template = template_init(template_path)

    inputIMG, cut_x, cut_y = inputIMG_process(raw_input_image)
    template = template_process(raw_template)  

    foundList = matchTemplate(inputIMG, template)
    detected_list, detected_objs, display_image, rejected_list, rejected_objects, failed_image = findObjects(foundList, template, inputIMG, rating_diff)
    
    #for i in range(0,rejected_objects): ###
        #logger.debug("VB", f"Failed object {i+1} coords: X({rejected_list[i][0]},{rejected_list[i][1]}) Y({rejected_list[i][2]},{rejected_list[i][3]})    Correlation: {rejected_list[i][4]}", tag= LOG_TAG)

    if detected_objs != 0:
        logger.info("VB", f"PASSED", tag=LOG_TAG)
        logger.info("VB", f"Number of objects detected: {detected_objs}", tag=LOG_TAG)
        for i in range(0,detected_objs):
            logger.info("VB", f"Passed object {i+1} coords: X({(detected_list[i][0])*(cut_x/cnst.FOBJ_RESIZE_INPUT_STD)},{(detected_list[i][1])*(cut_x/cnst.FOBJ_RESIZE_INPUT_STD)}) Y({(detected_list[i][2])*(cut_y/cnst.FOBJ_RESIZE_INPUT_STD)},{(detected_list[i][3])*(cut_y/cnst.FOBJ_RESIZE_INPUT_STD)})    Correlation: {detected_list[i][4]}", tag=LOG_TAG)

    else:
        logger.warning("VB", f"FAILED", tag=LOG_TAG)

    try:
        cv2.imwrite('buena.png', display_image)
        print('si')
    except:
        cv2.imwrite('mala.png', failed_image)

