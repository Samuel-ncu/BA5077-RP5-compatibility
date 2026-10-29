# 補充 8｜PiCamera2 + TensorFlow Lite (MobileNetV1) + 即時影像分類 + 顯示分類文字 的 完整教學

[原始文章](https://liusming.pixnet.net/blog/posts/14223038310) · 更新日期：2026-10-29

> **部分實測**：模型和標籤已在 Thonny 下載；下方分類輸出目前是 RP5 終端機實測，**尚未在 Thonny 重跑**。新環境安裝、即時分類與顯示待驗證。[逐篇進度](./Thonny逐篇實測狀態.md)

## 學習目標與背景

理解 MobileNet 圖像分類，並以相機拍攝後的單張圖片測試。即時攝影機和畫面文字顯示仍待完成。

圖像分類根據整張圖產生各類別分數；它與物件偵測不同，通常不提供物件位置。TFLite Interpreter 載入模型並配置輸入輸出張量，資料的尺寸、型別與模型必須一致。本例使用量化模型：輸出需依 scale 與 zero point 換算；標籤列表必須與模型對應。

## 環境與素材

本次沿用 RP5 的 `/home/pi/myenv/bin/python3`：Python 3.11.2、NumPy 1.24.2、`tflite_runtime` 2.14.0 及 OpenCV。從全新虛擬環境透過 Thonny 安裝上述套件尚未驗證。模型和標籤來自 TensorFlow；標籤網址追蹤上游 master，日後內容可能改變。

依[素材下載與使用說明](./練習素材/素材下載與使用.md)取得本倉庫，將[模型下載程式](./範例程式/補充3和8-Thonny下載模型.py)、[分類範例](./範例程式/補充3和8-Thonny照片分類.py)和[相機照片裁切圖](./圖檔/lesson24-camera-roi.png)放在同一個新練習資料夾。照片是 RP5 拍攝螢幕上的 AI 生成物件後裁切所得，不是真實水果。

## Thonny 模型下載：已實測

選擇含上述套件的直譯器，在 Thonny 開啟下載程式並按綠色執行鈕。程式下載 TensorFlow 的模型壓縮檔、取出需要的模型及下載標籤，並印出大小與 SHA-256。需要網路及可容納下載暫存檔的空間；若模型或標籤已存在，請改用新的資料夾。

本次 Thonny 輸出：

```text
Downloading model archive...
Downloading labels...
mobilenet.tflite bytes: 4276352 sha256: ecc3a67c47c5a609ec35f6a58a7d97532834e43df4cb7d3f1204a8164b7d20dd
labels.txt bytes: 10484 sha256: 536feacc519de3d418de26b2effb4d75694a8c4c0063e36499a46fa8061e2da9
Download complete.
```

![Thonny 下載分類模型及標籤的真實畫面](./圖檔/supp-tflite-download-thonny.png)

## 單張分類範例：終端機已測、Thonny 待重測

在同一資料夾準備好模型、標籤與圖片後，可在 Thonny 開啟以下範例並執行；**本次這一步尚未透過 Thonny 驗證**，不能把以下輸出視為 Thonny 實測結果。程式先讀取圖片、轉換色彩和尺寸，然後呼叫 Interpreter 並列出前三個類別：

```python
import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter

image = cv2.imread('lesson24-camera-roi.png')
if image is None:
    raise RuntimeError('找不到相機裁切圖 lesson24-camera-roi.png')
with open('labels.txt', encoding='utf-8') as f:
    labels = [line.strip() for line in f]
interpreter = Interpreter(model_path='mobilenet.tflite')
interpreter.allocate_tensors()
input_info = interpreter.get_input_details()[0]
output_info = interpreter.get_output_details()[0]
print('input shape:', tuple(input_info['shape']))
print('input dtype:', input_info['dtype'].__name__)
print('input quantization:', input_info['quantization'])
print('output quantization:', output_info['quantization'])
if tuple(input_info['shape']) != (1, 224, 224, 3) or input_info['dtype'] != np.uint8:
    raise RuntimeError('此程式預期 MobileNetV1 量化模型的 uint8 224x224 RGB 輸入')
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
rgb = cv2.resize(rgb, (224, 224))
interpreter.set_tensor(input_info['index'], np.expand_dims(rgb, axis=0))
interpreter.invoke()
raw = interpreter.get_tensor(output_info['index'])[0]
scale, zero = output_info['quantization']
scores = (raw.astype(np.float32) - zero) * scale
if len(labels) != len(scores):
    raise RuntimeError('標籤數與模型輸出數不一致')
for index in np.argsort(scores)[-3:][::-1]:
    print(f'top class: {index} {labels[index]} {scores[index]:.4f}')
```

同一程式及模型在這台 RP5 的終端機實際輸出：

```text
input shape: (1, 224, 224, 3)
input dtype: uint8
input quantization: (0.0078125, 128)
output quantization: (0.00390625, 0)
top class: 949 Granny Smith 0.3984
top class: 955 banana 0.1055
top class: 957 custard apple 0.0625
```

這些是模型對這張生成圖片給出的分數，不能用來確認水果品種或估計整體準確率。不同版本與輸入可能改變結果。

## 練習與後續應用

解釋為何模型需要 224 × 224 的輸入；比較分類結果與第 40 課的物件偵測框。準備其他圖片測試前，先確認標籤順序及模型輸出是否一致，再紀錄結果與人工觀察差異。

## 與原文章的差異

- 本版在 Thonny 實測模型下載；分類只完成終端機實測。原文的完整即時分類、畫面顯示與模型轉換尚未重做。
- 新增相機拍攝生成圖、模型和標籤下載方式及可核對的檔案資訊；乾淨環境安裝與 Thonny 分類待驗證。
