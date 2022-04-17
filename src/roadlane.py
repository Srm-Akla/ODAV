import numpy as np
import cv2

#largely derived from https://github.com/oneshell/road-lane-detection/blob/master/detection.py
#modified and commented by Hana for fitting different viewpoints/private videos

#variables needing to be changed for another video:
#frame for the clip
#threshold when converting to binary,black/white

def read_snip(cap):
    # reading the video in frames
    ret, frame1 = cap.read()
    frame = cv2.resize(frame1, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    #cv2.imshow("Original Video", frame)

    # take a snip from the video that is interesting
    #clip = frame[500:700,300:950]   #for testvideo2
    clip = frame[30:900, 200:950]   #for private video

    cv2.imshow("Clip", clip)

    return clip

def mask(clip):

    # create a polygon mask to select interesting region
    mask = np.zeros((clip.shape[0], clip.shape[1]), dtype="uint8")

    #the polygon needs to be changed according to the view from the car
    # so it can detect lines when further away from them
    # [where to start on the left,how far to the right]
    #setting the values according to the view from the car
    #pts = np.array([[0, 200], [180, 60], [400, 70], [600, 200]], dtype=np.int32)  #for testvideo2
    pts = np.array([[0, 300], [150, 200], [450, 200], [600, 300]], dtype=np.int32)  #for private video

    cv2.fillConvexPoly(mask, pts, 255)
    #cv2.imshow("Mask", mask)

    # apply mask and show masked image on screen
    masked = cv2.bitwise_and(clip, clip, mask=mask)
    cv2.imshow("Region of Interest", masked)

    return masked

def to_grayscale(masked):

    # convert frames to grayscale
    frame = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    #thresh = 200   #for testvideo2
    thresh = 200    #fits test_video for detecting the yellow line
    #convert grayscale to binary image, black/white
    frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Black/White", frame)

    return frame

def blur_image(frame):

    # blur image before edge detection
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #cv2.imshow("Blurred video", blurred)

    return blurred

def edge_detection(blurred):
    #identify edges using canny edge detection
    edged = cv2.Canny(blurred, 300, 500)
    cv2.imshow("Canny Edge Detection", edged)

    return edged

def line_detection(edged, snip):

    # perform full Hough Transform to identify lane lines
    lines = cv2.HoughLines(edged, 1, np.pi / 180, 25)

    # define arrays for left and right lanes
    rho_left = []     #top left?
    theta_left = []    #bottom left?q
    rho_right = []     #top right?
    theta_right = []   #bottom right?

    # ensure cv2.HoughLines found at least one line
    if lines is not None:

        # looping through the found lines
        for i in range(0, len(lines)):

            # check every row of lines from Hough Lines function
            for rho, theta in lines[i]:

                # collect the left lanes
                if theta < np.pi/2 and theta > np.pi/4:   #defines if the line most likely belongs to the left lanes
                    rho_left.append(rho)
                    theta_left.append(theta)

                # collect the right lanes
                if theta > np.pi/2 and theta < 3*np.pi/4: #defines if the line most likely belongs to the right lanes
                    rho_right.append(rho)
                    theta_right.append(theta)

                #this results in a lot of tiny lines


    # statistics for identifying the median lane dimensions, collecting all the tiny lines into one thick line
    left_rho = np.median(rho_left)
    left_theta = np.median(theta_left)
    right_rho = np.median(rho_right)
    right_theta = np.median(theta_right)

    # plot the median line on the video clip
    if left_theta > np.pi/4:
        a = np.cos(left_theta); b = np.sin(left_theta)
        x0 = a * left_rho; y0 = b * left_rho
        offset1 = 70
        offset2 = 200
        x1 = int(x0 - offset1 * (-b))
        y1 = int(y0 - offset1 * (a))
        x2 = int(x0 + offset2 * (-b))
        y2 = int(y0 + offset2 * (a))

        cv2.line(snip, (x1, y1), (x2, y2), (255, 0, 0), 6)

    if right_theta > np.pi/4:
        a = np.cos(right_theta); b = np.sin(right_theta)
        x0 = a * right_rho; y0 = b * right_rho
        offset1 = 400   #how far away from the car the right line is
        offset2 = 800
        x3 = int(x0 - offset1 * (-b))
        y3 = int(y0 - offset1 * (a))
        # x4 = int(x0); y4=int(y0)    her vil den bare vise linje helt øverst
        x4 = int(x0 - offset2 * (-b))
        y4 = int(y0 - offset2 * (a))

        cv2.line(snip, (x3, y3), (x4, y4), (255, 0, 0), 6)


    cv2.imshow("Road lanes detected", snip)


if __name__ == "__main__":
    # identify filename of video to be analyzed
    #cap = cv2.VideoCapture('../data/testvideo2.mp4')
    cap = cv2.VideoCapture('../data/CarPOV_roadlane.mp4')

    # loop through until entire video file is played
    while(cap.isOpened()):
        try:
            snip = read_snip(cap)
            masked = mask(snip)
            frame = to_grayscale(masked)
            blurred = blur_image(frame)
            edged = edge_detection(blurred)
            line_detection(edged, read_snip(cap))
        except(RuntimeError):
           pass

    # press the q key to break out of video
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # clear everything once finished
    cap.release()
    cv2.destroyAllWindows()



