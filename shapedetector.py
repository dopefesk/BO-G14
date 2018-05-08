import cv2

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		# initialiser shape variabel og approksimer konturene
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		
		# for triangler vil det vaere tre toppunkter
		if len(approx) == 3:
			shape = "triangle"

		# for kvadrater eller rektangler vil det vaere fire toppunkter
		elif len(approx) == 4:
			# regn ut boksen og konturene for aspect ratioen
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)

			# et kvadrat vil ha en AR tilnaermet 1, ellers er det et rektangel
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

		# pentagon vil ha fire toppunkter
		elif len(approx) == 5:
			shape = "pentagon"

		# vi antar ellers at det er en sirkel
		else:
			shape = "circle"

		return shape
