import cv2 as cv
import numpy as np
import os

net = cv.dnn.readNetFromDarknet('yolov4-tiny-custom.cfg',r'yolov4-tiny-custom_MNV_final.weights')
classes = ['head','hat']
path = 'Images'
outPath = 'testOutputs'
font = cv.FONT_HERSHEY_PLAIN
colors = (255,0,0) #np.random.uniform(0,255,size=(len(boxes),3))
color2 = (0,0,255)

for i in os.listdir(path):
    img = cv.imread(os.path.join(path,i))
    #img = cv.resize(img,(1280,720))
    #img = cv.resize(cv.imread('images/images\hard_hat_workers0.png').shape[:2])
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
        fname = str(os.path.join(outPath,str(i)[:-3]))+'txt'
        file = open(fname, 'w')   
    
    # Writing a string to file
        if len(indexes) > 0:
            for j in indexes.flatten():
                x,y,w,h = boxes[j]
                label = str(class_ids[j])
                file.write(label+' '+str(x)+' '+str(y)+' '+str(w)+' '+str(h)+'\n')
        file.close()
cv.destroyAllWindows()