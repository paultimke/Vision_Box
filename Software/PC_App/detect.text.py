import csv
import boto3
import cv2
import copy



def init():
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

    x,y,w,h= get_pixelcount(Geometry, img)

    text = "".join([c if ord(c) < 128 else "" for c in Text]).strip()
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

    return(img, [x,y,w,h])

def get_pixelcount(Boundingbox,  img):
    image_h,image_w, image_c= img.shape

    x = int(Boundingbox['Left']*image_w)
    y = int(Boundingbox['Top']*image_h)

    w = int(Boundingbox['Width']*image_w)
    h =int(Boundingbox['Height']*image_h)

    return x,y,w,h

def get_words_and_mark(responses, img_word, img_line):
    l_words=[] 
    l_lines=[]
    for x,i in enumerate(responses['TextDetections']):
        #print(i['Confidence'])
        if i['Type'] =='WORD':
            word=[i['DetectedText']]
            img_word, box=make_boxes(i['DetectedText'], i['Geometry']['BoundingBox'], img_word)
            word.append(box)
            l_words.append(tuple(word))
            

        elif i['Type'] =='LINE':
            line=[i['DetectedText']]
            img_line, box=make_boxes(i['DetectedText'], i['Geometry']['BoundingBox'], img_line)
            line.append(box)
            l_lines.append(tuple(line))
        
        

    return l_words,l_lines, img_word, img_line


def compare_text(input_text, l_line, l_word):
    control=input_text.split()
    found_text=[]
    print('imput text: ' , input_text)
    if len(control)==1:
        for i in l_word:            
            if i[0]==input_text:
                found_text.append(i)
    elif len(control)>1:
        for i in l_line:
            if i[0]==input_text:
                found_text.append(i)

    return found_text


def find_text(user_text,img ):
    img1=copy.deepcopy(img)
    img2=copy.deepcopy(img)



    #source_bytes = cv2.imencode('.png', img)[1].tobytes()

    response= client.detect_text(Image={'Bytes':source_bytes} 
                                        )

    l_words,l_lines, img1, img2=get_words_and_mark(response, img1,img2)




    found_text=compare_text(user_text, l_lines, l_words)

    cv2.imshow('Word found', img1)
    cv2.imshow('Type found', img2)
    cv2.waitKey(0)

    return found_text

    
client=init()
photo='wireframes\wireframe4.png'
img = cv2.imread(photo)
with open(photo,'rb') as source_image:
    source_bytes=source_image.read()


print(find_text('Date',img))