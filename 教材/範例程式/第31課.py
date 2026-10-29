import cv2
import numpy as np
sift = cv2.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create()
image = np.random.default_rng(42).integers(0, 256, (240, 320), dtype=np.uint8)
panels = [cv2.drawKeypoints(image, detector.detect(image, None), None) for detector in (sift, surf, orb)]
if not cv2.imwrite('lesson31-features.png', cv2.hconcat(panels)):
    raise RuntimeError('image save failed')
print('SIFT created', bool(sift))
print('SURF created', bool(surf))
print('ORB created', bool(orb))
