# 補充 11｜🎯 Raspberry Pi 5 上使用 EAST + Tesseract 進行即時文字辨識（含 PiCamera2 即時預覽）

[原始文章](https://liusming.pixnet.net/blog/posts/14223038385) · 更新日期：2026-10-29

## 學習目標

以 Tesseract 辨識自行產生的英文測試圖片。

## 事前準備

需要已安裝的 Tesseract、pytesseract 與 DejaVu Sans 字型。

依[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#6-tesseract-ocr)建立 OCR 環境；本機的 Tesseract 已安裝。

## 程式與執行

將以下程式存為 `補充11.py`，或使用[已測試的範例程式](./範例程式/補充11.py)。在檔案所在目錄執行 `python3 補充11.py`。

```python
from PIL import Image, ImageDraw, ImageFont
import pytesseract

image = Image.new('RGB', (600, 120), 'white')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 48)
draw.text((15, 15), 'HELLO 123', font=font, fill='black')
result = pytesseract.image_to_string(image, config='--psm 7').strip()
print('OCR:', result)
```

## 本機實際輸出

```text
OCR: HELLO 123
```

英文合成文字成功辨識；本機目前只有 eng、osd 語言資料。此例不含 EAST 偵測、相機即時影像或中文辨識。

## 與原文章的差異

- 原文結合 EAST、Tesseract 與相機；本版先隔離驗證 OCR，完整即時整合與中文仍待測試。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
