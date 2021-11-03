'''
Author : @Rahul Agrwal         
Github: " https://github.com/rahul-agrawal-99 "
title : Virtual Keyboard
software-dependencies : opencv, numpy
hardware-dependencies : camera

'''

import cv2 as cv  # Version :  4.5.4.58
import numpy as np  # Version :  1.21.3
from cvzone.HandTrackingModule import  HandDetector  # Version : 1.4.1


#  it is list contains all the keybord buttons with their coordinates
#  0th position : Key Value
#  1th position : X1 coordinate
#  2th position : Y1 coordinate
#  3th position : X2 coordinate  i.e. X1 + X2 = width of the button
#  4th position : Y2 coordinate i.e. Y1 + Y2 = height of the button
btnlist = [["Q", 100 , 100 , 100 , 100 ],
           ["W", 220 , 100 , 100 , 100],
           ["E", 340 , 100 , 100 , 100],
           ["R", 460, 100 , 100 , 100],
           ["T",580, 100 , 100 , 100],
           ["Y", 700, 100 , 100 , 100],
           ["U", 820, 100 , 100 , 100],
           ["I", 940, 100 , 100 , 100],
           ["O", 1060, 100 , 100 , 100],
           ["P", 1180, 100 , 100 , 100],
           
           ["A", 130 , 220 , 100 , 100],
           ["S", 220  +30 , 220 , 100 , 100],
           ["D", 340  +30, 220 , 100 , 100],
           ["F", 460 +30, 220 , 100 , 100],
           ["G", 580 +30, 220 , 100 , 100],
           ["H", 700 +30, 220 , 100 , 100],
           ["J", 820 +30, 220 , 100 , 100],
           ["K", 940 +30, 220 , 100 , 100],
           ["L", 1060 +30, 220 , 100 , 100],
           
           ["Z", 100 + 60, 340 , 100 , 100],
           ["X", 220+ 60 , 340 , 100 , 100],
           ["C", 340 + 60, 340 , 100 , 100],
           ["V", 460+ 60, 340 , 100 , 100],
           ["B", 580+ 60, 340 , 100 , 100],
           ["N", 700+ 60, 340 , 100 , 100],
           ["M", 820+ 60, 340 , 100 , 100],
           
           
           [" ", 450, 450 , 430 , 100],   # sapce bar
           ["Enter",1210, 220 , 200 , 100]  # Enter 
      
           
           
           ]


#  detecting the hand and drawing the bounding box
detector =  HandDetector(detectionCon=0.8)

# for capturing the video
cam=cv.VideoCapture(1)


#  function to draw the bounding box
def drawbtn(img,x,y,w,h,text , color = (255,0,255) , hover = "no"):
    if hover == "slide":
        cv.rectangle(img,(x,y),(x+w,y+h),color,cv.FILLED)
    if hover == "click":
        cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255),cv.FILLED)
    
    cv.putText(img,text,(x+23,y+60),cv.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
    sub_img = img[y:y+h, x:x+w]
    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
    res = cv.addWeighted(sub_img, 0.4, white_rect, 0.5, 1.0)
    img[y:y+h, x:x+w] = res
    return img


# contains typed message
msg =  " "



#  loop camera captured frames
while True:
    ist , f =  cam.read() 
    f=cv.resize(f,(1400,700))
    f=detector.findHands(f)
    lmList, bbox = detector.findPosition(f)
    if lmList:
        for i in btnlist:
            f=drawbtn(f , i[1] ,  i[2] , i[3] , i[4], i[0])
            if i[1] < lmList[8][0] < i[1] + i[3] and i[2] < lmList[8][1] < i[2] + i[4]:
                f=drawbtn(f , i[1] ,  i[2] , i[3] , i[4], i[0] , color = (255,0,255) , hover="slide")
                l,_,_ = detector.findDistance(8,12,f)
                if l< 55:
                    f=drawbtn(f , i[1] ,  i[2] , i[3] , i[4], i[0] , color = (0,255,0) , hover="slide")
                    #  avoid multiple clicks on the same button 
                    if i[0] != msg[len(msg)-1]:
                        if i[0]=="Enter":
                            msg =msg + "\n"
                        else:    
                            msg =msg + i[0]
    else:
        cv.putText(f,f"No Hand Detected",(200,400),cv.FONT_HERSHEY_SIMPLEX,3,(0,0,255),5)
        cv.putText(f,f"for exiting from code press button 'd' 2 times",(10,500),cv.FONT_HERSHEY_SIMPLEX,1,(230,180,250),3)
    cv.putText(f,f" Typed : {msg}",(5,600),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                    
                
    cv.imshow("video", f)
    if (cv.waitKey(20) & 0xFF== ord('d')):

        break


print(f'Typed :\n " { msg} "')

print("****** Program Ended ******")


cv.waitKey(0)  
