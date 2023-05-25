import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from crop_screen import StraightenAndCrop
from find_text import find_all_words

# Box type (x, y, w, h) where (x,y) is Top-Left and (w,h) are width and height
box_t = Tuple[int, int, int, int]

################### HELPER FUNCTIONS #####################
def img_show(img_list: List[cv2.Mat]):
    """ Shows a list of images """
    if len(img_list) == 1:
        plt.imshow(cv2.cvtColor(img_list[0], cv2.COLOR_BGR2RGB))
    else:
        _, imarr = plt.subplots(1, len(img_list))
        for i in range(len(img_list)):
            imarr[i].imshow(cv2.cvtColor(img_list[i], cv2.COLOR_BGR2RGB))

def img_preprocess_IoU(img: cv2.Mat) -> cv2.Mat:
    """ Processes an image to make it ready for IoU comparison """
    # Binarize
    THRESH = 140
    new_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, new_img = cv2.threshold(new_img, THRESH, 255, cv2.THRESH_BINARY_INV)

    # Erode
    kernel = np.ones((1, 1), np.uint8)
    new_img = cv2.erode(new_img, kernel, iterations=1)
    return new_img

def img_preprocess_Text(img: cv2.Mat):
    """ Processes an image to make it ready for text extraction """
    THRESH = 140
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img,THRESH,255,cv2.THRESH_BINARY)
    return img

def intersection_over_union(boxA: box_t, boxB: box_t) -> float:
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

def img_getSimilarity(sample_boxes: List[box_t], ref_boxes: List[box_t]) -> float:
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

def CompareText(sample_img: cv2.Mat, ref_path: str) -> float:
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
    
def CompareIoU(sample_img: cv2.Mat, ref_img: cv2.Mat) -> float:
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
    sample_img = StraightenAndCrop(sample_img, ref_img.shape[1], ref_img.shape[0])
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