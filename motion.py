from numpy import mean
from numpy import median
from urllib2 import urlopen
from time import sleep,time
from tempfile import mkstemp
import sys
from PIL import Image
import io
import numpy as np
import time
from PIL import ImageFont
from PIL import ImageDraw
import os
import cv2
from images2gif import writeGif
url = 'http://johnson.webcam.oregonstate.edu'

class motionManip:
	def detectMotion(self):
		
		webcam = urlopen('{0}/axis-cgi/jpg/image.cgi'.format(url))
		image_file = io.BytesIO(webcam.read())
		im = Image.open(image_file)
		time.sleep(1)
		webcam = urlopen('{0}/axis-cgi/jpg/image.cgi'.format(url))
		image_file = io.BytesIO(webcam.read())
		im2 = Image.open(image_file)
		rgb = np.array(im)
		rgb2 = np.array(im2)
		g = 0.2989*rgb[:,:,0]+0.5870*rgb[:,:,1]+0.1140*rgb[:,:,2]
		g2 = 0.2989*rgb2[:,:,0]+0.5870*rgb2[:,:,1]+0.1140*rgb2[:,:,2]


		dif = g-g2	
		x,y = dif.shape

		for i in range(x):
			for j in range(y):
				if dif[i,j] < -30:
					rgb[i,j] = [255,0,0]
	

		newimage = Image.fromarray(rgb)
		draw = ImageDraw.Draw(newimage)

		font = ImageFont.truetype("sans-serif.ttf",48)
		draw.text((200,200),"MOTION DETECTED!",(255,0,0),font = font)
		newimage.save("edited.jpg")

	def lotsofMotion(self):


		#cap = cv2.VideoCapture('http://128.193.38.138/mjpg/video.mjpg')
		cap = cv2.VideoCapture('http://mu.webcam.oregonstate.edu')

		lol,img = cap.read()
		og = np.array(img)
		imglist = []
		for ok in range(40):
			lol,img1 = cap.read()
			time.sleep(1)
			lol,img2 = cap.read()
			
			rgb = np.array(img1)
			rgb2 = np.array(img2)
			
			g = 0.2989*rgb[:,:,0]+0.5870*rgb[:,:,1]+0.1140*rgb[:,:,2]
			g2 = 0.2989*rgb2[:,:,0]+0.5870*rgb2[:,:,1]+0.1140*rgb2[:,:,2]



			blankimg = Image.new('1',(1280,960))
			dif = g-g2	
			print dif
			x,y = dif.shape
			for i in range(x):
				for j in range(y):
					if dif[i,j] < -30:
						blankimg.putpixel((j,i),1)
			
			imglist.append(blankimg.convert(mode="RGB"))
		writeGif("result.gif",imglist,duration=0.1,dither=0)

motion = motionManip()

motion.lotsofMotion()
