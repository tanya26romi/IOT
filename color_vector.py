import numpy as np
import cv2
import time
import serial
import math

#declare variables for window
cap = cv2.VideoCapture(1)

#define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out0 = cv2.VideoWriter('output.avi',fourcc,20.0, (640,480))

while(1):

    #take each frame
    ret,frame = cap.read()

    #making image blur to remove noise and edges
    frame = cv2.blur(frame,(5,5))
    #convert BGR to HSV
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #define range of blue colors in HSV and threshold the hsv image to get blue color

    #lower_blue = np.array([93, 149, 215])
    #upper_blue = np.array([113, 169, 295])

    #blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    #contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    idx = 0
    max_area = 0
    best_cnt = 0
    result = 0
    #convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    bool1 = False
    bool2 = False
    bool3 = False


    #image masking
    cx_b = 0
    cy_b = 0
    cx_g = 0
    cy_g = 0
    cx_y = 0
    cy_y = 0
    z=0

    #define range of green colors in HSV and threshold the hsv image to get green color

    lower_green = np.array([70, 75, 95])
    upper_green = np.array([90, 95, 175])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    contours,hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    idx = 0
    max_area = 0
    best_cnt = 0

    if(len(contours)>0):
        #print("coordinates :")
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if(area > max_area):
                max_area = area
                best_cnt = cnt

        M = cv2.moments(best_cnt)
        try:

            cx_g = int(M['m10']/M['m00'])
            cy_g = int(M['m01']/M['m00'])
            bool1 = True
            #print cx_g
            #print cy_g

            #drawing a circle
            cv2.circle(frame, (cx_g,cy_g), 5, (0,255,0), -1)#green dot

        except Exception as e:
            bool1=True
            print("ex")

    else:
        print("sorry please put green color infront of camera")

        #define range of yellow colors in HSV and threshold the hsv image to get yellow color

    lower_yellow = np.array([19, 91, 170])
    upper_yellow = np.array([39, 111, 250])

    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    idx = 0
    max_area = 0
    best_cnt = 0

    if(len(contours)>0):
        #print("coordinates :")
        for cnt in contours :
            area = cv2.contourArea(cnt)
            if(area > max_area):
                max_area = area
                best_cnt = cnt

        M = cv2.moments(best_cnt)
        try:

            cx_y = int(M['m10']/M['m00'])
            cy_y = int(M['m01']/M['m00'])
            bool2 = True

        #    print cx_y
        #    print cy_y

            #drawing a circle
            cv2.circle(frame , (cx_y,cy_y), 5, (255,255,0), -1)#lime dot

        except Exception as e:
            bool2=True
            print("ex")


    else:
        print("sorry please put yellow color infront of camera")


        #define range of blue colors in HSV and threshold the hsv image to get blue color

    lower_blue = np.array([96, 140, 144])
    upper_blue = np.array([116, 160, 224])

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    idx = 0
    max_area = 0
    best_cnt = 0
    result = 0

    if(len(contours)>0):
        #print("coordinates :")
        for cnt in contours :
            area = cv2.contourArea(cnt)
            if(area > max_area):
                max_area = area
                best_cnt = cnt

        M = cv2.moments(best_cnt)
        try:
            cx_b = int(M['m10']/M['m00'])
            cy_b = int(M['m01']/M['m00'])
            bool3 = True

        #    print cx_b
        #    print cy_b
            cv2.circle(frame,(cx,cy),5, (0,0,255), -1)#red
        except Exception as e:
            bool3=True
            print("ex_w")





        cv2.line(frame,(cx_g,cy_g),(cx_y,cy_y),(255,0,0),5)
        cv2.line(frame,(cx_g,cy_g),(cx_b,cy_b),(255,255,0),5)
        temp1 = math.sqrt(math.pow(cx_b-cx_g,2) + math.pow(cy_b-cy_g,2))
        temp2 = math.sqrt(math.pow(cx_y-cx_g,2) + math.pow(cy_y-cy_g,2))

        # |i       j      k|
        # |

        cx_bcx_gdiff = cx_b - cx_g
        cy_bcy_gdiff = cy_b - cy_g
        cy_ycy_gdiff = cy_y - cy_g
        cx_ycx_gdiff = cx_y - cx_g

        diff1 = cx_bcx_gdiff * cy_ycy_gdiff
        diff2 = cy_bcy_gdiff * cx_ycx_gdiff

        z=0

        z = diff1 - diff2
        tmp = temp1 * temp2

        result=z/tmp #sin thita
        print(result)

#        except Exception as e:
##            print("ex_w")



    else:
        print("sorry please put blue color")

    out0.write(frame)

    cv2.imshow('frame',frame)

    if cv2.waitKey(5) & 0xFF == ord('a'):
        print cv2.waitKey(5)
        break

cap.release()
cv2.destroyAllWindows()
