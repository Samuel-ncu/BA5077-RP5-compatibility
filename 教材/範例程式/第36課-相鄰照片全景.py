"""第 36 課：用 OpenCV 把相鄰拍攝的真實照片拼成全景。

在 Raspberry Pi 5 的 Thonny 執行。右下角請選裝有 OpenCV 的環境。
請先把 OpenCV 官方測試資料中的 boat1.jpg～boat6.jpg 下載到這支程式
所在的資料夾（下載方式見第 36 課課文）。

程式做兩個實驗：
  實驗 A：boat1～boat3 三張相鄰照片 → 應該成功，存成 lesson36-boat-123.jpg
  實驗 B：只用 boat1 和 boat6（中間缺了好幾張，重疊太少）→ 觀察失敗訊息
同名輸出檔會被覆寫。
"""
from pathlib import Path
import time

import cv2

folder = Path(__file__).resolve().parent
WIDTH = 800  # 先縮小到 800 像素寬，RP5 算得比較快

STATUS_TEXT = {
    cv2.Stitcher_OK: "OK 成功",
    cv2.Stitcher_ERR_NEED_MORE_IMGS: "ERR_NEED_MORE_IMGS 找不到足夠重疊，需要更多或更相鄰的照片",
    cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "ERR_HOMOGRAPHY_EST_FAIL 無法估計照片間的對應關係",
    cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "ERR_CAMERA_PARAMS_ADJUST_FAIL 相機參數調整失敗",
}


def load(name):
    path = folder / name
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"讀不到 {path}，請確認檔名與資料夾")
    scale = WIDTH / image.shape[1]
    small = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    print(f"  {name}: 原始 {image.shape[1]}x{image.shape[0]} -> {small.shape[1]}x{small.shape[0]}")
    return small


def experiment(title, names, output_name):
    print(title)
    images = [load(name) for name in names]
    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    started = time.monotonic()
    status, panorama = stitcher.stitch(images)
    seconds = time.monotonic() - started
    print("  status:", status, STATUS_TEXT.get(status, "其他錯誤"))
    print("  seconds:", round(seconds, 1))
    if status == cv2.Stitcher_OK:
        cv2.imwrite(str(folder / output_name), panorama)
        print("  panorama size:", panorama.shape[1], "x", panorama.shape[0])
        print("  saved:", output_name)


print("OpenCV", cv2.__version__)
experiment("實驗 A：三張相鄰照片", ["boat1.jpg", "boat2.jpg", "boat3.jpg"], "lesson36-boat-123.jpg")
experiment("實驗 B：重疊太少的兩張", ["boat1.jpg", "boat6.jpg"], "lesson36-boat-16.jpg")
