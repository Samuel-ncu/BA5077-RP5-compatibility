# 第 39 課｜YOLOv8 與 COCO 資料集完整教學

[原始文章](https://liusming.pixnet.net/blog/posts/14222888508) · 更新日期：2026-10-29

> **部分實測。** 既有 Trixie 的 Thonny 已建立 CPU 環境、以 COCO8 跑一回合訓練並重新載入權重；完整 COCO 訓練與全新系統安裝仍待驗證。[逐篇進度](./Thonny逐篇實測狀態.md) · [素材下載說明](./練習素材/素材下載與使用.md)

## 學習目標

理解資料集、模型與類別名稱的關係；使用 Thonny 下載並載入 YOLOv8n，讀取類別資料。

## 背景與理論

COCO 提供影像與物件標註，是訓練及評估模型時可用的資料集。訓練後的模型將學到的參數保存在模型檔；本例的 `yolov8n.pt` 含有類別名稱。讀取這份名稱只能證明模型可載入，**不能證明已下載完整資料集，也不能代表辨識準確率**。

物件偵測除了回答「是什麼」，還要給出圖片中的位置。下一課會以一張照片練習。

## 事前準備

先前測試使用已存在的 `/home/pi/myenv/bin/python3`，Python 3.11.2、Ultralytics 8.3.50、PyTorch 2.5.1。它同時含有不同 OpenCV 發行套件；它只代表這台機器當時可執行，**不是已驗證可從零重現的乾淨安裝方案**。2026-11-10 在既有 Trixie 另建 CPU 環境的測試見下文；第 25–38 課的 OpenCV 環境不等同此 YOLO 環境。

使用已具備 YOLO 套件的環境時，在 Thonny 選擇「工具 → 選項 → 直譯器」，選擇該環境的 Python。下載模型時需要網路。

## 下載模型及範例

1. 依[素材下載與使用說明](./練習素材/素材下載與使用.md)下載並解壓本倉庫；建立一個新的練習資料夾，將[模型下載程式](./範例程式/第39課-Thonny下載YOLOv8模型.py)和[第 39 課程式](./範例程式/第39課.py)複製進去。
2. 在 Thonny 使用「檔案 → 開啟」開啟下載程式，按綠色執行鈕。它從 Ultralytics 的 GitHub 版本資產下載 `yolov8n.pt` 到程式所在的練習資料夾。為避免覆蓋，若檔案已存在請改用新資料夾；下載中斷時請檢查不完整檔案。
3. 本次下載的檔案大小為 6,549,796 bytes，SHA-256 為 `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`。檔案由上游提供，不包含在本倉庫。

本機 Thonny 的下載輸出：

```text
Downloading: yolov8n.pt
Saved: yolov8n.pt bytes: 6549796
Download complete.
```

![Thonny 下載 YOLOv8 模型的實際畫面](./圖檔/lesson39-download-thonny.png)

## 在 Thonny 載入模型

在同一資料夾開啟 `第39課.py`，按綠色執行鈕：

```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
print('class count', len(model.names))
print('class 0', model.names[0])
```

本次 Shell 中最後的輸出如下，首次載入可能另有套件設定提示：

```text
class count 80
class 0 person
```

![Thonny 載入模型並列印類別的實際畫面](./圖檔/lesson39-thonny.png)

模型列出 80 個類別，第 0 類名稱是 person。輸出的是模型內的名稱，尚未對人像做推論。

## 既有 Trixie：建立 CPU 環境與 COCO8 單回合實測（2026-11-10）

本節使用既有 Debian 13 Trixie／Python 3.13.5，並非全新系統。原文的完整 COCO 訓練量大；本次採 [Ultralytics COCO8](https://docs.ultralytics.com/datasets/detect/coco8/) 小型測試資料：4 張訓練圖、4 張驗證圖，僅跑 **1 個 epoch**，用來檢查下載、訓練、驗證及權重載入流程，不能代表完整 COCO 結果或模型實際準確率。資料和預訓練權重由上游下載，本倉庫不重新發布圖片或權重；使用與再散布前請查核 COCO 圖片各自的授權及 [Ultralytics 授權](https://www.ultralytics.com/license)。

### 1. 在 Thonny 建立獨立 CPU 環境

1. 準備網路與足夠空間，下載[環境建立程式](./範例程式/Thonny建立TrixieYOLOCPU環境.py)。在 Thonny 開啟後，將 `folder` 改成自己主目錄下**不存在**的資料夾；程式遇到已存在路徑會停止，不應刪除別人的環境。
2. 按 Run。程式先以系統 Python 建立隔離 venv，再從 [PyTorch 官方 CPU 套件來源](https://pytorch.org/get-started/locally/)安裝本次測試的 CPU 版本，最後以 pip 安裝 Ultralytics。下載可能耗時；只在 Shell 出現 `Environment ready` 才代表安裝程式結束。版本與套件供應可能改變，安裝失敗時保留錯誤並改用新的目錄重試。
3. 選 **Run → Configure interpreter**，選新環境的 `bin/python3`。本機路徑為 `/home/pi/ba5077-yolov8-cpu-trixie-20261110/bin/python3`；你的路徑可不同。

```python
from pathlib import Path
import subprocess

folder = Path('/home/pi/ba5077-yolov8-cpu-trixie-20261110')
if folder.exists():
    raise RuntimeError('Environment folder already exists; choose another')
subprocess.run(['/usr/bin/python3', '-m', 'venv', str(folder)], check=True)
python = str(folder / 'bin/python3')
subprocess.run([python, '-m', 'pip', 'install', 'torch==2.15.0+cpu', 'torchvision==0.29.2+cpu', '--index-url', 'https://download.pytorch.org/whl/cpu'], check=True)
subprocess.run([python, '-m', 'pip', 'install', 'ultralytics'], check=True)
print('Environment ready:', folder, flush=True)
```

本次取得 Ultralytics 8.4.208、PyTorch 2.15.0+cpu、torchvision 0.29.2+cpu、OpenCV 5.0.0、NumPy 2.5.4；版本匯入確認由終端機完成，訓練與權重推論由 Thonny 執行。安裝程式使用未固定版本的 `ultralytics`，日後解析到的套件可能不同，應記錄實際版本。第一次未指定 CPU 來源時套件管理器開始解析 CUDA 相依項，因此中止；下圖及上述結果是後續新建 CPU 環境的成功紀錄，未把先前未完成的環境算作成功。

![既有 Trixie 的 Thonny 建立 YOLO CPU 環境](./圖檔/lesson39-trixie-cpu-install-20261110.png)

### 2. 下載小型資料集並訓練

把[單回合程式](./範例程式/第39課-ThonnyCOCO8單回合.py)放入新練習資料夾，用上述環境在 Thonny 開啟並按 Run。首次需網路下載 `yolov8n.pt` 與 COCO8；程式將本次設定、資料集及訓練結果放在練習目錄內。若再執行，Ultralytics 可能建立帶編號的新結果資料夾；勿覆寫需保留的結果。本次預訓練模型 SHA-256 為 `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`。

```python
from pathlib import Path
import os

folder = Path(__file__).resolve().parent
config = folder / 'ultralytics-config'
config.mkdir(exist_ok=True)
os.environ['YOLO_CONFIG_DIR'] = str(config)

from ultralytics import YOLO, settings
import torch
import ultralytics

settings.update({'datasets_dir': str(folder / 'datasets'), 'sync': False})
print('Ultralytics:', ultralytics.__version__, flush=True)
print('PyTorch:', torch.__version__, 'CUDA available:', torch.cuda.is_available(), flush=True)
model = YOLO(str(folder / 'yolov8n.pt'))
print('class count:', len(model.names), 'class 0:', model.names[0], flush=True)
results = model.train(data='coco8.yaml', epochs=1, imgsz=320, batch=1,
                      workers=0, device='cpu', amp=False, plots=False,
                      project=str(folder / 'runs'), name='coco8-one-epoch', exist_ok=False)
save_dir = Path(model.trainer.save_dir)
print('training directory:', save_dir, flush=True)
print('best weights exist:', (save_dir / 'weights' / 'best.pt').is_file(), flush=True)
print('last weights exist:', (save_dir / 'weights' / 'last.pt').is_file(), flush=True)

```

程式印出本次結果目錄，並檢查 `weights/best.pt`、`weights/last.pt`。本次 Thonny 最後輸出節錄：

```text
training directory: /tmp/ba5077-lesson39-bKGVW7/runs/coco8-one-epoch
best weights exist: True
last weights exist: True
```

![既有 Trixie 的 Thonny 完成 COCO8 單回合並檢查權重](./圖檔/lesson39-trixie-coco8-train-20261110.png)

本次實際下載後核對到 4 張訓練圖與 4 張驗證圖；訓練輸出包含驗證統計與 `results.csv`，但樣本太少，不應把這些數字當成正式評估。預訓練模型、下載的資料集與輸出權重均留在測試設備，未納入公開 repo。

### 3. 重新載入權重

將[權重驗證程式](./範例程式/第39課-ThonnyCOCO8權重驗證.py)放在同一練習資料夾，在 Thonny 按 Run。它讀取上一步第一個 `runs/coco8-one-epoch/weights/best.pt` 及資料集的一張驗證圖片；如果你的結果目錄被自動加上編號，請修改 `weights` 路徑。圖片與輸出可能不同，這只是測試檔案能重新載入並執行推論，不是獨立測試集的準確率。

```python
from pathlib import Path
import os
folder = Path(__file__).resolve().parent
os.environ['YOLO_CONFIG_DIR'] = str(folder / 'ultralytics-config')
from ultralytics import YOLO

weights = folder / 'runs/coco8-one-epoch/weights/best.pt'
image = folder / 'datasets/coco8/images/val/000000000036.jpg'
model = YOLO(str(weights))
results = model.predict(source=str(image), imgsz=320, device='cpu', verbose=False, save=False)
print('weights loaded:', weights.is_file())
print('images processed:', len(results))
print('image shape:', results[0].orig_shape)
print('detections:', len(results[0].boxes))
print('classes:', [results[0].names[int(c)] for c in results[0].boxes.cls])
```

本次實際輸出：

```text
weights loaded: True
images processed: 1
image shape: (640, 481)
detections: 3
classes: ['umbrella', 'person', 'handbag']
```

![既有 Trixie 的 Thonny 重新載入權重並執行推論](./圖檔/lesson39-trixie-coco8-verify-20261110.png)

練習：觀察資料夾中圖片與標註檔的對應名稱，解釋為何驗證資料應與訓練資料分開；再比較不同輸入大小或 epoch 的結果。若下載失敗，確認網路、檔案與資料夾；如果環境未完成，不要把它標為已驗證。完整 COCO 下載、長時間訓練、原文自訂資料及全新系統仍需另行驗收。

## 練習與後續應用

1. 將 `model.names[0]` 改為其他編號，觀察名稱；超出可用編號會發生什麼事？
2. 用自己的話區分訓練資料、模型檔和模型推論結果。為什麼只有類別名稱無法保證測試圖片一定會被正確辨識？
3. 延伸到物品盤點前，需要蒐集適用場景的測試圖片，並比較漏檢與誤檢。

參考：[Ultralytics COCO 資料集文件](https://docs.ultralytics.com/datasets/detect/coco/)。

## 與原文章的差異

- 本版改用 RP5 CPU 與 Thonny 操作，未採原文 CUDA 安裝流程。
- 已在既有 Trixie 增加 COCO8 單回合下載、訓練、驗證與重新推論；完整 COCO 及原文自訂資料流程尚未全部重做。
- 增加既有 Trixie 的 CPU 環境安裝、訓練和權重驗證截圖；全新重灌系統安裝仍待驗證。
