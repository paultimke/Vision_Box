import csv
import boto3
import cv2
import copy
import crop_screen
import find_object
import matplotlib.pyplot as plt
from vbox_logger import logger

LOG_TAG='FTEXT'

def init():
    """Initializes AWS client for text rekognition"""
    

    #Reads AWS access keys from csv
    with open('Visionbox_accessKeys.csv','r')as input:
        next(input)
        reader=csv.reader(input)
        for line in reader:
            access_key_id= line[0]
            secret_access_key=line[1]
    
    client=boto3.client('rekognition',
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key= secret_access_key)
    return client

def make_boxes(Text, Geometry, img):
    """Marks text's bounding box in the image"""
    x,y,w,h= get_pixelcount(Geometry, img)

    text = "".join([c if ord(c) < 128 else "" for c in Text]).strip()
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

    return(img, [x,y,w,h])

def get_pixelcount(Boundingbox,  img)-> int:
    """Converts AWS bounding box values into absolute pixel values"""
    image_h,image_w, image_c= img.shape

    x = int(Boundingbox['Left']*image_w)
    y = int(Boundingbox['Top']*image_h)

    w = int(Boundingbox['Width']*image_w)
    h = int(Boundingbox['Height']*image_h)

    return x,y,w,h




def get_words_and_mark(responses, img_word, img_line)  :
    """Separate AWS dictionary into lists that includes, the word or line and the goemetry of the bounging box"""
    #Bounding box: x,y,w,h
    l_words=[] 
    l_lines=[]
    for i in(responses['TextDetections']):
        if i['Type'] =='WORD':
            word=i['DetectedText']
            #box=get_pixelcount(i['Geometry']['BoundingBox'], img_word)
            img_word, box=make_boxes(i['DetectedText'], i['Geometry']['BoundingBox'], img_word)            
            box.insert(0, word)
            l_words.append(tuple(box))

        elif i['Type'] =='LINE':
            line=i['DetectedText']
            #box=get_pixelcount(i['Geometry']['BoundingBox'], img_line)
            img_line, box=make_boxes(i['DetectedText'], i['Geometry']['BoundingBox'], img_line)
            box.insert(0, line)
            l_lines.append(tuple(box))
    #print('words', l_words)
    return l_lines, img_word, img_line


def compare_text(input_text, l_line)->list:
    """Compares the user's input with the words found and returns the text with the goemetry if there is any match """
    found_text=[]
    for i in l_line:
        if i[0]==input_text:
            found_text.append(i)

        start_index=0
        for j in range(len(i[0])):
            index=i[0].find(input_text,start_index)
            if (index!=-1):
                start_index=index+1
                characters=[*i[0]]
                length=len(characters)
                character_size=int(i[3]/ (length))
                found_text.append((input_text, i[1]+ character_size*index, i[2], character_size*len(input_text), i[4]))

    return found_text

def show_images (found_text, img, img1, img2):
    """Shows matching texts"""
    for i in range(len(found_text)):
        Text=found_text[i][0]
        x=found_text[i][1]
        y=found_text[i][2]
        w= found_text[i][3]
        h=found_text[i][4]
        text = "".join([c if ord(c) < 128 else "" for c in Text]).strip()
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

    list_images = [img, img1, img2]
    find_object.show_image_list(list_images, 
        list_titles=['matched text', 'words', 'lines'],
        figsize=(3,3),
        grid=False,
        title_fontsize=8)
    plt.show()
    cv2.waitKey(0)

def different_size_in_line(found_text, user_text, l_lines):
    """Checks for different sizes in the same line and joins the bounding box """
    for i in range(len(l_lines)):
        y_position1=l_lines[i][2]+l_lines[i][4]
        for k in range(i+1, len(l_lines)):
            y_position2=l_lines[k][2]+l_lines[k][4]
            if (abs(y_position1 - y_position2) < y_position1*.1):
                if (l_lines[i][0] in user_text) and (l_lines[k][0] in user_text):
                    found_text.append((user_text, l_lines[i][1], l_lines[i][2], l_lines[i][3]+l_lines[k][3], l_lines[i][4]))

    return found_text

def find_text(user_text, img )-> list:
    """main function to find text"""

    photo='Testing\screens_vbox_cam\T15_vbox_cam.png'
    img = cv2.imread(photo)
    x, y, c=img.shape
    #print('size: ' ,img.shape)
    #plt.imshow(img )
    img= cv2.rotate(img, cv2.ROTATE_180)
    # plt.imshow(img)
    img= crop_screen.StraightenAndCrop(img, x, y)
    user_text='o'
    

    try :
        client=init()
        logger.debug("VB", "AWS client correctly initialize", tag=LOG_TAG)
    except:
        logger.error("VB", "Could not initialize AWS client", tag=LOG_TAG)
        found_text=[]
        return []
    
    img1=copy.deepcopy(img)
    img2=copy.deepcopy(img)

    
    source_bytes = cv2.imencode('.png', img)[1].tobytes()
    try:
        response= client.detect_text(Image={'Bytes':source_bytes} 
                                            )
        logger.debug("VB", "Image correctly sent to AWS client", tag=LOG_TAG)
    except:
        logger.error("VB", "Could not send data to AWS client", tag=LOG_TAG)
        found_text=[]
        return []


    l_lines, img1, img2=get_words_and_mark(response, img1,img2)
    found_text=compare_text(user_text, l_lines)
    if len(found_text)==0:
        found_text=different_size_in_line(found_text, user_text, l_lines)
           
    #Show images
    show_images(found_text, img, img1, img2)

    times=len(found_text)
    logger.info("VB", f"Number of times the text '{user_text}' was found: {times}", tag=LOG_TAG)
    for i in range(times):
        logger.info("VB", f"Postion {i+1}: x: {found_text[i][1]} px, y:{found_text[i][2]+found_text[i][4]} px", tag=LOG_TAG)

    return l_lines

    
print(find_text(1,1))
