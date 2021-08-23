# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 23:52:41 2021

@author: kiran
"""

import cv2
import numpy as np
import sys

video_name = "video.mp4"

video = cv2.VideoCapture(video_name)

tracker = cv2.TrackerCSRT_create()
multiTracker = cv2.MultiTracker_create()
bboxes=[]

file = open("bounding_box.txt", "a") 

if not video.isOpened():
    print("Could not open video")
    sys.exit()

frame_number=0

while True:
    ok,frame = video.read()
    
    if not ok:
        print("Cannot read video file")
        break
    
    status,boxes = multiTracker.update(frame)
    
    #press s key to realign the bounding box
    if cv2.waitKey(1) & 0xFF == ord('s'):
        bboxes=[]
        multiTracker = cv2.MultiTracker_create()
        count=0
        while count<2:
            bbox = cv2.selectROI(frame, False)
            bboxes.append(bbox)
            count=count+1
                 
        for box in bboxes:
            tracker = cv2.TrackerCSRT_create()
            multiTracker.add(tracker,frame,box)
     
    
    if status:
        for i,bbox in enumerate(boxes):
            p1 = (int(bbox[0]),int(bbox[1]))
            p2 = (int(bbox[0]+bbox[2]),int(bbox[1]+bbox[3]))
            file.write(str(frame_number)+","+str(bbox[0])+","+str(bbox[1])+","+str(bbox[2])+","+str(bbox[3])+"\n")
            #Save the image here with the frame_number as the name of the image file
            cv2.rectangle(frame,p1,p2,(255,0,0),2,1)
    else:
        cv2.putText(frame,"Tracking failure detected",(100,80),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2);
    
    cv2.imshow("Tracking",frame)
    
    frame_number=frame_number+1
    
    #press ESC to exit
    if cv2.waitKey(20) & 0xFF ==27:
        break    
        
video.release()
cv2.destroyAllWindows()