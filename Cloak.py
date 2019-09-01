#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import cv2
import time


# In[2]:


# setting the width and height of webcam
width = 1300
height = 900

# capturing from webcam
cam = cv2.VideoCapture("C:/Users/Muhammad Ahmed/Desktop/DataScience/Harry Potter/720_30_13.23_Sep012019.mp4")


# In[3]:


# setting width and height
cam.set(3,width)
cam.set(4,height)

#warming up camera before capturing background
time.sleep(1)

# capturing image in 0  to 60 sec to capture background
background = 0
for i in range(60):
    return_v,background = cam.read()
    if return_v == False: #returns false if no frame is captured
        continue

background = np.flip(background,axis=1) #flipping the frame


# In[ ]:


while(cam.isOpened()):
    return_v,img  = cam.read()
    if not return_v:
        break
    #fliping and converting the captured image to hsv for better results
    img = np.flip(img,axis=1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    # upper and lower range colors for background
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    #making mask for both upper and lower
    mask1= cv2.inRange(hsv,lower_red,upper_red)
    #same process for mask2
    lower_red = np.array([170,120,70]) 
    upper_red = np.array([180,255,255]) 
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
    #merging both masks
    mask1 = mask1+mask2
    
    #applying morphilogy. to see how it looks go to https://docs.opencv.org/3.0-beta/_images/gradient.png
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.int8),iterations=2)
    # dilating it. see what it does: https://docs.opencv.org/3.0-beta/_images/dilation.png
    mask1 = cv2.dilate(mask1,np.ones((3,3),np.int8),iterations=1)
    #bitwise operation to create inv mask, see how it works: https://docs.opencv.org/3.2.0/overlay.jpg
    mask2 = cv2.bitwise_not(mask1)
    
    #generating final output
    res1 = cv2.bitwise_and(background,background,mask=mask1)
    res2 = cv2.bitwise_and(img,img,mask=mask2)
    # look how this bitwish operations(not,and) are joining everything up: https://docs.opencv.org/3.2.0/overlay.jpg
    #final output
    output = cv2.addWeighted(res1,1,res2,1,0)
    #display
    cv2.imshow("Magic !!!",output)
    k = cv2.waitKey(10)
    if k == 27:
        break


