# 補充 4｜📸 Raspberry Pi 5 + PiCamera2 + MediaPipe Face Mesh 教學（支援 468 點臉部特徵點）

[原始文章](https://liusming.pixnet.net/blog/posts/14223033921) · 更新日期：2026-10-29

## 學習目標

以 MediaPipe Face Mesh 處理一張 Pi 相機影格。

## 事前準備

需要 PiCamera2、相機及 MediaPipe 0.10.9 虛擬環境。

MediaPipe 的已測試安裝方式請看[安裝操作與實測紀錄](../安裝操作與實測紀錄.md#5-mediapipe-手勢與-face-mesh)。不同專案請使用獨立環境。

## 程式與執行

將以下程式存為 `補充4.py`，或使用[已測試的範例程式](./範例程式/補充4.py)。在檔案所在目錄執行 `python3 補充4.py`。

```python
import cv2
import mediapipe as mp
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={'size': (320, 240), 'format': 'RGB888'}))
    camera.start()
    frame = camera.capture_array()
finally:
    camera.stop()
    camera.close()
with mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as mesh:
    result = mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
print('frame processed', result is not None)
```

## 本機實際輸出

```text
frame processed True
```

成功處理影格不代表一定偵測到臉部或 468 點；真人追蹤、顯示與精度未測。

## 背景與核心概念

### 臉部特徵點和身分辨識

臉部特徵點估計眼睛、鼻子等區域的位置；點的數量與 API／模型版本有關。特徵點不等於臉部身分，也不保證每個姿勢與光線都能正確定位。

### 思考、練習與後續應用

偵測到臉、估計臉部特徵點與辨識身分有何差別？為何空畫面測試不能證明人臉結果？

可用於互動展示；實際人臉影像可能是敏感資料，需事先確認使用目的與授權。

進一步閱讀：[相關官方文件](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker)。請以下方實測狀態為準；尚未實作或測試的情境不能視為已通過。

## 概念流程圖

```mermaid
flowchart LR
    A["經授權的人臉影像"]
    B["臉部特徵點模型"]
    C["特徵點座標"]
    D["視覺化或分析"]
    A --> B --> C --> D
```

此圖用於說明文章的概念或完整目標流程，**不是操作截圖，也不代表每個步驟都已實測**；本機實測範圍請看文章中的標示。

## 與原文章的差異

- 原文即時臉部網格在本版先縮小成可驗證的單張流程，並不宣稱 GUI 與完整模型表現已通過。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
- 加入教學流程示意；圖中的完整目標流程不代表已逐步實測。
