import cv2

# objects-board.png 是第 40 課的相機實拍測試圖，已裁切並透視校正。
image = cv2.imread('objects-board.png', cv2.IMREAD_GRAYSCALE)
if image is None:
    raise RuntimeError('無法讀取 objects-board.png，請確認檔案與目錄')
print('gray shape', image.shape)
print('gray dtype', image.dtype)
print('saved', cv2.imwrite('lesson17-camera-gray.png', image))
