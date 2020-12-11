import numpy as np
import cv2
import imutils
import os

def detectFeaturesAndMatch(img1, img2, algo):
    if algo == 'SIFT':
        sift = cv2.xfeatures2d.SIFT_create()
        print('detect and compute sift')
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        print('FLANN')
        match = cv2.FlannBasedMatcher(index_params, search_params)
        print('Match')
        matches = match.knnMatch(des1,des2,2)
        good = []

        for m,n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    if algo == 'ORB':
        orb = cv2.ORB_create()
        print('detect and compute ORB')
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
        print('matching')
        src_pts = np.float32([kp1[elem.queryIdx].pt for elem in matches])
        dst_pts = np.float32([kp2[elem.trainIdx].pt for elem in matches])

    print('done matching')
    return src_pts, dst_pts

def match(img2, img1, direction = None):
    bwimg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    bwimg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    src_pts, dst_pts = detectFeaturesAndMatch(img1, img2, 'ORB')

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h,w, _ = img1.shape
    height1, width1 = img1.shape[0], img1.shape[1]
    height2, width2 = img2.shape[0], img2.shape[1]
    #create blank image that will be large enough to hold stitched image
    blank_image = np.zeros(((width1 + width2),(height1 + height2),3),np.uint8)
    #stitch image two into the resulting image while using blank_image
    #to create a large enough frame for images
    dst = cv2.warpPerspective(img2,M,blank_image.shape[0:2])

    #dst = cv2.warpPerspective(img1,M,(img2.shape[1] + img1.shape[1], img2.shape[0]))
    dst[0:img2.shape[0],0:img2.shape[1]] = img2
    return dst

directory = '/home/keenan/code/get_learnt/uav/images'
images = []
for image in os.listdir(directory):
    if image.endswith('.JPG') and image.startswith('S'):
        images.append(cv2.imread('images/'+image))

dst = match(images[0], images[1])
cv2.imwrite('testerester2.jpg', dst)
