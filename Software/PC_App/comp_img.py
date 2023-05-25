import cv2
from cv2 import Mat
import os
import numpy as np
import matplotlib.pyplot as plt
from find_text import find_all_words

# Helper functions to process and visualize images
def order_points(pts):
    Xorder = pts[np.argsort(pts[:, 0]), :]
    left = Xorder[:2, :]
    right = Xorder[2:, :]

    # Order along axes
    (tl, bl) = left[np.argsort(left[:, 1]), :]
    (tr, br) = right[np.argsort(right[:, 1]), :]
    return np.array([tl, tr, br, bl])

def reorder_corner_points(corners):
    Corners_ = []
    tr, tl, bl, br = [(corner[0], corner[1]) for corner in corners][0:4]
    for corner in corners:
        Corners_.append([(corner[0], corner[1])])

    Corners_ = np.reshape(Corners_, (-1, 2))
    # order the points in clockwise order
    ordered_corners = order_points(Corners_)
    return ordered_corners

def img_getScreenCorners(img):
    # convert img to grayscale
    processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_img = 255 - processed_img
    # blur image
    processed_img = cv2.GaussianBlur(processed_img, (3,3), 0)
    # do adaptive threshold on gray image
    processed_img = cv2.adaptiveThreshold(
        processed_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 2
    )
    processed_img = 255 - processed_img

    # apply morphology
    kernel = np.ones((5,5), np.uint8)
    rect = cv2.morphologyEx(processed_img, cv2.MORPH_OPEN, kernel)
    rect = cv2.morphologyEx(rect, cv2.MORPH_CLOSE, kernel)
    # thin
    kernel = np.ones((5,5), np.uint8)
    rect = cv2.morphologyEx(rect, cv2.MORPH_ERODE, kernel)

    # get largest contour
    contours = cv2.findContours(rect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for c in contours:
        area_thresh = 0
        area = cv2.contourArea(c)
        if area > area_thresh:
            area = area_thresh
            big_contour = c

    # get rotated rectangle from contour
    rot_rect = cv2.minAreaRect(big_contour)
    box = cv2.boxPoints(rot_rect)
    box = np.int0(box)
 
    (tl, tr, br, bl) = reorder_corner_points(box)
    return (tl, tr, bl, br)

def img_StraightenAndCrop(img, corners, ref_img):
    # Corner coordinates of the original image
    input_points = np.float32([corners[0], corners[1], corners[2], corners[3]])

    # Output image size
    width = ref_img.shape[1]
    height = ref_img.shape[0]

    # Desired points values in the output image
    converted_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Perspective transformation
    matrix = cv2.getPerspectiveTransform(input_points, converted_points)
    img_output = cv2.warpPerspective(img, matrix, (width, height))
    return img_output

def img_show(img_list):
    if len(img_list) == 1:
        plt.imshow(cv2.cvtColor(img_list[0], cv2.COLOR_BGR2RGB))
    else:
        _, imarr = plt.subplots(1, len(img_list))
        for i in range(len(img_list)):
            imarr[i].imshow(cv2.cvtColor(img_list[i], cv2.COLOR_BGR2RGB))

def img_dilate(img):
        kernel = np.ones((1, 1), np.uint8)
        return cv2.erode(img, kernel, iterations=1)

def img_binarize(img):
    THRESH = 140
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(gray_img,THRESH,255,cv2.THRESH_BINARY_INV)
    return img_thresh

def img_preprocess_IoU(img):
    """ Processes an image to make it ready for IoU comparison """
    new_img = img_binarize(img)
    new_img = img_dilate(new_img)
    return new_img

def img_preprocess_Text(img):
    """ Processes an image to make it ready for text extraction """
    THRESH = 140
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img,THRESH,255,cv2.THRESH_BINARY)
    return img

# Input is given in the form box = (x, y, w, h)
# where (x,y) is the top-left corner and (w,h) are width and height
def intersection_over_union(boxA, boxB):
    # Convert the boxes to the form (x, y, x+w, y+h)
	  # to get top-left and bottom-right corners      
    boxA = (boxA[0], boxA[1], boxA[0] + boxA[2], boxA[1] + boxA[3])
    boxB = (boxB[0], boxB[1], boxB[0] + boxB[2], boxB[1] + boxB[3])

    # Determine the (x, y) - coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # Compute the area of input rectangles and their intersection rectangle
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    # Compute intersection over union metric
    # Intersection area must be subtracted to avoid counting it doubly
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def img_getSimilarity(sample_boxes, ref_boxes):
    boxesA = sample_boxes.copy()  # Make copies to avoid mutation of inputs
    boxesB = ref_boxes.copy()     # Make copies to avoid mutation of inputs
    iou_thresh = 0.15         # Threshold to trigger successful IoU match
    IoU_matches = []          # Stores succesful IoU match values
    
    while len(boxesA) > 0:
        max_IoU = 0
        Bbox_to_delete = None
        for i in range(len(boxesB)):
            iou = intersection_over_union(boxesA[0], boxesB[i])
            if iou > iou_thresh and iou > max_IoU:
                max_IoU = iou
                Bbox_to_delete = boxesB[i]
        if max_IoU != 0:
            IoU_matches.append(max_IoU)
            boxesB.remove(Bbox_to_delete)
    		
    	# Remove first item in boxes list until process complete
        boxesA.pop(0)
    return (len(IoU_matches)/len(ref_boxes))

def CompareText(sample_img: Mat, ref_path: str) -> float:
    # Temporarily save sample img while find_text module
    # is ready to accept images
    tmp_sample_path = 'sample_tmp.png'
    sample_img = img_preprocess_Text(sample_img)
    cv2.imwrite(tmp_sample_path, sample_img)

    # Read all words in both images and delete temporary img after done
    sample_words = find_all_words(tmp_sample_path)
    ref_words = find_all_words(ref_path)
    os.remove(tmp_sample_path)

    # Compare words
    matches = 0
    union_length = max(len(ref_words), len(sample_words))
    for sw in sample_words:
        for rw in ref_words:
            if sw == rw:
                matches += 1
                ref_words.remove(rw)
                break
        
    text_sim = matches/union_length
    return text_sim
    
def CompareIoU(sample_img: Mat, ref_img: Mat) -> float:
    # Preprocess Images for Structural Similarity test
    SAMPLE_PROCESSED = img_preprocess_IoU(sample_img)
    REF_PROCESSED = img_preprocess_IoU(ref_img)
    SAMPLE_PROCESSED = cv2.resize(SAMPLE_PROCESSED, 
                                    (REF_PROCESSED.shape[1], REF_PROCESSED.shape[0]))

    # Calculate bounding boxes
    contours_sample, _ = cv2.findContours(SAMPLE_PROCESSED, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_ref, _ = cv2.findContours(REF_PROCESSED, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes_sample = [cv2.boundingRect(cnt) for cnt in contours_sample]
    boxes_ref = [cv2.boundingRect(cnt) for cnt in contours_ref]
    
    # Calculate similarity
    return img_getSimilarity(boxes_sample, boxes_ref)

def CompareImage(sample_path: str, ref_path: str) -> float:
    # Read images
    sample_img = cv2.imread(sample_path)
    ref_img = cv2.imread(ref_path)
    assert sample_img is not None, "Sample Image could not be read"
    assert ref_img is not None, "Reference Image could not be read"

    # First crop sample_img to show only screen of device
    #sample_img = img_cropToScreen(sample_img)
    sample_corners = img_getScreenCorners(sample_img)
    sample_img = img_StraightenAndCrop(sample_img, sample_corners, ref_img)
    # Compute comparison metrics
    iou_sim = CompareIoU(sample_img, ref_img)
    text_sim = CompareText(sample_img, ref_path)

    if text_sim < 0.9:
       return 0
    return iou_sim
 
if __name__ == '__main__':
    sample = 'Testing/screens_cam18/T07_cam_18.png'
    ref = 'Testing/screens/T07.png'
    sim = CompareImage(sample, ref)
    print(sim)