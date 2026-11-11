# 第 13 課｜Raspberry Pi 使用攝影機完整指南

[原始文章](https://liusming.pixnet.net/blog/posts/14222876433) · 更新日期：2026-10-29

在拍照前，先讓我們看見相機現在看到什麼。你會先確認相機，再開一個短暫的預覽，觀察結束後相機是否能繼續使用。

第一次準備環境的同學，可以先讀[課前學習說明](./學習前先讀我.md)；操作遇到紅字時，我們用[排錯故事](./程式卡住時怎麼辦.md)一起找原因。

如果你使用 Trixie，我們先從[這一套系統的練習](#2026-11-10既有-trixie-的限時相機預覽)開始；前後的舊版例子可留到比較時閱讀。

## 學習目標

1. 認識 Picamera2 的建立、啟動、擷取與釋放流程（先只取一張影格）。
2. 在 Thonny 開一個限時預覽，確認結束後相機能再次使用。
3. 用終端機的 `rpicam-vid` 錄一段 5 秒影片，用 `ffprobe` 與 OpenCV 檢查影片是否完整；並知道為什麼 RP5 的 CSI 相機不用 `VideoCapture(0)` 直接讀取（見[錄影一節](#2026-11-11用終端機錄一段影片rpicam-vid)）。

## 背景與原理

攝影機能把光線轉換成影像資料，供人觀看或讓程式分析。RP5 可搭配相機模組，透過相機軟體取得畫面；這台機器實際使用的是 IMX708 廣角相機。CSI 相機與 USB 攝影機的裝置介面可能不同，不能因某一種能用就假設另一種使用相同程式。

Picamera2 是 Python 使用 Raspberry Pi 相機的介面。先設定影格大小，再啟動相機並擷取資料，最後停止、釋放資源；如果另一個程式正佔用相機，新的程式可能無法啟動。[官方相機軟體文件](https://www.raspberrypi.com/documentation/accessories/camera-software.html)說明相機連接與相關工具。

```mermaid
flowchart LR
    A[相機感測光線] --> B[相機系統處理影像]
    B --> C[Picamera2 擷取影格]
    C --> D[Python 分析或保存]
```

這是概念圖，不是操作截圖。影格就是某一時刻的一張影像；連續取得多張影格則可形成影片。

## 事前準備

相機已連接，系統 Python 可以匯入 Picamera2。

請在自己的練習目錄操作。已存在的同名輸出檔可能被覆寫，先確認路徑；用不著將任何相機照片上傳公開儲存庫。

## 程式與執行

將下列程式存為 `第13課.py`。這是本次在 RP5 上執行的程式；完整檔案也在[範例程式](./範例程式/第13課.py)。

```python
from picamera2 import Picamera2

camera = Picamera2()
try:
    camera.configure(camera.create_still_configuration(main={"size": (320, 240), "format": "RGB888"}))
    camera.start()
    frame = camera.capture_array()
    print("camera", frame.shape, str(frame.dtype))
finally:
    camera.stop()
    camera.close()
```

在 Thonny 選 **File → Open** 開啟 `第13課.py`，確認右下角是包含所需套件的 Python 環境，再點綠色執行鈕。若程式會輸出檔案，先在新的練習目錄操作，避免覆寫。

## Thonny 實測輸出

```text
camera (240, 320, 3) uint8
```

![第 13 課在 Thonny 的程式與 Shell 實際畫面](./圖檔/lesson13-thonny2.png)

本次選用既有環境 `/home/pi/myenv/bin/python3`。相機格式與影格尺寸已在 Thonny 重新測試；連續錄影及 USB 相機尚待測。 相機或影像相關套件的準備及可重現環境請參考[Thonny 環境指南](./Thonny環境與套件安裝.md)。

影格是高度 240、寬度 320 的三通道陣列；`uint8` 是每個通道的資料型別。這不代表圖形預覽或 USB 攝影機已測試。

## 練習與應用

1. 說明輸出 `(240, 320, 3)` 的高度、寬度與通道數；它與設定的 `(320, 240)` 為何順序不同？
2. 檢查目前是否有其他相機程式佔用裝置，然後再執行範例。
3. 延伸至第 18 課，將影格存成照片；再思考哪些拍攝內容不適合直接公開。

相機擷取可用在影像監測或產品檢測；要得到可信結果，還須驗證光線、拍攝位置、畫質、隱私和錯誤處理。

## 2026-11-10：既有 Trixie 的限時相機預覽

本次使用現有 Trixie、Thonny 的系統 Python `/usr/bin/python3`（3.13.5）及系統 Picamera2，使用已連接的 CSI 相機；這不是新重灌系統。已另外確認第 12 課的獨立 `opencv-course-env` 無法匯入 Picamera2，不能因為 OpenCV 可用就假設相機套件也在該環境。相機須可用且不能被其他程式佔用。

1. 在 RP5 的圖形桌面啟動 Thonny，開啟 **Tools → Options → Interpreter**，選擇包含 Picamera2 的解譯器；本次選系統 `/usr/bin/python3`。確認選擇後在 Shell 測 `from picamera2 import Picamera2`；若匯入失敗，先確認環境與套件，不要在系統 Python 隨意執行 pip。
2. 在新檔輸入下列程式或開啟[完整範例](./範例程式/第13課-限時相機預覽.py)，再按 F5 或綠色執行鈕。桌面支援 Qt 預覽時會出現畫面，約 20 秒後關閉；第一次觀看前請確認相機不會拍到不願公開的內容。

```python
from picamera2 import Picamera2, Preview
from time import sleep

camera = Picamera2()
try:
    camera.configure(camera.create_preview_configuration(main={'size': (640, 480)}))
    camera.start_preview(Preview.QTGL)
    camera.start()
    print('Preview started for 20 seconds', flush=True)
    sleep(20)
finally:
    camera.stop()
    camera.stop_preview()
    camera.close()
print('Camera closed')
```

本次 Thonny 顯示的程式輸出為：

```text
Preview started for 20 seconds
Camera closed
```

相機函式庫另外印出裝置資訊、V4L2 格式警告及 Qt 執行目錄權限警告；此次預覽視窗仍有顯示並自動關閉。第二次執行也顯示上述兩行並結束；結果依圖形環境和相機而異。`finally` 區塊會嘗試停止並釋放相機；若初始化中途失敗，清理呼叫仍可能產生錯誤，請保留完整錯誤訊息排查。

![限時預覽結束後的 Thonny 程式與輸出](./圖檔/lesson13-trixie-preview-end-20261110.jpg)

*圖：實際 Thonny 執行結果；相機預覽已結束。因本次預覽拍到含帳號資訊的螢幕，未公開預覽畫面；不含個資的預覽成果圖仍待補。* 這項測試未驗證錄影或 USB 攝影機。若沒有預覽，檢查是否在圖形桌面、相機是否被佔用、選對 Picamera2 環境及實際錯誤訊息；不要假設不同解譯器套件相同。

## 2026-11-11：用終端機錄一段影片（rpicam-vid）

前面我們用 Python 一次拿一張影格。原文的做法是先用系統內建的錄影指令把相機畫面錄下來；在現在的 Raspberry Pi OS（Trixie）中，這個指令叫 `rpicam-vid`，舊文章寫的 `libcamera-vid` 是它以前的名字。錄影不是 Python 程式，所以這一段用**終端機**操作，不用 Thonny。

**為什麼要學這一段：**有時候我們只想先錄一段畫面，之後再慢慢用 Python 分析；或想確認「相機本身沒問題」，把相機和自己的程式分開排錯。

### 步驟 1：確認相機被系統看見

在 RP5 桌面左上角開啟**終端機**（黑色視窗圖示），輸入下面這行後按 Enter：

```bash
rpicam-hello --list-cameras
```

本次輸出（只節錄開頭）：

```text
Available cameras
-----------------
0 : imx708_wide [4608x2592 10-bit RGGB] (/base/axi/pcie@1000120000/rp1/i2c@88000/imx708@1a)
    Modes: 'SRGGB10_CSI2P' : 1536x864 [120.13 fps - (768, 432)/3072x1728 crop]
                             2304x1296 [56.03 fps - (0, 0)/4608x2592 crop]
                             4608x2592 [14.35 fps - (0, 0)/4608x2592 crop]
```

`0 : imx708_wide` 表示系統找到一台編號 0 的相機，型號 IMX708 廣角。下面的 `Modes` 是感測器支援的尺寸和最快每秒張數。如果顯示 `No cameras available!`，先回到[第 07 課](./第%2007%20課｜連接%20Raspberry%20Pi%205%20相機模組.md)檢查排線；也確認沒有其他程式正在用相機。

### 步驟 2：錄 5 秒影片

先建立練習資料夾並進去，再錄影：

```bash
mkdir -p ~/lesson13
cd ~/lesson13
rpicam-vid -n -t 5000 --width 1280 --height 720 --framerate 30 --codec libav -o lesson13-test.mp4
```

每個部分的意思：

| 參數 | 意思 |
| --- | --- |
| `-n` | 不開預覽視窗。拿掉它就會在桌面看到即時畫面，但用 SSH 等沒有桌面的連線時會出錯。 |
| `-t 5000` | 錄 5000 毫秒，也就是 5 秒；時間到自動停止。 |
| `--width 1280 --height 720` | 影片寬 1280、高 720。 |
| `--framerate 30` | 請相機每秒給 30 張。 |
| `--codec libav -o lesson13-test.mp4` | 用軟體編碼成 H.264，存成 MP4。RP5 沒有硬體 H.264 編碼器，所以要指定 `libav`。 |

錄影前先看一下鏡頭對著什麼：**影片會存下鏡頭看到的一切**，不要對著帳號、訊息或他人臉孔。若 `~/lesson13` 裡已有 `lesson13-test.mp4`，會被覆寫。

本次執行時，終端機會印出許多以 `[` 開頭的相機日誌，最後幾行是：

```text
Output #0, mp4, to 'lesson13-test.mp4':
  Stream #0:0: Video: h264, yuv420p(tv, bt709), 1280x720, q=2-31, 30 fps, 30 tbr, 1000k tbn
Halting: reached timeout of 5000 milliseconds.
```

`Halting: reached timeout` 表示 5 秒到了、正常停止，不是錯誤。

### 步驟 3：檢查影片是否真的錄好

用 `ffprobe` 查看影片資訊：

```bash
ls -l lesson13-test.mp4
ffprobe -v error -show_entries stream=codec_name,width,height,avg_frame_rate,nb_frames:format=duration,size -of default=nw=1 lesson13-test.mp4
```

本次輸出：

```text
-rw-rw-r-- 1 pi pi 780793 Nov 11 17:48 lesson13-test.mp4
codec_name=h264
width=1280
height=720
avg_frame_rate=3550000/118281
nb_frames=142
duration=4.731239
size=780793
```

怎麼讀這些數字：檔案約 0.78 MB、H.264 編碼、1280 × 720。`nb_frames=142` 是錄到 142 張；`avg_frame_rate` 是分數，3550000 ÷ 118281 ≈ 30.0，表示平均每秒約 30 張。`duration` 約 4.7 秒而不是剛好 5 秒，是因為相機啟動和曝光穩定花了一點時間，前面的空檔沒有影格。你的數字可能略有不同；只要 `nb_frames` 不是 0、`width` 和 `height` 正確，就代表錄影成功。

也可以在檔案管理員雙擊 `lesson13-test.mp4`，用系統播放器播放。本次沒有截取播放器畫面。

![RP5 相機當時拍到的畫面](./圖檔/lesson13-camera-view-20261111.jpg)

上圖是錄影後緊接著用 `rpicam-still -n -t 1000 --width 1280 --height 720 -o lesson13-frame.jpg` 拍的一張照片，用來讓你知道本次相機看到什麼：鏡頭對著另一個實體螢幕上的測試畫面，深色圓形當時是靜止的。這是相機實拍照片，不是預覽視窗截圖；影片本身沒有上傳到教材庫。

### 步驟 4：用 Python 讀回影片，以及為什麼不要用 `VideoCapture(0)`

原文接著用 OpenCV 的 `cv2.VideoCapture(0)` 直接開相機。**在 RP5 的 CSI 相機上，這條路通常走不通**：本次在 `opencv-course-env` 測試，`VideoCapture(0)` 回報「已開啟」，但讀第一張就失敗：

```text
VideoCapture(0) opened True read False None
```

原因是 RP5 的 CSI 相機要經過 libcamera 處理，`/dev/video0` 不是 OpenCV 能直接讀的一般攝影機。所以本教材讀**相機**用 Picamera2（本課上方、第 15 課），讀**影片檔**才用 `VideoCapture`。在 Thonny 選第 14 課的 OpenCV 環境，於 `~/lesson13` 建立下面的程式並執行：

```python
import cv2

video = cv2.VideoCapture("lesson13-test.mp4")
print("opened", video.isOpened(), "fps", round(video.get(cv2.CAP_PROP_FPS), 2))
count = 0
shape = None
while True:
    ok, frame = video.read()
    if not ok:
        break
    count += 1
    shape = frame.shape
video.release()
print("frames read", count, "shape", shape)
```

本次以 SSH 用 `/home/pi/opencv-course-env/bin/python3` 執行（與 Thonny 相同直譯器，但不是在 Thonny 按 Run）的輸出：

```text
opened True fps 30.01
frames read 142 shape (720, 1280, 3)
```

讀回 142 張，和 `ffprobe` 的 `nb_frames=142` 相同，代表 OpenCV 能完整讀取這支影片。之後第 16 課會把「拍攝」和「處理」寫進同一支 Python 程式。

### 錄影時遇到問題

| 你看到的情況 | 可能原因 | 先試試看 |
| --- | --- | --- |
| 錯誤訊息提到 `in use`、`busy` 或相機無法取得 | Thonny 或其他程式正在用相機 | 先停止其他相機程式（Thonny 按紅色 Stop），再錄一次。 |
| 錯誤訊息提到 encoder 或 `h264` | 沒有加 `--codec libav` | RP5 沒有硬體 H.264 編碼器，請加上 `--codec libav`。 |
| 用 SSH 連線時出現與 display、預覽視窗有關的錯誤 | 沒加 `-n`，程式想開預覽視窗 | SSH 時加 `-n`；想看預覽請在 RP5 桌面的終端機執行。 |
| `nb_frames` 比預期少很多 | 解析度或每秒張數太高，軟體編碼跟不上 | 先改成 `--width 640 --height 480 --framerate 15` 比較。 |

### 練習

1. 把 `-t 5000` 改成 `-t 10000`，預測 `nb_frames` 大約多少，再用 `ffprobe` 驗證。
2. 把 `--framerate 30` 改成 `--framerate 10`，比較檔案大小與 `nb_frames`。
3. 拿掉 `-n`，在 RP5 桌面的終端機錄一次，觀察預覽視窗；確認畫面中沒有不能公開的內容。

USB 攝影機的錄影方式不同，本機沒有 USB 攝影機，這部分尚未實測。

## 與原文章的差異

- 2026-11-11 新增 `rpicam-vid` 終端機錄影主線：列出相機、錄 5 秒 1280 × 720 H.264、`ffprobe` 檢查 142 影格約 30 FPS、OpenCV 讀回 142 張，並實測原文 `VideoCapture(0)` 在 RP5 CSI 相機上讀不到影格；附可公開的相機實拍畫面。編修前版本存於[歷史紀錄](./歷史紀錄/第13課-編修前-20261111.md)。
- 新增以 Thonny 操作的實測與截圖：Picamera2 單張影格擷取；不含預覽或 USB 相機。

- 原文以持續執行的 `libcamera-vid` 接著使用 `VideoCapture(0)`；本版採 Picamera2 單張擷取，避免阻塞並配合本機 CSI 相機。
- 上述文字輸出是本次實機紀錄，其他版本或環境可能不同。
- 新增既有 Trixie 的限時 Qt 預覽與重開測試；可公開的預覽畫面、錄影和 USB 相機仍待補。

<details>
<summary>給教師：原有實測範圍與版本備註</summary>

> 本課已在 Thonny 實測：Picamera2 單張影格擷取；不含預覽或 USB 相機。完整原文情境及其他舊案例仍須依下文標示重測。
>
> 2026-11-11 錄影一節：既有 Trixie、rpicam-apps v1.14.0，從另一台電腦以 SSH 執行於 `/home/pi/ba5077-validation-20261111/lesson13/`；影片 SHA-256 `c9221320…1a72`，未入庫。錄影時相機對著螢幕上靜止的測試畫面；`--codec libav` 錄 5 秒得 142 影格。表中的錯誤訊息是常見類型的描述，本次未逐一重現。待補：桌面終端機不加 `-n` 的預覽、播放器畫面、USB 攝影機（需額外硬體）。[逐篇進度](./Thonny逐篇實測狀態.md) · [圖片與程式下載方式](./練習素材/素材下載與使用.md)

</details>
