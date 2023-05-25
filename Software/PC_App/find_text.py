import csv
import boto3

def text_find_init():
    with open('Visionbox_accessKeys.csv', 'r') as input:
        next(input)
        reader = csv.reader(input)
        for line in reader:
            access_key_id = line[0]
            secret_access_key = line[1]

    client = boto3.client('rekognition',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key)
    return client

def find_all_words(img_path: str):
    client = text_find_init()

    with open(img_path, 'rb') as source_img:
        source_bytes = source_img.read()

    response = client.detect_text(Image={'Bytes': source_bytes})

    words = []
    for (x,i) in enumerate(response['TextDetections']):
        if i['Type'] == 'WORD':
            word = i['DetectedText']
            word_lst = word.split(' ')
            if len(word_lst) > 1:
                for w in word_lst:
                    words.append(w)
            else:
                words.append(word_lst[0])
    return words

if __name__ == '__main__':
    words = find_all_words('Testing/screens_cam18/T07_cam_18.png')
    print(words)