import cv2
import numpy as np
import os

directory = '/home/keenan/code/get_learnt/uav/images'
images = []
for image in os.listdir(directory):
    if image.endswith('.JPG') and image.startswith('S'):
        images.append(cv2.imread('images/'+image))

print(len(images))
def join_two(img1, img2):
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key = lambda x:x.distance)

    src_pts = np.float32([kp1[match.queryIdx].pt for match in matches])
    dst_pts = np.float32([kp2[match.trainIdx].pt for match in matches])
    homo, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # inverse_homo = np.linalg.inv(homo)
    # ds = np.dot(inverse_homo, np.array([img1.shape[1], img1.shape[0], 1]));
    # ds = ds/ds[-1]
    #
    # f1 = np.dot(inverse_homo, np.array([0,0,1]))
    # f1 = f1/f1[-1]
    # inverse_homo[0][-1] += abs(f1[0])
    # inverse_homo[1][-1] += abs(f1[1])
    # ds = np.dot(inverse_homo, np.array([img1.shape[1], img1.shape[0], 1]))
    # offsety = abs(int(f1[1]))
    # offsetx = abs(int(f1[0]))
    # dsize = (int(ds[0])+offsetx, int(ds[1]) + offsety)
    #
    # tmp = cv2.warpPerspective(img1, inverse_homo, dsize)
	# # cv2.imshow("warped", tmp)
	# # cv2.waitKey()
    # tmp[offsety:img2.shape[0]+offsety, offsetx:img2.shape[1]+offsetx] = img2
    #

    #h,w, d = img1.shape
    #pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    #dst = cv2.perspectiveTransform(pts, M)
    #img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    dst = cv2.warpPerspective(img1,homo,(img2.shape[1] + img1.shape[1], img2.shape[0]))
    dst[0:img2.shape[0],0:img2.shape[1]] = img1
    return dst

dst = join_two(images[0], images[1])
# for i in range(2,len(images)):
#     print(i)
#     dst = join_two(dst, images[i])



cv2.imwrite('untrimmed.jpg', dst)
