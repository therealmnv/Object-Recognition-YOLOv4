import cv2 as cv
import numpy as np

net = cv.dnn.readNetFromDarknet('yolov4-tiny-custom.cfg',r'yolov4-tiny-custom_MNV_final.weights')
classes = ['head','hat']


font = cv.FONT_HERSHEY_PLAIN

def findColor(label,confidence):
    if label=='hat':
        return (200+int(float(confidence))*55,(150-int(float(confidence))*200),0)
    else:
        return (150-int(float(confidence))*200,0,200+int(float(confidence))*55)

result = cv.VideoWriter('final3.mp4', 
                         cv.VideoWriter_fourcc(*'H264'),10,
                         (1280,720))

cap = cv.VideoCapture('Top 10 Safety Vest For Construction For Men And Women.mp4')


while True:
    _,img = cap.read()

    #img = cv.resize(cv.imread('images/images\hard_hat_workers0.png').shape[:2])
    img = cv.resize(img,(1280,720))
    height,width,_ = img.shape
    blob = cv.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True)

    net.setInput(blob)

    layerOutputs = net.forward(net.getUnconnectedOutLayersNames())
    
    boxes = [] #coordinates
    confidences = [] #%
    class_ids = [] #head/hat

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]

            if confidence>0.5:
                centerX = int(detection[0]*width)
                centerY = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(centerX - w/2)
                y = int(centerY - h/2)

                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(classId)
    
        indexes = cv.dnn.NMSBoxes(boxes,confidences,0.5,0.4)
        

        if len(indexes) > 0:
            for i in indexes.flatten():
                x,y,w,h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i],2))
                color = findColor(label,confidence)
                if label == 'hat':
                    cv.rectangle(img,(x,y), (x+w,y+h), color, 2)
                else:
                    cv.rectangle(img,(x,y), (x+w,y+h), color, 2)
                cv.putText(img, label + " " + confidence, (x, y+25), font, 2, (0,255,0), 2) #size color thickness

    result.write(img)
    # cv.imshow('Out', img)
    # k = cv.waitKey(1)
    # if k == 27:
    #     break

cap.release()
cv.destroyAllWindows()