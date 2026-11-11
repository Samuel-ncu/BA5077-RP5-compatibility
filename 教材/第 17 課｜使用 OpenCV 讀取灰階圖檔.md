# 第 17 課｜使用 OpenCV 讀取灰階圖檔

[原始文章](https://liusming.pixnet.net/blog/posts/14222886366) · 教學編排修訂：2026-11-11

彩色照片變成灰階後，哪些資訊留下來了？這一課從讀取一張檔案開始，讓我們親眼比較原圖與結果，再學會在資料夾中找到作品。

## 第一步：準備一張我們都能取得的照片

先完成[第 14 課](./第%2014%20課｜在%20Raspberry%20Pi%205%20安裝%20OpenCV.md)，沿用已能畫圓的環境。這一課讀的是圖片檔，暫時不必接相機。

在 RP5 建立一個新的練習資料夾，把[彩色圖片 objects-board.png](./圖檔/objects-board.png)和[本課程式](./範例程式/第17課-灰階讀圖顯示-trixie.py)放在一起。保留圖片原檔名；我們會靠這個名字找到它。

這張圖片是先生成物件圖，再顯示於螢幕、由 RP5 相機拍攝及裁切校正的練習素材。圖中有水果和杯子，適合觀察顏色消失後的差異。

## 第二步：先看看程式怎樣找到圖片

在 Thonny 開啟程式，找到 `folder` 那一行。`__file__` 指這份程式的位置，`.parent` 是它所在的資料夾；因此我們把照片放在程式旁邊，就不用知道老師電腦上的路徑。

再往下看，`IMREAD_GRAYSCALE` 告訴 OpenCV：「讀取時就變成灰階。」程式若讀不到圖會停下來提示，而不會繼續處理空的資料。

```python
from pathlib import Path
import cv2

folder = Path(__file__).resolve().parent
image = cv2.imread(str(folder / 'objects-board.png'), cv2.IMREAD_GRAYSCALE)
if image is None:
    raise RuntimeError('Cannot read image; check path')
print('gray shape:', image.shape)
print('gray dtype:', image.dtype)
print('saved:', cv2.imwrite(str(folder / 'gray-output.png'), image))
cv2.namedWindow('Gray image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Gray image', 800, 450)
cv2.imshow('Gray image', image)
print('Window open: press any key or wait 60 seconds', flush=True)
cv2.waitKey(60000)
cv2.destroyAllWindows()
print('Window closed')
```

## 第三步：執行，並用眼睛比較

確認資料夾中沒有需要保留的 `gray-output.png`；程式會寫入這個檔名。選好第 14 課的環境後按綠色 Run，你應看見灰階圖。點一下圖片視窗，再按任意鍵，或等待 60 秒讓視窗結束。

![RP5 上 Thonny 與灰階圖片視窗的原始實測](./圖檔/lesson17-trixie-thonny-window-20261110.jpg)

先前既有 Trixie 的實際輸出是：

```text
gray shape: (675, 1200)
gray dtype: uint8
saved: True
Window open: press any key or wait 60 seconds
Window closed
```

`675` 是圖片高度、`1200` 是寬度；灰階的每個位置只需要一個亮度值，所以沒有彩色陣列最後的 `3`。`saved: True` 表示 OpenCV 回報已完成存檔。

## 第四步：回到資料夾，找出留下來的作品

在 RP5 的檔案管理員打開同一個練習資料夾，找到 `gray-output.png`。把它與原本的 `objects-board.png` 都打開，觀察蘋果、香蕉和杯子的差別。

![先前由相同素材產生的灰階結果](./圖檔/lesson17-camera-gray.png)

試著說出兩件事：哪些形狀還看得出來？哪些顏色已經無法直接分辨？灰階常能幫助後續找邊界，但若任務是找紅色物件，就需要保留顏色資訊。

## 如果圖片沒有出現

若看到讀圖失敗，先用檔案管理員核對兩個檔案是否放在一起，圖片是否真的叫 `objects-board.png`。若出現找不到 `cv2`，先看 Thonny 是否仍選著第 14 課的環境。若存檔成功但沒有視窗，確認是在 RP5 的圖形桌面執行，再和老師查看完整顯示錯誤。更多例子在[排錯故事](./程式卡住時怎麼辦.md)。

## 換成自己的照片

先把自己的照片另存到新的練習資料夾，修改程式中輸入與輸出檔名再試一次。執行前先猜哪一部分在灰階下會比較難辨認，完成後再用結果解釋。這是延伸練習，需要記錄自己的實際輸出。

## 給教師的版本與實測備註

圖片、視窗與輸出沿用 2026-11-10 既有 Trixie／OpenCV 4.12.0 證據；2026-11-11 修正下載程式寫死的 `/tmp` 路徑，改由程式所在資料夾讀圖，並重新編排教學。路徑調整只完成本機靜態檢查，尚未在 RP5 重跑；不能當作新實機測試。[編修前完整紀錄](./歷史紀錄/第17課-編修前-20261111.md)保留原始實驗。
