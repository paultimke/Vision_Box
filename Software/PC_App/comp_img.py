import cv2
import numpy as np
import matplotlib.pyplot as plt

# Helper functions to process and visualize images
def img_cropToScreen(img):
    bin_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(bin_img, 127, 255, cv2.THRESH_BINARY)

    MIN_CONTOUR_AREA = 300
    MARGIN_CUT = 0

    # Find screen contours
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            [x, y, w, h] = cv2.boundingRect(contour)

    cropped_img = img.copy()[y+MARGIN_CUT : y+h-MARGIN_CUT, x+MARGIN_CUT : x+w-MARGIN_CUT]
    return cropped_img

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

def img_preprocess(img):
    new_img = img_binarize(img)
    new_img = img_dilate(new_img)
    return new_img

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
    
def CompareImage(sample_path: str, ref_path: str) -> float:
    # Read and pre-process images
    SAMPLE_PATH = sample_path
    REF_PATH = ref_path
    SAMPLE = cv2.imread(SAMPLE_PATH)
    REF = cv2.imread(REF_PATH)

    SAMPLE_PROCESSED = img_cropToScreen(SAMPLE)
    SAMPLE_PROCESSED = img_preprocess(SAMPLE_PROCESSED)
    REF_PROCESSED = img_preprocess(REF)
    SAMPLE_PROCESSED = cv2.resize(SAMPLE_PROCESSED, 
                                    (REF_PROCESSED.shape[1], REF_PROCESSED.shape[0]))
    
    # Calculate bounding boxes
    contours_sample, _ = cv2.findContours(SAMPLE_PROCESSED, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_ref, _ = cv2.findContours(REF_PROCESSED, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boxes_sample = [cv2.boundingRect(cnt) for cnt in contours_sample]
    boxes_ref = [cv2.boundingRect(cnt) for cnt in contours_ref]
    
    # Calculate similarity
    Similarity = img_getSimilarity(boxes_sample, boxes_ref)
    return Similarity

if __name__ == '__main__':
    sample = 'screens_cam18/T8_cam_18.png'
    ref = 'screens/T8.png'
    sim = CompareImage(sample, ref)
    print(sim)