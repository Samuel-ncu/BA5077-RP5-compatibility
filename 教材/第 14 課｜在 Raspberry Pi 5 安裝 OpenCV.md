# 第 14 課｜在 Raspberry Pi 5 安裝 OpenCV

> **Trixie 狀態：**Trixie 64 位元為主要教學版本；本文列出的舊系統操作或輸出不可視為 Trixie 已驗收。請以[基線與測試矩陣](./乾淨系統基線與測試矩陣.md)查看已測與待補範圍。
[原始文章](https://liusming.pixnet.net/blog/posts/14222877021) · 更新日期：2026-11-05 · [目前測試基線](./乾淨系統基線與測試矩陣.md)

> **Trixie 主流程：**Raspberry Pi OS 64 位元、Debian 13 Trixie、Python 3.13.5；在新的虛擬環境使用 `opencv-python==4.12.0.88`。2026-10-29 的 Bookworm／OpenCV 4.10 紀錄不屬於本課目前的安裝步驟。

## 學習目標

完成本課後，你能在 Thonny 選對 Python 虛擬環境、安裝 OpenCV，並用程式建立、存檔及讀回一張影像。安裝成功只代表基本影像操作可用，不代表每個 OpenCV 擴充功能或相機功能都已通過。

## 背景：套件安裝到哪裡？

Python 是執行程式的工具，OpenCV 提供讀圖、繪圖和影像分析功能。Python 程式使用 `import cv2` 載入 OpenCV，但套件名稱是 `opencv-python`；安裝名稱和匯入名稱不同。

一台 Raspberry Pi 可以同時有系統 Python 和多個虛擬環境。若套件裝在 A 環境，Thonny 卻使用 B 環境，程式就會出現 `ModuleNotFoundError`。因此要一起檢查安裝輸出的 Python 路徑和 Thonny 右下角的 interpreter。

本課使用 venv 隔離課程套件。不要對 Raspberry Pi OS 系統 Python 執行 `sudo pip install`，也不要在同一個環境同時安裝 `opencv-python`、`opencv-python-headless` 或 `opencv-contrib-python`；它們都提供名為 `cv2` 的模組，混裝會讓載入結果難以判斷。

## 準備項目

- Raspberry Pi 5，安裝 Raspberry Pi OS Trixie 64 位元。
- 可連上網際網路，且根目錄有足夠空間下載 NumPy 與 OpenCV wheel。
- Thonny 使用 Raspberry Pi OS 原生安裝版本。
- 完成[乾淨系統基線檢查](./乾淨系統基線與測試矩陣.md)，確認系統 Python 為 Python 3.13.x，並記錄目前解譯器路徑。

乾淨基線上以系統 Python 執行 `python3 -c 'import cv2'` 預期會得到 `ModuleNotFoundError`。這是安裝前的比較點；請不要為了消除錯誤而把 OpenCV 裝進系統 Python。

## 操作步驟

1. 在 Thonny 選擇 **Tools → Options → Interpreter**，建立一個新的 virtual environment。選一個尚未存在的路徑，例如 `/home/pi/ba5077-opencv-20261105`。如果這個路徑已存在，換一個新名稱，不要刪除不熟悉的環境。
2. 在同一個 Interpreter 設定畫面選取新環境中的 `bin/python3`，按 **OK**。看 Thonny 右下角確認路徑包含 `ba5077-opencv-20261105`，再重新啟動 Shell backend。
3. 從 GitHub 下載[Thonny 安裝程式](./範例程式/第14課-Thonny安裝套件.py)，在 Thonny 開啟後先閱讀。它會印出目前的 Python 路徑、版本及架構；確認是新建的 venv、Python 3.13 和 `aarch64` 後，按綠色執行按鈕。
4. 等待 Shell 顯示 `Successfully installed` 與 `Installation completed`。這次安裝的版本為 `numpy==2.2.4` 和 `opencv-python==4.12.0.88`。安裝中斷時先讀錯誤訊息，不要在系統 Python 重試。
5. 重新啟動 Thonny backend，開啟[驗證程式](./範例程式/第14課-Trixie驗證.py)並執行。程式會畫一個綠色矩形、把影像編碼成 PNG，再讀回並存檔。請確認輸出圖片位於目前工作資料夾。

若 Thonny 無法建立 venv，可以在 RP5 終端機執行 `python3 -m venv ~/ba5077-opencv-20261105`，再回到 **Tools → Options → Interpreter** 選擇該資料夾中的 `bin/python3`。命令只建立新環境，不會修改系統 Python。

## 預期結果與實測範圍

Trixie/Python 3.13 的 RP5 環境已測得以下基本輸出：

```text
OpenCV module: 4.12.0
OpenCV wheel: 4.12.0.88
NumPy: 2.2.4
Image shape: (120, 160, 3)
Encode/decode: True
Saved: True
```

`Image shape` 依序代表影像高度、寬度、色彩通道數。`Saved: True` 表示 OpenCV 回報成功寫入檔案；請再用圖片檢視器打開檔案確認內容。已驗證的範圍是 venv 套件安裝、匯入、合成影像繪製、編碼／解碼和存檔。相機取像、GUI 視窗、影片與進階 OpenCV 模組另由相關課程驗收。

APT 模擬安裝 `python3-opencv` 會新增 72 個套件，因此本教材採用已測通的 PyPI wheel venv 流程。這是兩種安裝路徑的影響比較，不是宣稱 APT 套件有錯。

目前尚未保存一張符合本課 Trixie 主流程的 Thonny 安裝操作截圖。既有的 `lesson14-install-screenshot.png` 和 OpenCV 4.10 輸出屬於 Bookworm 歷史紀錄，不能放在本段冒充 Trixie 畫面；圖檔待以 RP5 Wayland 桌面重新擷取、裁切及檢查後補上。

## 常見錯誤

| 看到的情況 | 先檢查什麼 |
| --- | --- |
| `ModuleNotFoundError: No module named 'cv2'` | Thonny 右下角 interpreter 是否與剛才安裝時印出的路徑相同；是否已重新啟動 backend |
| `pip` 找不到符合版本的 wheel | 確認是 64 位元 Trixie、Python 3.13 和 `aarch64`；不要改裝來源不明的 wheel |
| `cv2` 匯入時出現 NumPy ABI 錯誤 | 檢查此 venv 是否混裝過不同 OpenCV 或 NumPy 版本；不要對系統套件做移除操作 |
| Thonny Shell 顯示安裝成功但程式仍找不到套件 | 安裝程式的 `Python:` 路徑和 Thonny 右下角應相同 |
| 圖片沒有出現在預期位置 | 程式使用相對路徑時，輸出會放在目前工作目錄；從 Thonny Shell 查看工作目錄或改用完整路徑 |

## 練習與延伸

1. 將矩形的顏色參數由 `(0, 255, 0)` 改成 `(0, 0, 255)`，比較 BGR 色彩順序對結果的影響。
2. 把輸出圖片寬度改成 320，並說明 `image.shape` 三個數字分別代表什麼。
3. 在新 venv 中執行 `python -m pip show opencv-python`，記錄套件版本和安裝位置。說明為什麼同一台 RP5 的系統 Python 仍可能找不到 `cv2`。
4. 搜尋 OpenCV 官方影像讀取教學，找出一個本課尚未測過的函式，寫下輸入、輸出和你想驗證的條件。

## 舊版差異與參考資料

Bookworm/Python 3.11 的歷史操作、OpenCV 4.10 輸出及 headless 測試請看[安裝與實測紀錄](../安裝操作與實測紀錄.md)的舊版章節。兩個版本的主流程分開記錄，避免將舊套件指令貼進 Trixie 課程。

- [OpenCV Python 套件](https://pypi.org/project/opencv-python/)
- [Python venv 官方文件](https://docs.python.org/3/library/venv.html)
- [Thonny 套件安裝說明](https://github.com/thonny/thonny/wiki/InstallingPackages)
- [GitHub Markdown 基本語法](https://docs.github.com/en/get-started/writing-on-github/basic-writing-and-formatting-syntax)
