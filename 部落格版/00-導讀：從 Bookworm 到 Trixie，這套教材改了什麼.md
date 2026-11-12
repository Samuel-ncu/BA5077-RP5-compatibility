# 00｜導讀：從 Bookworm 到 Trixie，這套教材改了什麼

## 原課號：無（本篇為部落格版新增）

原始課程目錄：[BA5077 AIoT 產品發展實作（digithouse.net）](https://digithouse.net/ba5077-aiot-product-development?locale=zh-TW) · 教材 repo：[Samuel-ncu/BA5077-RP5-compatibility](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/README.md)

上學期有同學拿著自己剛燒好的 Raspberry Pi 5 來問我：「老師，我照文章打 `pip install mediapipe`，為什麼後面的程式一直說 `mp` 沒有 `solutions`？」我回頭一查才發現，不是他打錯，而是**他的系統和寫文章那時候已經不是同一代了**。原課程大多寫於 2025 年 4 月，那時我們用的是 Raspberry Pi OS Bookworm；現在手上的 RP5 跑的是 Trixie。很多指令還能用，有些改了名字，有些套件整個換了寫法。

這篇導讀先把「哪裡變了、我們怎麼確認的」講清楚，後面 56 篇你就知道哪些地方要特別留意。

## 這篇會學到什麼

- Bookworm 和 Trixie 是什麼，為什麼版本不同會讓同一段程式跑出不同結果。
- 這套教材實際遇到的幾個主要差異：Python、桌面與遠端桌面、OpenCV、MediaPipe、qiv、虛擬環境路徑、相機。
- 這次部落格版怎麼重新整理課程，以及「已實測」「尚未實測」的標示是什麼意思。

> **先講好規則**：本文每一點都附出處，出處只有兩種——這個 repo 裡的實測紀錄，或 Raspberry Pi／Debian／PyPI 的官方發行資料。找不到根據的事，我就不寫。

## 先認識兩個名字：Bookworm 與 Trixie

**Raspberry Pi OS** 是 Raspberry Pi 官方的作業系統，它是以 **Debian**（一個歷史很久的 Linux 發行版，可以想成「一整套已經配好的 Linux 系統」）為基礎改出來的。Debian 每一代都有一個玩具總動員角色的代號：

| 代號 | Debian 版本 | Raspberry Pi OS 發行日 | 出處 |
| --- | --- | --- | --- |
| Bookworm | Debian 12 | 2023-10-10 | [Raspberry Pi OS 發行說明](https://downloads.raspberrypi.com/raspios_arm64/release_notes.txt)：`2023-10-10: Based on Debian bookworm release` |
| Trixie | Debian 13 | 2025-10-01 | 同上：`2025-10-01: Based on Debian Trixie release` |

我們用來實測的這台 RP5（Raspberry Pi 5 Model B Rev 1.0、8 GB）目前是 `Debian GNU/Linux 13 (trixie)`，出處：[repo 第 02 課實測](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2002%20%E8%AA%B2%EF%BD%9C%E8%AA%8D%E8%AD%98%20Raspberry%20Pi%20%E8%88%87%20Raspberry%20Pi%20OS.md)。要注意，**它是「既有系統」，不是剛重灌的乾淨系統**；這點會影響我們能宣稱什麼，後面會再說。

## 一、你會遇到的差異

### 1. Python 版本：3.11 → 3.13

| 項目 | 舊課程機器（Bookworm） | 目前機器（Trixie） |
| --- | --- | --- |
| `python3 --version` | `Python 3.11.2` | `Python 3.13.5` |

- 實測出處：[repo 第 02 課](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2002%20%E8%AA%B2%EF%BD%9C%E8%AA%8D%E8%AD%98%20Raspberry%20Pi%20%E8%88%87%20Raspberry%20Pi%20OS.md)的版本對照表。
- 官方出處：[Debian 13 新功能說明](https://www.debian.org/releases/trixie/release-notes/whats-new.en.html)的套件版本表，Python 3 由 3.11 升到 3.13。

**為什麼重要**：很多 Python 套件要針對每個 Python 版本另外打包。套件沒有出 3.13 版時，`pip install` 就會失敗或裝到別的版本。下面 MediaPipe 的問題就是這樣來的。

### 2. 桌面與遠端桌面：不是 Trixie 才換的

很多網路文章會說「Trixie 改用 Wayland」。查官方資料後，事實是：

| 時間 | 官方說明 | 出處 |
| --- | --- | --- |
| 2023-10-10（Bookworm） | Raspberry Pi 4、5 的桌面改跑在 **Wayland** 上（Wayfire 視窗管理員）；在 Wayland 下用 **WayVNC** 取代 RealVNC 當 VNC 伺服器 | [Bookworm 發布文章](https://www.raspberrypi.com/news/bookworm-the-new-version-of-raspberry-pi-os/)、[發行說明](https://downloads.raspberrypi.com/raspios_arm64/release_notes.txt) 2023-10-10 |
| 2024-10-22（仍是 Bookworm） | 所有型號預設改用 **labwc** | [發行說明](https://downloads.raspberrypi.com/raspios_arm64/release_notes.txt) 2024-10-22、[2024-10-28 官方文章](https://www.raspberrypi.com/news/a-new-release-of-raspberry-pi-os/) |
| 2025-10-01（Trixie） | 新的 **Control Centre（控制中心）** 取代原本好幾個設定程式 | [Trixie 發布文章](https://www.raspberrypi.com/news/trixie-the-new-version-of-raspberry-pi-os/)、[發行說明](https://downloads.raspberrypi.com/raspios_arm64/release_notes.txt) 2025-10-01 |

名詞白話一下：

- **X11 與 Wayland**：都是「把視窗畫到螢幕上」的系統。X11 用了三十多年；Wayland 是新一代，比較快也比較安全。
- **labwc／Wayfire**：在 Wayland 上負責排列、移動視窗的程式，叫做合成器（compositor）。
- **VNC**：讓你在另一台電腦看見並操作 RP5 整個桌面的方法。RP5 上要有「VNC 伺服器」送出畫面。

**對這套教材的影響**：舊課程那台機器跑的是 X11，VNC 伺服器是 RealVNC 的 `vncserver-x11-serviced`；目前這台 Trixie 的 VNC 伺服器是 **wayvnc 0.10.2**，狀態 `active`／`enabled`，監聽 5900 埠。RealVNC Server 7.13.1 雖然裝著，但 `vncserver-x11-serviced` 是 `inactive`。出處：[repo 第 10 課](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2010%20%E8%AA%B2%EF%BD%9CRaspberry%20Pi%205%20%E5%AE%89%E8%A3%9D%E8%88%87%E8%A8%AD%E5%AE%9A%20VNC%20Viewer.md)、[2026-11-12 全面盤點紀錄](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/2026-11-12%E5%85%A8%E9%9D%A2%E7%9B%A4%E9%BB%9E%E7%B4%80%E9%8C%84.md)。所以你在網路上看到要你啟動 `vncserver-x11-serviced` 的舊教學，在現在的桌面不適用。

### 3. OpenCV 與 NumPy

| 項目 | 目前機器的實測 | 出處 |
| --- | --- | --- |
| 課程主環境 `opencv-course-env` | opencv-python 4.12.0.88、NumPy 2.2.6 | [repo 第 14 課](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2014%20%E8%AA%B2%EF%BD%9C%E5%9C%A8%20Raspberry%20Pi%205%20%E5%AE%89%E8%A3%9D%20OpenCV.md) |
| Thonny 的套件管理員 | 出現 `No module named 'pkg_resources'`，所以改用安裝腳本 | 同上 |
| YOLO 相機環境（2026-11-12 新建） | OpenCV 5.0.0、PyTorch 2.15.0+cpu、Ultralytics 8.4.208 | [全面盤點紀錄](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/2026-11-12%E5%85%A8%E9%9D%A2%E7%9B%A4%E9%BB%9E%E7%B4%80%E9%8C%84.md) |
| SIFT 特徵 | 用 `cv2.SIFT_create()`；SURF 在目前環境不能用 | [repo 第 31 課](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2031%20%E8%AA%B2%EF%BD%9C%E4%BD%BF%E7%94%A8%20OpenCV%20%E6%AF%94%E8%BC%83%20SIFT%E3%80%81SURF%20%E8%88%87%20ORB%20%E7%89%B9%E5%BE%B5%E6%AA%A2%E6%B8%AC.md) |

舊課程在 Bookworm 上記錄過 OpenCV 4.10.0（自行編譯）與系統套件 4.6.0；各篇保留的舊數字都會清楚寫明是 Bookworm。

### 4. MediaPipe：`mp.solutions` 不見了

- PyPI 上，MediaPipe 從 **1.0.0**（2026-07-27）起才提供 ARM64 Linux（`manylinux_2_28_aarch64`）的安裝檔；0.10.30～0.10.35 只有 x86_64。出處：[PyPI mediapipe](https://pypi.org/project/mediapipe/#files)（2026-11-12 查詢時最新為 1.2.3）。
- 我們在目前 Trixie 裝的 1.2.2 已經**沒有 `mp.solutions`**，舊程式會出現 `AttributeError: module 'mediapipe' has no attribute 'solutions'`。改用 CVZone 2.0.0（內部用新的 Tasks API）可以正常使用，臉部模型回傳 **478 點**（含虹膜 10 點），不是舊文章寫的 468 點；手部仍是 21 點。出處：[全面盤點紀錄](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/2026-11-12%E5%85%A8%E9%9D%A2%E7%9B%A4%E9%BB%9E%E7%B4%80%E9%8C%84.md)、[repo 補充 1](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E8%A3%9C%E5%85%85%201%EF%BD%9C%F0%9F%8E%AF%20MediaPipe%20%E4%BB%8B%E7%B4%B9%EF%BC%9AGoogle%20%E9%96%8B%E6%BA%90%E7%9A%84%E8%B7%A8%E5%B9%B3%E5%8F%B0%E8%A6%96%E8%A6%BA%20AI%20%E6%A1%86%E6%9E%B6.md)。

### 5. qiv 看圖程式

目前 Trixie **沒有預裝** qiv；用 `sudo apt install -y qiv` 裝到的是 `3.0.1-2+deb13u1`（約 102 kB）。舊教材裡的 qiv 2.3.3 紀錄來自另一台系統。出處：[repo 第 08 課](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2008%20%E8%AA%B2%EF%BD%9CRaspberry%20Pi%205%20%E5%AE%89%E8%A3%9D%E8%88%87%E4%BD%BF%E7%94%A8%20qiv%20%E5%9C%96%E7%89%87%E6%AA%A2%E8%A6%96%E5%99%A8.md)。

### 6. 虛擬環境路徑：舊的 `myenv` 不在了

**虛擬環境**是替某個專案準備的一個「獨立 Python 工具箱」，裝在裡面的套件不會影響系統或其他專案。

舊課程把大部分套件裝在 Bookworm 的 `/home/pi/myenv`（Python 3.11.2、MediaPipe 0.10.9、Ultralytics 8.3.50）。這個環境在目前 Trixie **已經不存在**；而且目前的 13 個環境裡，沒有任何一個同時有 `picamera2` 和 `ultralytics`，也沒有任何一個有 `mediapipe`，所以 2026-11-12 另外新建了兩個。出處：[全面盤點紀錄](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/2026-11-12%E5%85%A8%E9%9D%A2%E7%9B%A4%E9%BB%9E%E7%B4%80%E9%8C%84.md)。

下表依 repo 各篇紀錄整理，課號是**部落格版新課號**；實際路徑以各篇為準，你自己的路徑可以不同。

| 環境名稱（目前 Trixie） | 用在哪幾篇 |
| --- | --- |
| `opencv-course-env`（新 11 建立） | 新 11、12、19～21、34、35 |
| `ba5077-camera-contrib-trixie-20261110` | 新 17、23、27、30、31～33、38 |
| `ba5077-contrib-trixie-20261109` | 新 36 |
| `ba5077-picamera2-opencv-trixie-20261109` | 新 22 |
| `ba5077-yolov8-cpu-trixie-20261110` | 新 39～41 |
| `ba5077-yolo-camera-trixie-20261112` | 新 42、43 |
| `ba5077-mediapipe-trixie-20261112` | 新 49～53 |
| LiteRT 專用環境（2026-11-10） | 新 47、48 |

要同時用相機（Picamera2）和 OpenCV 擴充功能時，環境的建法寫在 [Thonny 環境與套件安裝](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/Thonny%E7%92%B0%E5%A2%83%E8%88%87%E5%A5%97%E4%BB%B6%E5%AE%89%E8%A3%9D.md)。

### 7. 相機

**相機堆疊**指的是「從相機感光元件到你的程式」中間那一串軟體。

- 目前 Trixie 的相機工具是 `rpicam-apps` v1.14.0。repo 第 07 課記載，官方相機程式在 Bookworm 時已改名為 `rpicam-*`，所以原文的 `libcamera-hello`、`libcamera-jpeg` 在新版教材改寫成 `rpicam-hello`、`rpicam-jpeg`。出處：[repo 第 07 課](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2007%20%E8%AA%B2%EF%BD%9C%E9%80%A3%E6%8E%A5%20Raspberry%20Pi%205%20%E7%9B%B8%E6%A9%9F%E6%A8%A1%E7%B5%84.md)。
- 終端機錄影 `rpicam-vid -n -t 5000 --width 1280 --height 720 --framerate 30 --codec libav` 錄到 142 影格，約 30 FPS。出處：[repo 第 13 課](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2013%20%E8%AA%B2%EF%BD%9CRaspberry%20Pi%20%E4%BD%BF%E7%94%A8%E6%94%9D%E5%BD%B1%E6%A9%9F%E5%AE%8C%E6%95%B4%E6%8C%87%E5%8D%97.md)。
- 許多網路範例會用 `cv2.VideoCapture(0)` 開相機。在這台 RP5 上，它對排線接的 CSI 相機會「開成功（True）但讀不到影格（False）」，所以本教材統一用 **Picamera2** 取像。出處同上。

> 尚未實測：舊的 `libcamera-*` 指令在目前 Trixie 上還能不能執行，repo 裡沒有紀錄，我也沒找到可以引用的官方說明，所以這裡不做判斷。

### 8. 其他：Tesseract 與 Ollama

- 文字辨識工具 **Tesseract** 在目前 Trixie **沒有安裝**（`command -v tesseract` 沒有輸出），所以 OCR 那幾篇在 Trixie 上屬於「尚未實測」。出處：[全面盤點紀錄](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/2026-11-12%E5%85%A8%E9%9D%A2%E7%9B%A4%E9%BB%9E%E7%B4%80%E9%8C%84.md)。
- **Ollama** 原本也沒裝，2026-11-11 由帳號持有人用官方安裝程式裝了 0.40.16（約 2.2 GB），再下載 SmolLM2 135M 模型。出處：[repo 補充 7](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E8%A3%9C%E5%85%85%207%EF%BD%9C%F0%9F%A7%A0%20Raspberry%20Pi%205%20%E4%B8%8A%E5%AE%89%E8%A3%9D%20Ollama%20%E5%AE%8C%E6%95%B4%E6%95%99%E5%AD%B8%EF%BC%88%E6%94%AF%E6%8F%B4%20ARM64%EF%BC%89.md)。

## 二、這次教材怎麼升級

1. **在實機上重新測試，並老實記錄**：2026-11-09～11-12 在目前 Trixie 上逐篇重做或補測。依 2026-11-12 的分類，56 篇中「主要成果已做」39 篇、「明確未完成」13 篇（新 04、06、07、13、31、32、36、39、44、50～53）、「待核」4 篇（新 01、03、08、09）；新舊課號請見[新舊課號對照表](./新舊課號對照表.md)。**目前沒有任何一篇能證明零基礎學生可以從頭到尾自己做完**——這是我們誠實的現況。出處：[56 篇完成度分類](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/56%E7%AF%87%E5%AE%8C%E6%88%90%E5%BA%A6%E5%88%86%E9%A1%9E%E8%88%87%E4%BA%BA%E5%B7%A5%E4%BD%9C%E6%A5%AD.md)。
2. **改用 Thonny 當主線**：Thonny 是給初學者用的 Python 編輯器，RP5 桌面內建。Python 課一律在 Thonny 裡選好虛擬環境再按執行，減少「同一段程式在終端機和編輯器結果不同」的困擾。出處：[Thonny 逐篇實測狀態](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/Thonny%E9%80%90%E7%AF%87%E5%AF%A6%E6%B8%AC%E7%8B%80%E6%85%8B.md)。
3. **補上排錯表**：常見錯誤訊息、可能原因與先試的做法，各篇都會整理成表。
4. **分清素材來源**：每張圖都會標明是「操作截圖」「相機實拍」「程式輸出」還是「生成素材」。例如有些相機課拍的是螢幕上播放的生成動畫，這和拍真實物體是兩回事。出處：[測試素材說明](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%B7%B4%E7%BF%92%E7%B4%A0%E6%9D%90/%E6%B8%AC%E8%A9%A6%E7%B4%A0%E6%9D%90%E8%AA%AA%E6%98%8E.md)。
5. **依難度重新排序**：原課號大致照寫作順序；部落格版改成「先備知識 → 系統與連線 → 終端機與編輯器 → Python／Thonny → 相機 → OpenCV 基礎 → 影像處理 → 特徵與追蹤 → 深度學習／YOLO → 補充應用」，而且「要先安裝的課一定排在使用它的課前面」。

## 三、怎麼讀這套部落格版

- 每篇標題下第一行是「原課號」，連到 GitHub 上的 repo 教材；旁邊另附 digithouse.net 的原文。想看完整紀錄、教師備註或歷史版本，請點 repo 連結。
- 看到 **「尚未實測」**，表示那一步是依官方文件或原文整理，我們還沒在目前這台 Trixie 上做過，請把它當作參考步驟，不要當成保證。
- 看到 **「舊環境（Bookworm）」**，表示那個輸出來自舊機器，留下來讓你比較，不代表在 Trixie 上會一樣。
- 你自己的輸出數字（記憶體用量、環境路徑、IP 位址）和文章不同是正常的，不需要改成一樣。
- 練習圖片和程式的下載方式見[素材下載與使用](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%B7%B4%E7%BF%92%E7%B4%A0%E6%9D%90/%E7%B4%A0%E6%9D%90%E4%B8%8B%E8%BC%89%E8%88%87%E4%BD%BF%E7%94%A8.md)。

## 小結

這一代 Raspberry Pi OS 的大改變（Wayland、wayvnc、labwc）其實在 Bookworm 就開始了；Trixie 帶來的是 Python 3.13、新的控制中心，以及跟著 Python 版本而來的套件變化，例如 MediaPipe。這套教材的做法是：能在目前機器測的就實測並保留數字，不能測的就清楚標示，不把舊結果當新結果。

## 下一篇預告

下一篇[01｜這門課要帶你做出什麼？](./01-%E9%80%99%E9%96%80%E8%AA%B2%E8%A6%81%E5%B8%B6%E4%BD%A0%E5%81%9A%E5%87%BA%E4%BB%80%E9%BA%BC%EF%BC%9FBA5077%20AIoT%20%E8%AA%B2%E7%A8%8B%E5%9C%B0%E5%9C%96.md)，我們先不碰任何安裝，從「誰需要幫忙」開始，畫出你這學期想做的 AIoT 產品。
