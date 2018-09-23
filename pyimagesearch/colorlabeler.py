from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
	def __init__(self):
		colors = OrderedDict({
			"vermelho": (0, 0, 255),
			"verde": (0, 250, 0),
			"azul": (255, 0, 0),
			"amarelo": (0, 255 , 255),
			"branco": (240,250,250)
			})

		self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
		self.colorNames = []

		for (i, (name, rgb)) in enumerate(colors.items()):
			self.lab[i] = rgb
			self.colorNames.append(name)

		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)
		cv2.imshow('as', self.lab)
	def label(self, image, c):
		image = cv2.cvtColor(image,cv2.COLOR_RGB2LAB)
		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.erode(mask, None, iterations=2)
		cv2.imshow('lab', image)
		mean = cv2.mean(image, mask=mask)[:3]

		minDist = (np.inf, None)
		minDist2 = (np.inf, None)

		for (i, row) in enumerate(self.lab):

			d = dist.euclidean(row[0], mean)

			if d < minDist[0]:
				minDist = (d, i)
			elif d < minDist2[0]:
				minDist2 = (d,i)

		print(minDist, "/n" , minDist2)
		if(minDist[1] == 0 and minDist2[1] == 3):
			return 'yellow'

		return self.colorNames[minDist[1]]
