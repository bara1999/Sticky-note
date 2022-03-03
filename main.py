
import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)


def empty(x):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",100,255,empty)
cv2.createTrackbar("Threshold2","Parameters",200,255,empty)
cv2.createTrackbar("Area","Parameters",2000,20000,empty)

def getContours(imgDil,imgContour):
    contours,hierarchy = cv2.findContours(imgDil,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        areaMin = cv2.getTrackbarPos("Area","Parameters")
        area = cv2.contourArea(cnt)
        #print(area)

        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        #print(len(approx))

        if  len(approx)==4:
            cv2.circle(imgContour, (cX, cY), 3, (0, 255,0 ), -1)

            cv2.line(imgContour,(cX,cY),(cX-100,cY-100),(0,200,0))
            print(cX,cY)
            #print(len(approx))
            #print(area)
            #cv2.drawContours(imgContour,cnt,-1,(255,0,255),3)
            x, y, w, h = cv2.boundingRect(approx)
            W=8.5
            #d=31
            #f=(w*d)/W
            f=698
            d=(W*f)/w
            s=str(int(d))+"cm"
            #print(d)
            cv2.putText(imgContour, s, (cX-105,cY-105), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (36, 255, 12), 1)
            # x,y,w,h = cv2.boundingRect(approx)
            # cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),3)
            # cv2.putText(imgContour,"Points: "+str(len(approx)),(x+w+20,y+20),
            #             cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0)
            # cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45),
            #             cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)
            # edges = len(approx)
            #
            # if(edges == 4):
            #     cv2.putText(imgContour, "Rectangle", (x + w + 20, y + 65),
            #                 cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)
            #
            # else:
            #     cv2.putText(imgContour, "Unknown", (x + w + 20, y + 65),
            #                 cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0)


while cap.isOpened():
    ret,img = cap.read()
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img, (7,7),1)
    imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)

    t1 = cv2.getTrackbarPos("Threshold1","Parameters")
    t2 = cv2.getTrackbarPos("Threshold2","Parameters")

    imgCanny = cv2.Canny(imgGray,t1,t2)
    #
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny,kernel,iterations=1)
    getContours(imgDil,imgContour=imgContour)
    #
    imgGray = cv2.cvtColor(imgGray,cv2.COLOR_GRAY2BGR)
    imgCanny = cv2.cvtColor(imgCanny,cv2.COLOR_GRAY2BGR)
    imgDil = cv2.cvtColor(imgDil,cv2.COLOR_GRAY2BGR)
    imgStack = np.hstack([img,imgContour])

    cv2.imshow('Output',imgStack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()