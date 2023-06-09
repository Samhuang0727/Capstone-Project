import cv2
import numpy as np
from robot import Robot
import time

robot = Robot()

def gstreamer_pipeline(
    w=640,
    h=480,
    display_width=640,
    display_height=480,
    framerate=60,
    flip_method=0,
):
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                w,
                h,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
    )

#HSV tracking
#cv2.namedWindow("Tracking")
#cv2.createTrackbar("Hmin", "Tracking", 0, 255, nothing)
#cv2.createTrackbar("Hmax", "Tracking", 255, 255, nothing)
#cv2.createTrackbar("Smin", "Tracking", 0, 255, nothing)
#cv2.createTrackbar("Smax", "Tracking", 255, 255, nothing)
#cv2.createTrackbar("Vmin", "Tracking", 0, 255, nothing)
#cv2.createTrackbar("Vmax", "Tracking", 255, 255, nothing)    
#hmin = cv2.getTrackbarPos("Hmin", "Tracking")
#hmax = cv2.getTrackbarPos("Hmax", "Tracking")
#smin = cv2.getTrackbarPos("Smin", "Tracking")
#smax = cv2.getTrackbarPos("Smax", "Tracking")
#vmin = cv2.getTrackbarPos("Vmin", "Tracking")
#vmax = cv2.getTrackbarPos("Vmax", "Tracking")
#lower_bound = np.array([hmin, smin, vmin])
#upper_bound = np.array([hmax, smax, vmax])

def show_camera():
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        window_handle = cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)
        while cv2.getWindowProperty("frame", 0) >= 0:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            ret, frame1 = cap.read()
            if not ret:
                print("No detected frame")
                break
            cv2.imshow('frame', frame1)

            frame = frame1
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            Green_lower_bound = np.array([54, 20, 200])
            Green_upper_bound = np.array([85, 255, 255])
            Gmask = cv2.inRange(hsv, Green_lower_bound, Green_upper_bound)
            green_circles = cv2.HoughCircles(Gmask, cv2.HOUGH_GRADIENT, 1, 60, param1=50, param2=10, minRadius=8, maxRadius=14)
            print(green_circles)
            if green_circles is not None &:
                green = True
                robot.set_motors(0.25,0.247)
                time.sleep(2)
                break
            else:
                green = False
            
            # hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # green_lower = np.array([55, 30, 250], np.uint8)
            # green_upper = np.array([110, 255, 255], np.uint8)
            # green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
            # kernel = np.ones((5, 5), "uint8")
            # green_mask = cv2.dilate(green_mask, kernel)
            # res_green = cv2.bitwise_and(frame, frame, mask = green_mask)
            # contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # leave = False
            
            # #print(contours)
            # for pic, contour in enumerate(contours):
            #     area = cv2.contourArea(contour)
            #     print(area)
            #     if(area > 1000): #detected green light
            #         x, y, w, h = cv2.boundingRect(contour)
            #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #         leave = True
            #         break
            # if leave == True:
                #  robot.set_motors(0.25,0.17)
                #  time.sleep(2)
            #     break
            
            

            # if area is not None:
            #     #robot.set_motors(0.2,0.2)
            # else:
            #     #robot.stop()

            # cv2.imshow('Result', frame)
            
            
        cv2.destroyAllWindows()

if __name__ == "__main__":
    show_camera()

