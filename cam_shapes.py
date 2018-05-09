from shapedetector import ShapeDetector
import argparse
import imutils
import cv2

#cam = cv2.VideoCapture(0)
# konstruer en argumenter parser og parse argumentene
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help ="path to the input image")
args = vars(ap.parse_args())


# last inn bildet og endre storrelsen til en mindre faktor
# paa den maaten kan vi approksimere formene bedre
image = cv2.imread(args["image"])
#ret, image = cam.read()
resized = imutils.resize(image, width=800)
ratio = image.shape[0] / float(resized.shape[0])

# konverter bildet til graaskala og blur det litt
# sett en threshold
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.threshold(blurred, 127,255,cv2.THRESH_BINARY_INV)[1]

# finn konturene i det naa thresholdede bildet og initialiser
# shapetector.py
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()

# totalt antall firkanter
total = 0
# vi looper over konturene
for c in cnts:
	# regn ut den midtre delen av konturene
	# detekter figuren utifra konturene
	M = cv2.moments(c)
	cX = int((M["m10"] / 1) * ratio)
	cY = int((M["m01"] / 1) * ratio)
	#cX = int((M["m10"] / M["m00"]) * ratio)
	#cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)

	# multipliser saa konturene (x,y) ko-ordinater med resize ratio
	# vi tegner saa konturene og navnet paa figuren
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (255, 255, 255), 2)

	if shape == "square":
		total += 1

	print("There are a total of "+str(total)+" squares in the image")

	cv2.imshow("Image", resized)
	cv2.waitKey(0)
