# Referenced opencv video source: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
# Referenced opencv contours source: https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html 
# Referenced tutorial: https://pythonprogramming.net/color-filter-python-opencv-tutorial/
# https://automaticaddison.com/real-time-object-tracking-using-opencv-and-a-webcam/ 
import numpy as np
import cv2

# RGB: 188, 216, 198
# HSV: 165°, 31%, 95%


#rgb_lower = np.array([178, 206, 188])

#rgb_upper = np.array([198, 226, 208])

lower_bound = np.array([95, 34, 128]) #HSV

upper_bound = np.array([140, 190, 255]) #HSV

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here

    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert frame to HSV
    #converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    detect = cv2.inRange(converted, lower_bound, upper_bound) # detect values in range
    #detect = cv2.inRange(converted, rgb_lower, rgb_upper) 
    
    contours,_ = cv2.findContours(detect, 1, 2)

    if contours:
        areas = [cv2.contourArea(c) for c in contours]

        max_index = np.argmax(areas)

        # Draw the bounding box
        cnt = contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            
        # Display the resulting frame
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()