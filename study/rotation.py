import numpy as np
import math

from PyQt5.QtCore import QPoint, QPointF
from PyQt5.QtGui import QVector2D


class QVector2D(QVector2D):
	def __init__(self, *args):
		super().__init__(*args)

	def rotate(self, deg, cx=0, cy=0):
		''' Rotates @deg degrees _clockwise_ about point (@cx, @cy). '''
		a = math.radians(deg)
		x = self.x()
		y = self.y()
		self.setX(round( (x-cx)*math.cos(-a) - (y-cy)*math.sin(-a) + cx, 10 ))
		self.setY(round( (x-cx)*math.sin(-a) + (y-cy)*math.cos(-a) + cy, 10 ))

	def toTuple(self):
		''' Return the vector as a tuple. '''
		return (self.x(), self.y())


class AndPort:
	def __init__(self, inputs=2):
		self.inputs = []
		centerPoint = QVector2D(1,1) # offset relative to top-left corner of the component

		for i in range(inputs):
			point = QVector2D(0, 2*i) - centerPoint
			self.inputs.append(QVector2D(point))
		point = QVector2D(inputs, 1) - centerPoint
		self.output = QVector2D(point)

		self.x = 0
		self.y = 0

	def setPosition(self, x, y):
		self.x = x
		self.y = y

	def rotate(self, deg):
		''' Rotates @deg degrees about the center point of the component. '''

		for (i,p) in enumerate(self.inputs):
			self.inputs[i].rotate(deg)
		self.output.rotate(deg)

	def printPorts(self):
		''' Relative to the center point! '''
		print("INS: " + str(list(map(lambda i: i.toTuple(), self.inputs))))
		print("OUT: " + str(self.output.toTuple()))


and1 = AndPort(2)
and1.printPorts()

and1.rotate(90)
and1.printPorts()
