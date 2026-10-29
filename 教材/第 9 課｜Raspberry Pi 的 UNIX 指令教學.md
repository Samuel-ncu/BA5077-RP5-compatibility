# 第 9 課｜Raspberry Pi 的 UNIX 指令教學

[原始文章](https://liusming.pixnet.net/blog/posts/14222855934) · 更新日期：2026-10-29

> 本篇為基礎系統或獨立工具教學；Python 課程改用 Thonny 的整體進度請見[逐篇狀態](./Thonny逐篇實測狀態.md)。

## 學習目標

了解如何在 RP5 終端機查詢系統、工具與網路狀態。讀取資訊的命令通常可以先練習；涉及寫入、覆蓋、移動或刪除檔案的命令，應先確認目標。

## 本次實測的查詢

```bash
uname -m
python3 --version
command -v apt
```

本機實際輸出：

```text
aarch64
Python 3.11.2
/usr/bin/apt
```

`uname -m` 查詢架構；`python3 --version` 顯示 Python 版本；`command -v apt` 查找程式位置。若 `command -v` 沒有輸出，代表目前搜尋路徑沒有找到該名稱。

## 建議練習

依序觀察目前目錄、列出檔案、切換目錄與閱讀文字檔，再學習建立自己的練習目錄。不要把尚未確認的刪除指令套用到正式資料。

## 背景與核心概念

### 終端機為什麼有用？

終端機提供文字介面，shell 接收命令並啟動程式。提示符號不是命令的一部分；檔案路徑有絕對路徑與相對於目前目錄的路徑。命令的執行位置與目前目錄會影響結果。

### 思考、練習與後續應用

解釋 `uname -m`、`python3 --version` 與 `command -v apt` 各回答什麼問題；比較在電腦與 RP5 執行查詢的差異。

文字操作適合遠端維護和重現實驗；涉及寫入、覆寫、移動或刪除時需先辨識路徑。

進一步閱讀：[相關官方文件](https://www.raspberrypi.com/documentation/computers/configuration.html)。下方的程式與輸出以標明的本機實測範圍為準；沒有測過的部分不代表已完成。

## 概念流程圖

```mermaid
flowchart LR
    A["使用者輸入命令"]
    B["Shell 解析"]
    C["啟動程式"]
    D["終端機顯示結果"]
    A --> B --> C --> D
```

此圖用於說明文章的概念或完整目標流程，**不是操作截圖，也不代表每個步驟都已實測**；本機實測範圍請看文章中的標示。

## 實作：建立、閱讀並複製自己的練習檔

本例使用獨立的暫存目錄，讓你練習建立檔案、讀取內容和核對複製結果。程式不會自動刪除目錄；系統日後可能清理暫存空間，重要作業請保存在自己的家目錄。

把下列程式存為 `第09課-檔案練習.sh`，或下載[範例程式](./範例程式/第09課-檔案練習.sh)；在 RP5 的終端機執行。

```bash
#!/bin/sh
set -eu

# 在系統暫存目錄建立獨立資料夾，不使用既有的練習資料。
practice_dir=$(mktemp -d "${TMPDIR:-/tmp}/ba5077-lesson09.XXXXXX")
cd "$practice_dir"
printf 'Hello, AIoT!\n' > welcome.txt
mkdir samples
cp welcome.txt samples/copy.txt

printf '原始內容: '
cat welcome.txt
printf '檔案大小（bytes）: '
wc -c < welcome.txt
if cmp -s welcome.txt samples/copy.txt; then
    printf '複製結果: 內容一致\n'
else
    printf '複製結果: 內容不同\n'
    exit 1
fi
printf '練習檔案:\n'
find . -type f -print | LC_ALL=C sort
printf '練習目錄: %s\n' "$practice_dir"
```

```bash
sh 第09課-檔案練習.sh
```

本次 RP5 的實際輸出：

```text
原始內容: Hello, AIoT!
檔案大小（bytes）: 13
複製結果: 內容一致
練習檔案:
./samples/copy.txt
./welcome.txt
練習目錄: /tmp/ba5077-lesson09.bNRFTx
```

最後一行的隨機目錄名稱每次不同。這次是用 `sh` 執行相同內容的腳本；所列目錄與文字均來自 RP5 實際輸出。

### 逐行理解

1. `mktemp -d` 建立一個名稱唯一的練習資料夾，`cd` 切換進去；變數 `practice_dir` 保存路徑。
2. `printf ... > welcome.txt` 將文字寫入檔案。`>` 會覆寫同名檔案，因此要先確認位置；此例在新建資料夾內執行。
3. `mkdir` 建立子資料夾，`cp` 複製檔案；`cat` 讀取內容，`wc -c` 計算位元組數。13 包含行尾的換行字元。
4. `cmp -s` 比較兩份檔案的內容；`find` 和 `sort` 顯示練習檔案。路徑開頭的 `./` 代表目前目錄。

### 學生練習

1. 找出輸出中哪兩個檔案的內容相同。若修改其中一份後再比較，預期會如何？請在自己的練習目錄實際試驗。
2. 說明相對路徑 `./welcome.txt` 和完整路徑的差別。
3. 若要保留檔案過夜或繳交作業，為何不應只依賴暫存目錄？

原文還涵蓋系統管理與其他指令，本次未逐條重測。請勿把不理解的刪除或系統設定命令直接用在正式資料上。
## 與原文章的差異

- 優先列出已在本機執行且不會修改檔案的基本指令。
- 不把需要額外安裝的工具視為所有 RP5 均已具備。
- 原文其他指令與圖形截圖尚未逐條重新測試。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
- 加入教學流程示意；圖中的完整目標流程不代表已逐步實測。
- 新增獨立暫存目錄的檔案建立、複製、比較與 RP5 實際輸出；原文其他管理命令尚未逐條測試。
