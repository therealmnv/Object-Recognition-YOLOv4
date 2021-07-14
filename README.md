# Object-Recognition-YOLOv4
Head/Hardhat Detector  
Trained YOLOv4-tiny on custom images  

There was an extra object labelled “person” which wasn’t needed for our purpose, hence, I wrote a python script to get rid of all objects labelled “person”.  
Images were annoted in Pascal VOL .xml format, hence I had to convert them to YOLO .txt format using xml.etree.  

At first I tried using the darknet53.conv.74 model, but the estimated training time was above 10 hours, so I decided to search for lighter models and came across the YOLOv4-tiny model which compromised on the accuracy slightly, but was much better with respect to frame rate. With this model the training time 
reduced drastically and was completed within 2 hours on Google Colab GPU (Tesla 4).  

Once we had the weights of the trained model, I used them to make predictions on a YouTube video: https://www.youtube.com/watch?v=6PoPwZ0WO9w  

The bounding box colour for “head” varies from pink to red and for “hat” varies from light blue to blue depending on the confidence of prediction.
