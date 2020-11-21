import cv2
import numpy as np 
import matplotlib.pyplot as plt 

SHOW = True

img = cv2.imread('board.jpg', cv2.IMREAD_GRAYSCALE)

#if SHOW:
	# cv2.namedWindow('image',cv2.WINDOW_NORMAL)
	# cv2.resizeWindow('image', 600,600)
	# cv2.imshow('image', img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

blur = cv2.medianBlur(img, 5)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
ret,thresh = cv2.threshold(sharpen,110,255,cv2.THRESH_BINARY)

kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(thresh,kernel,iterations = 1)

kern = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

squares = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
squares = squares[0] if len(squares) == 2 else squares[1]
print(squares)
for square in squares:
	print('in')
	x,y,w,h = cv2.boundingRect(square)
	cv2.rectangle(closing, (x,y), (x + w, y +h), [36, 255, 12], 2)


if SHOW:
	cv2.namedWindow('image',cv2.WINDOW_NORMAL)
	cv2.resizeWindow('image', 600,600)
	cv2.imshow('image', closing)
	cv2.waitKey(0)
	cv2.destroyAllWindows()