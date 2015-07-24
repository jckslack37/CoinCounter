e__author__ = 'pi'

# Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

cv2.imshow('image', image)

b, g, r = cv2.split(image)
blurred = cv2.GaussianBlur(r, (11, 11), 0)

ret, thresh = cv2.threshold(blurred, 107, 255, cv2.THRESH_BINARY)
close = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (7, 7))
cv2.imshow('close', close)
cv2.waitKey(2000)
cv2.destroyAllWindows()


(_, cnts, _) = cv2.findContours(close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE, None, None, None)


print "I count %d coins in this image" % (len(cnts))

coins = image.copy()
cv2.drawContours(coins, cnts, -1, (0, 255, 0), 2)
# imshow("Coins", coins)
# cv2.waitKey(0)

dimes = 0
quarters = 0
nickels = 0
pennies = 0

for (i, c) in enumerate(cnts) :
    (x, y, w, h) = cv2.boundingRect(c)

    print "Coin #%d" % (i + 1)
    coin = image[y:y + h, x:x + w]
    cv2.imshow("Coin", coin)
    cv2.waitKey(500)

    mask = np.zeros(image.shape[:2], dtype="uint8")
    ((centerX, centerY), radius) = cv2.minEnclosingCircle(c)
    print(radius)
    cv2.circle(mask, (int(centerX), int(centerY)), int(radius), 255, -1)
    mask = mask[y:y + h, x:x + w]
    # thomas is the greatest ever!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if radius > 38  and radius < 43:
        dimes = dimes + 1

print('I count %d dimes' % dimes)
time.sleep(2)
cv2.destroyAllWindows()


                          




