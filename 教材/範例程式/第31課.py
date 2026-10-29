import cv2
sift = cv2.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create()
print('SIFT created', bool(sift))
print('SURF created', bool(surf))
print('ORB created', bool(orb))
