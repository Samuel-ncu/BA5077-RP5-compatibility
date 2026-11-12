# 03｜網路與作業系統入門：介面狀態、名稱解析與 Linux 目錄

## [原課號：第 03 課｜網路基礎與作業系統：應用於 Raspberry Pi（上）](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/%E7%AC%AC%2003%20%E8%AA%B2%EF%BD%9C%E7%B6%B2%E8%B7%AF%E5%9F%BA%E7%A4%8E%E8%88%87%E4%BD%9C%E6%A5%AD%E7%B3%BB%E7%B5%B1%EF%BC%9A%E6%87%89%E7%94%A8%E6%96%BC%20Raspberry%20Pi%EF%BC%88%E4%B8%8A%EF%BC%89.md)

digithouse.net 原文：[第 3 課｜網路基礎與作業系統：應用於 Raspberry Pi（上）](https://digithouse.net/blog/ba5077-lesson-02-network-os?locale=zh-TW)

> **本篇狀態**：文中可以照做的查詢指令，都已在目前 Trixie 實測（2026-11-09）。依 [56 篇完成度分類](https://github.com/Samuel-ncu/BA5077-RP5-compatibility/blob/main/%E6%95%99%E6%9D%90/56%E7%AF%87%E5%AE%8C%E6%88%90%E5%BA%A6%E5%88%86%E9%A1%9E%E8%88%87%E4%BA%BA%E5%B7%A5%E4%BD%9C%E6%A5%AD.md)屬於「待核」：電腦與 RP5 直連的網段設定、外網排錯，目前只有觀念說明，**尚未實測**。

有一次上課，一位同學舉手說：「老師，我網路線明明插好了，燈也有亮，為什麼還是連不上？」這其實是一個很好的問題。「插好線」「拿到地址」「找得到對方」「對方有在服務」是四件不同的事，任何一件沒成功都會連不上。今天我們就把連線拆開來看，順便認識 RP5 上的作業系統。

## 這篇會學到什麼

- 作業系統和網路各負責什麼。
- 實體連線、IP 位址、名稱解析、服務埠是四個不同的檢查項目。
- 用指令查看網路介面狀態和名稱解析。
- 認識 Linux 的核心、發行版，以及樹狀的資料夾結構。

## 需要的東西

- 已開機的 RP5 和終端機（做法見[上一篇](./02-%E8%AA%8D%E8%AD%98%E4%BD%A0%E7%9A%84%E5%B0%8F%E9%9B%BB%E8%85%A6%EF%BC%9ARaspberry%20Pi%205%20%E8%88%87%20Raspberry%20Pi%20OS.md)）。
- 不需要改任何網路設定。

## 先懂幾個名詞

- **作業系統**：管理硬體、程式、檔案和使用者的基礎軟體。RP5 上的 Linux 讓 Python 能讀相機、存檔案，也能透過網路收送資料。
- **IP 位址**：網路裡的「收件地址」，資料靠它找到你的裝置。
- **名稱解析**：像查通訊錄，把名字（例如 `localhost`）查成 IP 位址。
- **服務埠（port）**：同一個地址下的不同「服務窗口」。對方電腦開著，不代表它的 SSH 或網頁窗口有人在。
- **網路介面**：裝置上負責連網的那個硬體。RP5 上 `eth0` 通常是有線網路，`wlan0` 通常是 Wi-Fi。

這些比喻是幫助入門，真實網路的路由與傳輸細節更多。

## RP5 有哪些連網方式

1. **透過路由器**：電腦和 RP5 接到同一個網路，由路由器發地址給它們（這個自動發地址的機制叫 DHCP）。
2. **電腦直接接 RP5**：兩端用網路線直連。沒有路由器時，**不能假設會自動拿到地址**，兩端要設定相容的位址。（本篇只說明觀念，直連設定**尚未實測**。）
3. **Wi-Fi 和網路線一起用**：例如 RP5 用 Wi-Fi 上網，同時用網路線連到電腦。這時要確認兩條路的地址和路由都正確。

## 一步一步操作

### 步驟 1：查名稱解析和網路介面

**為什麼**：先確認 RP5 自己這一端的狀態，再去懷疑網路或對方。

在 RP5 終端機一行一行輸入：

```bash
getent hosts localhost
cat /sys/class/net/eth0/operstate
cat /sys/class/net/wlan0/operstate
```

2026-11-09 在目前 Trixie 的實際輸出：

```text
::1             localhost ip6-localhost ip6-loopback
down
up
```

怎麼讀：

- 第一行：`localhost` 查到 `::1`，這是 IPv6 的「本機自己」地址。它只證明本機名稱解析正常，**不能**證明外面的網站查得到。
- `down`：測試當時有線網路 `eth0` 沒有啟用。
- `up`：Wi-Fi `wlan0` 是啟用狀態。這次我們就是透過 Wi-Fi 遠端操作的。

這只是**當時這一台**的狀態，你的 RP5 得到不同答案很正常。而且 `up` 只代表介面啟用，不代表能上網、也不代表每個服務都能用。

舊課程機器（Bookworm）當時用網路線，`eth0` 的輸出是 `up`，`localhost` 的查詢結果與上面相同。

### 步驟 2：介面名稱不一樣怎麼辦

**為什麼**：有些系統的介面不叫 `eth0` 或 `wlan0`，硬查會出現「找不到檔案」。

先列出實際的介面名稱：

```bash
ip -br link
```

再把步驟 1 裡的 `eth0`、`wlan0` 換成你看到的名稱。想看目前的 IP 位址，可以用 `ip -br addr`。

> **隱私提醒**：IP 位址是你所在網路的資訊。截圖或交作業前，先檢查是否需要遮蔽。

### 步驟 3：認識 Linux 的資料夾

**為什麼**：之後要存程式、找圖片、建虛擬環境，都要知道東西放在哪。

幾個名詞：

- **Linux 核心**：負責協調處理器、記憶體和各種裝置的那一層。
- **發行版**：核心加上工具和套件組成的一整套系統。Debian、Raspberry Pi OS 都是。
- **圖形桌面（GUI）與終端機**：一個用滑鼠點，一個用文字打指令（打指令的那層程式叫 shell）。兩者操作的是同一台電腦。

Linux 的資料夾是一棵樹，最上面是 `/`（根目錄）：

| 路徑 | 通常放什麼 |
| --- | --- |
| `/` | 根目錄，所有東西都從這裡開始 |
| `/home` | 使用者自己的資料 |
| `/tmp` | 暫存檔，重開機可能被清掉 |
| `/boot/firmware` | 這台 RP5 的開機檔所在位置 |

輸入下面的指令確認：

```bash
uname -s
uname -m
python3 -c 'import os; print(os.path.isdir("/home")); print(os.path.isdir("/tmp"))'
test -d /boot/firmware && echo boot-firmware-present
```

RP5 的實際輸出：

```text
Linux
aarch64
True
True
boot-firmware-present
```

前兩行是核心名稱和架構；兩個 `True` 表示 `/home` 和 `/tmp` 在測試當下存在；最後一行表示 `/boot/firmware` 是一個資料夾。它不代表裡面每個開機檔都正確。

## 成果圖

![目前 Trixie 終端機的名稱解析、有線與無線介面狀態實際截圖](https://raw.githubusercontent.com/Samuel-ncu/BA5077-RP5-compatibility/main/%E6%95%99%E6%9D%90/%E5%9C%96%E6%AA%94/lesson03-trixie-network.png)

*操作截圖：透過 Pi Connect 操作 RP5 時的終端機畫面，已裁切，只保留這次的指令與輸出（2026-11-09，目前 Trixie）。*

## 常見問題

| 你看到的情況 | 可能原因 | 怎麼做 |
| --- | --- | --- |
| `cat: /sys/class/net/eth0/operstate: No such file or directory` | 你的介面不叫 `eth0` | 用 `ip -br link` 查實際名稱 |
| 介面是 `up`，但還是連不上 | `up` 只代表介面啟用 | 再查 IP 位址、對方服務是否開著 |
| `localhost` 查得到，但上不了網站 | 本機解析不等於外網 DNS | 這是兩件事，要分開檢查 |
| 網路線插好但 `eth0` 是 `down` | 線材、對端設備或設定問題 | 換線或換孔試試；也可能你本來就只用 Wi-Fi |

## 小結

連不上網時，拆成四個問題一個一個查：線（或 Wi-Fi）有沒有連上？有沒有拿到 IP？名字查不查得到？對方服務有沒有在跑？今天我們查了前面兩三項，也認識了 Linux 從 `/` 開始的資料夾樹。

**練習**：

1. 用自己的話說明：「網路線接好」「拿到 IP」「SSH 可以登入」為什麼是三個不同的問題？
2. 如果 `localhost` 查得到，能證明外網可以用嗎？為什麼？
3. 畫出你的電腦、RP5、路由器之間的連線，標出資料走哪條線或哪個 Wi-Fi。

參考：[Raspberry Pi 遠端存取文件](https://www.raspberrypi.com/documentation/computers/remote-access.html)。

## 下一篇預告

下一篇[04｜動手安裝 Raspberry Pi OS](./04-%E5%8B%95%E6%89%8B%E5%AE%89%E8%A3%9D%20Raspberry%20Pi%20OS%EF%BC%9A%E7%94%A8%20Imager%20%E7%87%92%E9%8C%84%E8%88%87%E7%AC%AC%E4%B8%80%E6%AC%A1%E9%96%8B%E6%A9%9F.md)，我們會看一張全新的記憶卡，怎麼變成一台可以開機的電腦——以及為什麼按下「寫入」之前一定要再三確認。
