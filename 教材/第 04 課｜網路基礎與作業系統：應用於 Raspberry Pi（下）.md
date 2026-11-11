# 第 04 課｜網路基礎與作業系統：應用於 Raspberry Pi（下）

[原始文章](https://liusming.pixnet.net/blog/posts/14222880483) · 更新日期：2026-10-29

想像你坐在另一台電腦前，請 RP5 回答一個問題。我們先認識遠端登入，再用一個小網頁理解請求和回應。

如果你使用 Trixie，可以先做[一次性 Python 跨裝置 HTTP](#現有-trixie-實測windows-跨裝置-http2026-11-10)理解請求與回應，再做本課主線[安裝 Apache 網頁伺服器](#主線實作安裝-apache讓別台電腦打開-rp5-的網頁2026-11-11-實測)；前後的舊版例子可留到比較時閱讀。

## 學習目標

認識 Linux、套件管理器與 SSH，並能確認系統是否具備相關工具。套件管理器安裝系統程式；Python 專案則可用獨立虛擬環境管理額外套件。

## 背景：遠端操作與軟體從哪裡來？

當 RP5 沒有接螢幕時，另一台電腦仍可經網路使用 SSH 遠端登入。SSH 提供加密的連線，讓你在 RP5 的終端機執行命令；輸入命令的位置仍是 RP5，不是本機的 Windows。登入前需確認設備、帳號與網路連線正確。

作業系統中的套件管理器協助下載與管理軟體。APT 管理 Debian 系列的系統套件；Python 專案也可能使用虛擬環境管理程式庫。這是兩個不同層次：系統有 `apt`，不代表某個 Python 套件一定已安裝。

```mermaid
flowchart LR
    A[電腦的 SSH 用戶端] --> B[RP5 SSH 服務]
    B --> C[RP5 的 Linux 終端機]
    C --> D[APT 或 Python 程式]
```

上圖是教學流程圖；它不顯示或證明真實的網路連線狀態。

## 實作：確認作業系統與架構

```bash
python3 -c "import platform; print(platform.system()); print(platform.machine())"
command -v apt
```

本機實際輸出：

```text
Linux
aarch64
/usr/bin/apt
```

第一行是核心所屬系統，第二行是處理器架構；`/usr/bin/apt` 表示目前系統找得到 APT。這不代表每個需要的套件均已安裝。

## 實作：確認 SSH

```bash
systemctl is-active ssh
```

本機實際輸出：

```text
active
```

`active` 表示此時 SSH 服務正在執行；遠端登入仍需網路可達、帳號以及適當的認證方式。完成操作後應妥善保護密碼與私鑰。

## 套件與系統更新

APT 的套件來源、版本和網路狀況都會影響安裝結果。先確認要安裝的套件及儲存空間，再依該篇教材操作；不需要為了每一篇文章都全面升級系統。開放 Apache 等服務之前，應確認是否真的需要提供網路存取。

## 練習與後續應用

1. 解釋 `systemctl is-active ssh` 回傳 `active` 所表示的事，以及它不能保證什麼。
2. 說明 `command -v apt` 找得到程式，和某個套件已安裝，為什麼不是同一件事。
3. 設計一個本地網頁顯示感測資料的情境，寫出可能需要的輸入、處理方式與使用者；本次已測本機 Python HTTP 範例，Apache 安裝與跨裝置瀏覽見下方主線。

遠端操作適用於沒有螢幕的感測節點，也讓維護人員能檢查狀態。正式部署還要考量帳號認證、連線範圍、軟體更新與裝置失聯時的處置。[Raspberry Pi 遠端存取文件](https://www.raspberrypi.com/documentation/computers/remote-access.html)可供後續學習。

## 綜合實作：讓 RP5 回應一次本機網頁請求

原文包含架設網頁伺服器的情境。這裡先用 Python 內建工具理解「請求與回應」，不需要另安裝 Apache，也不對區域網路開放服務。這個練習會啟動一個暫時的本機服務、送出一次請求，再自行關閉。

### 事前準備

需要能在 RP5 執行 Python 3。下方程式沒有額外第三方套件；把它存為 `第04課-本機網頁.py`，也可使用[範例程式](./範例程式/第04課-本機網頁.py)。

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.request import urlopen


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'Hello, AIoT!'
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


# 只監聽 RP5 本機，並讓系統選擇一個可用的連接埠。
server = HTTPServer(('127.0.0.1', 0), DemoHandler)
thread = Thread(target=server.serve_forever)
thread.start()
try:
    url = f'http://127.0.0.1:{server.server_port}/'
    with urlopen(url, timeout=5) as response:
        print('HTTP status:', response.status)
        print('response:', response.read().decode('utf-8'))
finally:
    server.shutdown()
    thread.join()
    server.server_close()
```

在 RP5 的 Thonny 選「檔案 → 開啟」開啟上方範例，按綠色執行按鈕。2026-10-29 在先前 Bookworm 環境的 Thonny 實際輸出：

```text
HTTP status: 200
response: Hello, AIoT!
```

![Thonny 實際執行本機 HTTP 範例](./圖檔/lesson04-http-thonny.png)

### 在現有 Trixie 系統操作（2026-11-09）

這次使用 Raspberry Pi 5 現有的 Debian 13 Trixie 環境、Thonny 與系統 Python 3.13.5；並非全新安裝的系統。這個範例使用 Python 標準函式庫，不需要另外安裝套件。

1. 在 RP5 取得[本課 Python 範例](./範例程式/第04課-本機網頁.py)，下載與放置方式請見[素材下載與使用](./練習素材/素材下載與使用.md)。
2. 開啟 Thonny，選「File → Open」找到並開啟此範例。確認右下角選用 RP5 的系統 Python 3。
3. 點選綠色執行鈕，觀察下方 Shell。執行完成後會回到 `>>>` 提示符號。

本次在 Thonny 實際得到：

```text
HTTP status: 200
response: Hello, AIoT!
```

![現有 Trixie 系統中，Thonny 的程式與實際輸出](./圖檔/lesson04-http-trixie-thonny.png)

*圖：RP5 上 Thonny 實際執行畫面，為方便閱讀而裁切。路徑與檔名可依個人存放位置不同；輸出結果的兩行文字應相同。*

### 讀懂結果

`127.0.0.1` 指向執行程式的 RP5 本身；連接埠設為 `0` 時，由系統選一個目前可用的連接埠。程式以 `urlopen` 對自己的服務提出請求，`200` 表示這次請求收到成功回應，後面一行是回應內容。最後的 `shutdown` 與 `server_close` 負責關閉服務。

這個測試證明 RP5 本機內的 HTTP 請求和回應可運作，**不證明其他電腦能連到 RP5，也不代表 Apache 已安裝或對外提供服務**。

### 練習與問題排除

1. 修改 `body` 裡的英文訊息，再執行一次；記下輸出如何改變。若要使用中文字，需先用 UTF-8 編碼成 bytes，並注意 `Content-Length` 使用的是位元組數。
2. 試著解釋服務、連接埠、請求與回應各自扮演什麼角色。
3. 若看到 `ModuleNotFoundError`，確認是在 RP5 的 Python 3 執行；若埠綁定失敗，檢查環境是否限制本機網路。

延伸到感測器時，回應內容可以由固定文字改為溫度或其他數值。但在讓其他裝置連入之前，還需考慮誰能存取、資料是否敏感以及服務失敗時的處理方式。
## 現有 Trixie 實測：Windows 跨裝置 HTTP（2026-11-10）

這次在既有 Trixie、Thonny 的 `/home/pi/opencv-course-env/bin/python3` 執行下列不需額外套件的範例，再從同一網路的 Windows 電腦提出一次請求。這不是 Apache，也不是全新系統測試。只在可信任的練習網路使用；服務沒有驗證，只傳固定字串，處理一次請求，或在沒有連線時等候 120 秒後關閉。

1. 在 RP5 確認自己的 IPv4 位址；不要把實際私人位址貼到公開教材。
2. 在 Thonny 建立新檔，貼入下列程式，或下載[完整範例](./範例程式/第04課-跨裝置HTTP.py)後開啟。執行後記下 Shell 顯示的連接埠。

```python
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'Hello, AIoT!'
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print('Request handled: 200')
    def log_message(self, format, *args):
        pass

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
    probe.connect(('1.1.1.1', 53))
    address = probe.getsockname()[0]
with HTTPServer((address, 0), Handler) as server:
    server.timeout = 120
    print('Ready port:', server.server_port, flush=True)
    server.handle_request()
print('Server closed')
```

程式透過 UDP socket 選出系統到 `1.1.1.1` 的 IPv4 路由介面，僅查詢本機路由而未送出應用資料；若沒有可用路由，會在啟動服務前失敗。它只綁定所選介面，連接埠 `0` 由系統分配；若有多張網卡，所選介面可能不是電腦所連的網路，應先核對。連接埠每次可能不同。

3. 在本次使用的 Windows PowerShell 7 將 `<RP5位址>` 與 `<連接埠>` 換成當次值，執行以下兩行：

```powershell
$response = Invoke-WebRequest -Uri 'http://<RP5位址>:<連接埠>/' -TimeoutSec 8 -UseBasicParsing
$response.StatusCode
[System.Text.Encoding]::UTF8.GetString($response.Content)
```

本次 Windows 實際收到狀態 `200`；回應內容以位元組顯示為 `72 101 108 108 111 44 32 65 73 111 84 33`，將這些位元組以 UTF-8 解碼得到 `Hello, AIoT!`。RP5 的 Thonny Shell 當次輸出：

```text
Ready port: 34055
Request handled: 200
Server closed
```

![RP5 Thonny 跨裝置請求與服務關閉](./圖檔/lesson04-trixie-cross-http-20261110.jpg)

*圖：RP5 桌面分享中 Thonny 的實際程式與輸出；埠號為當次動態值。* `Server closed` 也可能在等候逾時後出現；必須同時看到 `Request handled: 200`，並在另一台電腦確認回應，才能證明本次跨裝置請求成功。第一次因誤讀埠號連線遭拒，核對 Thonny 顯示及監聽狀態後，使用正確埠成功。

若連線遭拒或逾時，先確認程式仍在等候、位址及埠號正確、兩台裝置可互通；網路隔離或防火牆可能限制連線。不要為了練習停用安全防護。此範例只提供暫時且未驗證的 HTTP，不能作為對外正式服務。

## 主線實作：安裝 Apache，讓別台電腦打開 RP5 的網頁（2026-11-11 實測）

前面的 Python 小服務只回應一次就關掉。真正的網站需要一個**一直在背景等候**的程式，這種程式叫做**網頁伺服器**。原文章用的是 Apache，它是世界上最常用的網頁伺服器之一。這一節我們用套件管理器 APT 把它裝起來，再從 Windows 的瀏覽器打開 RP5 的網頁。

```mermaid
flowchart LR
    A["Windows 瀏覽器<br/>輸入 http://RP5的IP/"] -->|"HTTP 請求（埠 80）"| B["RP5 上的 Apache<br/>systemd 服務，一直在背景"]
    B -->|"讀取"| C["/var/www/html/index.html"]
    B -->|"HTTP 回應 200 與網頁"| A
```

這張流程圖是教學示意，不是操作截圖。

### 事前準備

- RP5 已連上網路；你知道 RP5 的 IP（本次是 `192.168.1.78`，你的會不同，可用 `hostname -I` 查）。
- 另一台電腦（本次是 Windows）和 RP5 在**同一個區域網路**。
- 你知道 RP5 帳號的密碼：安裝系統軟體要用 `sudo`，它會問密碼。**密碼只輸入在自己的終端機，不要貼到聊天、作業或截圖裡。**

### 第一步：用 APT 安裝 Apache（在 RP5 的終端機）

**為什麼：**Apache 是系統程式，不是 Python 套件，所以用 APT 安裝，不用 Thonny 的 pip。先 `update` 讓 APT 拿到最新的套件清單，再 `install`。

```bash
sudo apt update
sudo apt install -y apache2
```

輸入第一行後會出現 `[sudo] password for pi:`，輸入密碼（畫面不會顯示字元）再按 Enter。`-y` 表示「安裝時的確認問題都回答是」。本次實際輸出的重點如下（中間的下載與解壓縮行省略）：

```text
Installing:
  apache2

Installing dependencies:
  apache2-bin   apache2-utils  libaprutil1-dbd-sqlite3  libaprutil1t64
  apache2-data  libapr1t64     libaprutil1-ldap

Summary:
  Upgrading: 0, Installing: 8, Removing: 0, Not Upgrading: 55
  Download size: 2,126 kB
  Space needed: 13.7 MB / 108 GB available
...
Setting up apache2 (2.4.69-1~deb13u1) ...
Enabling module mpm_event.
...
Enabling site 000-default.
Created symlink '/etc/systemd/system/multi-user.target.wants/apache2.service' → '/usr/lib/systemd/system/apache2.service'.
```

**這代表什麼：**APT 自動帶進 Apache 需要的 7 個相依套件；`Enabling site 000-default` 是預設網站；最後那行 `Created symlink ... multi-user.target.wants` 表示系統已把 Apache 設成**開機自動啟動**。`Not Upgrading: 55` 只是告訴你還有別的套件可以更新，這一課不需要全部升級。

### 第二步：確認服務真的在跑（仍在 RP5）

```bash
systemctl is-active apache2
systemctl is-enabled apache2
/usr/sbin/apache2 -v
curl -s -o /dev/null -w "localhost HTTP %{http_code}\n" http://localhost/
hostname -I
```

本次輸出：

```text
active
enabled
Server version: Apache/2.4.69 (Debian)
Server built:   2026-10-01T16:54:08
localhost HTTP 200
192.168.1.78
```

`active` 是「現在正在執行」，`enabled` 是「開機會自動啟動」，兩者不同。`curl` 在 RP5 自己身上要了一次首頁，得到 HTTP 狀態碼 `200`（成功）。`apache2` 這個指令放在 `/usr/sbin`，一般帳號直接打 `apache2 -v` 可能出現 `command not found`，寫完整路徑即可；這不代表安裝失敗。

### 第三步：從另一台電腦打開網頁（在 Windows）

在 Windows 的瀏覽器網址列輸入 `http://192.168.1.78/`（換成你的 RP5 IP），按 Enter。

![Windows 的 Chrome 開啟 http://192.168.1.78/，顯示 Apache2 Debian Default Page 與紅色 It works! 橫幅](./圖檔/lesson04-apache-windows-browser-20261111.jpg)

*圖：Windows 瀏覽器的操作截圖（2026-11-11）。網址列的「不安全」是因為用的是 HTTP 而不是 HTTPS，練習網路中可以接受，但不要在這種頁面輸入密碼。*

看到 **Apache2 Debian Default Page** 和紅色的 **It works!**，就代表請求從 Windows 經過網路到達 RP5 的 Apache，Apache 把 `/var/www/html/index.html` 回傳給瀏覽器。也可以在 Windows 的 PowerShell 用 `curl.exe -I http://192.168.1.78/` 檢查，本次回應標頭中有 `Server: Apache/2.4.69 (Debian)`，狀態碼 200。

### 讀懂結果與排錯

| 你看到的情況 | 可能原因 | 先試試看 |
| --- | --- | --- |
| `E: Unable to locate package apache2` | 套件清單太舊或沒有網路 | 先執行 `sudo apt update`，確認 RP5 能上網。 |
| `Could not get lock /var/lib/dpkg/lock-frontend` | 另一個 APT 或系統更新正在執行 | 等它結束再試；不要刪除鎖定檔。 |
| `systemctl is-active apache2` 不是 `active` | 服務沒起來或設定有誤 | `sudo systemctl status apache2` 看紅字；`sudo systemctl restart apache2`。 |
| RP5 上 `localhost HTTP 200`，Windows 卻連不上 | IP 打錯、兩台不在同一網路、網路有隔離 | 用 `hostname -I` 重新確認 IP；確認 Windows 和 RP5 連的是同一個網路。 |
| 瀏覽器自動改成 `https://` 而打不開 | 瀏覽器預設升級到 HTTPS | 網址前面明確打 `http://`。 |

### 練習與安全提醒

1. 說明 `active` 和 `enabled` 的差別：如果只做 `sudo systemctl stop apache2`，重開機後 Apache 會不會又啟動？
2. 預測：把 RP5 的網路線拔掉（或關 Wi-Fi）後，Windows 重新整理頁面會看到什麼？
3. 進階（本次未實測）：用 `sudo nano /var/www/html/index.html` 把首頁改成自己的一行文字，存檔後在 Windows 重新整理。修改系統檔案前先備份：`sudo cp /var/www/html/index.html /var/www/html/index.html.bak`。

裝好 Apache 等於讓同一個網路裡的**任何人**都能連到 RP5 的 80 埠。練習結束、不需要時，可以用 `sudo systemctl disable --now apache2` 停止並取消開機啟動；要移除則用 `sudo apt remove apache2`。在學校或公共網路開服務前，先確認是否被允許。

## 與原文章的差異

- 2026-11-11 新增 Apache 主線：在既有 Trixie 以 `sudo apt install -y apache2` 安裝 Apache 2.4.69（8 個套件、13.7 MB），確認 `active`、`enabled`、本機 HTTP 200，並從 Windows 瀏覽器開啟 `http://192.168.1.78/` 看到預設頁，附 Windows 瀏覽器截圖。修改首頁的練習未實測。
- 新增本機實測的 Linux、ARM64、APT 與 SSH 服務檢查。
- 不將全面升級或啟動網頁伺服器視為閱讀文章的必要步驟。
- 新增既有 Trixie 系統的 Thonny 本機 HTTP 實測及操作截圖；SSH 與 Apache 設定步驟未補拍，乾淨系統尚未驗證。
- 補充 SSH、套件管理、連線流程圖及學生練習；原文網頁伺服器情境仍未在本篇完整實測。
- 新增本機回送 HTTP 的實作及真實輸出；原文的 Apache 仍未完成實測；另已用一次性 Python 服務實測區域網路跨裝置請求。

<details>
<summary>給教師：原有實測範圍與版本備註</summary>

> 2026-11-11 Apache 實測：RP5 主機 PR5、IP `192.168.1.78`、既有 Trixie。帳號持有人在 Windows 端終端機經 SSH 執行預先寫好的腳本 `~/ba5077-validation-20261111/sudo-tasks.sh` 並自行輸入 sudo 密碼，完整輸出存於 RP5 `~/ba5077-validation-20261111/sudo-installs/install-20261111-193047.log`。腳本中 `apache2 -v` 因不在一般使用者 PATH 而顯示 `command not found`，另以 `/usr/sbin/apache2 -v` 補查。Windows 截圖為 Chrome（獨立暫時設定檔）視窗裁切。Apache 目前保持 `active`／`enabled`，不需要時由教師決定停用。
>
> 本篇為基礎系統或獨立工具教學；Python 課程改用 Thonny 的整體進度請見[逐篇狀態](./Thonny逐篇實測狀態.md) · [圖片與程式下載方式](./練習素材/素材下載與使用.md)。

</details>
