import cv2
import imutils
import time

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def humanDetection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    (regions, _) = hog.detectMultiScale(gray, winStride=(8, 8),scale=1.05)
    return regions

#cap = cv2.VideoCapture(camera_test.gstreamer_pipeline(), cv2.CAP_GSTREAMER)
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('../data/CarPOV_h-detect.mp4')

while cap.isOpened():
    # Reading the video stream
    ret, image = cap.read()
    if ret:
        image = imutils.resize(image, width=min(1080, image.shape[1]))

        start = time.time()
        regions = humanDetection(image)
        end = time.time()
        #print(f"function time taken: {end - start}")

        for (x, y, w, h) in regions:
            cv2.rectangle(image, (x, y),
                          (x + w, y + h),
                          (26, 74, 255), 1)

        # Showing the output Image
        cv2.imshow("Video", image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

print("Ending ")

cap.release()
cv2.destroyAllWindows()
