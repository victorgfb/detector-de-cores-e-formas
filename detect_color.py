from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.colorlabeler import ColorLabeler
import argparse
import imutils
import cv2
import os
import urllib.request
import serial



def configSerial():
	global ser
	ser = serial.Serial('/dev/ttyACM0', 9600)

def sendSerial(dados):
	global ser
	ser.write(dados.encode())
	
configSerial()

link_fotos = 'http://192.168.11.2:8080/photo.jpg'

if not os.path.exists('fotos'):
    os.makedirs('fotos')

urllib.request.urlretrieve(link_fotos, "fotos/foto.jpg")

image = cv2.imread("fotos/foto.jpg")

resized = imutils.resize(image, width=300)
resized = resized[40:170, 100:270]
image = resized
ratio = image.shape[0] / float(resized.shape[0])

blurred = cv2.GaussianBlur(resized, (5, 5), 0)

lab = cv2.cvtColor(blurred.copy(), cv2.COLOR_BGR2HSV)
h, s, gray = cv2.split(lab)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imshow("Thresh", thresh)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

sd = ShapeDetector()
cl = ColorLabeler()


for c in cnts:
	peri = cv2.arcLength(c, True)
	if(peri < 50):
		continue
	
	M = cv2.moments(c)
	if(M["m00"] != 0):
	
		shape = sd.detect(c)
		color = cl.label(blurred, c)

		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		print(shape, color)
		
		if(color == "vermelho"):
			sendSerial("r")

		if(color == "verde"):
			sendSerial("g")

		text = "{} {}".format(shape, color)
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	
		rec = imutils.resize(image, width=600)
		cv2.imshow("Image", rec)
		cv2.waitKey(0)
		break
