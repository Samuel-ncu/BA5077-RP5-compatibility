# 補充 7｜🧠 Raspberry Pi 5 上安裝 Ollama 完整教學（支援 ARM64）

[原始文章](https://liusming.pixnet.net/blog/posts/14223038205) · 更新日期：2026-10-29

## 學習目標

確認本機是否已有 Ollama，以及服務是否啟動。

## 事前準備

本次 RP5 已有 Ollama，以下使用系統現有安裝。

## 實際操作

```bash
command -v ollama
ollama --version
systemctl is-active ollama
```

## 本機實際輸出

```text
/usr/local/bin/ollama
ollama version is 0.9.0
active
```

本機已安裝 0.9.0 且服務 active；沒有在此步驟下載模型、更新版本或驗證聊天。模型的空間與記憶體需求因版本而異。

## 背景與核心概念

### 本地模型服務與推論

Ollama 可用來管理及執行相容的模型；應用程式通常透過服務取得推論結果。程式版本、服務狀態、模型是否存在和模型能否回答，是不同的檢查。

### 思考、練習與後續應用

服務顯示 active 但沒有模型時，能否宣稱聊天推論已成功？選擇模型時應考量哪些記憶體與儲存需求？

本地模型可用於輔助互動原型；應量測速度、回應品質，並檢查資料與模型授權。

進一步閱讀：[相關官方文件](https://docs.ollama.com/)。請以下方實測狀態為準；尚未實作或測試的情境不能視為已通過。

## 概念流程圖

```mermaid
flowchart LR
    A["應用程式"]
    B["Ollama 服務"]
    C["已下載的模型"]
    D["推論回應"]
    A --> B --> C --> D
```

此圖用於說明文章的概念或完整目標流程，**不是操作截圖，也不代表每個步驟都已實測**；本機實測範圍請看文章中的標示。

## 進一步實驗：使用本機既有模型回答問題

Ollama 是模型執行服務；服務程式與模型檔是兩回事。這台 RP5 測試時已裝好 Ollama 0.9.0，且 `ollama list` 已列出 `tinyllama:latest`（約 637 MB），因此本次**沒有重新安裝服務或下載模型**。當模型不在清單中時，需要足夠儲存空間與網路，另行下載並核對模型來源。

1. 使用 `ollama list` 檢查模型、`systemctl is-active ollama` 檢查服務，應先確認模型與服務可用。
2. 下載[本實驗程式](./範例程式/補充7-Ollama本機推論.py)，執行 `python3 補充7-Ollama本機推論.py`。這次請求送到 RP5 本機 `127.0.0.1` 的 Ollama 服務，完成後要求卸載本次模型以釋放資源。
3. `stream: False` 表示等完整回應；`num_predict: 40` 限制生成 token 數。token 不是固定的一個中文字或一個英文單字。參見 [Ollama 官方 Generate API 文件](https://docs.ollama.com/api/generate)。

```python
import json
from urllib.request import Request, urlopen

request_data = {
    'model': 'tinyllama:latest',
    'prompt': 'In one sentence, what does an IoT temperature sensor measure?',
    'stream': False,
    'keep_alive': 0,
    'options': {'temperature': 0, 'num_predict': 40},
}
request = Request('http://127.0.0.1:11434/api/generate',
                  data=json.dumps(request_data).encode('utf-8'),
                  headers={'Content-Type': 'application/json'}, method='POST')
with urlopen(request, timeout=120) as response:
    result = json.load(response)
print('model:', result['model'])
print('response:', result['response'].strip())
print('done:', result['done'])
print('generated tokens:', result.get('eval_count'))
```

這台 RP5 一次實際輸出：

```text
model: tinyllama:latest
response: An IoT temperature sensor measures the temperature in real-time and provides accurate readings based on its sensors' ability to detect changes in temperature caused by various factors such as heat, cold, or
done: True
generated tokens: 40
```

回答在 `or` 處截斷，顯示 `done: True` 只表示生成已結束，不保證句子完整或內容正確。模型聲稱「準確讀數」也需依實際感測器校準與量測驗證，不能只因模型說了就相信。不同版本、設定和硬體可能得到不同文字。本次未量測效能，也未驗證教材原本的安裝及下載過程。

練習：調整輸出長度上限並比較結果；用感測器資料或可信來源檢驗回答，不要把模型回覆視作感測器實際量測值。

## 與原文章的差異

- 新增已存在模型的本機 API 推論；不代表原文安裝與下載流程已重新驗證。

- 原文以安裝 Ollama 為主；本版先檢查已安裝版本，不重複執行安裝或宣稱已完成模型推論。
- 本機測試範圍僅限上述流程；尚未保存操作畫面截圖。
- 新增初學者背景、概念、思考練習及後續應用，實測範圍仍以本文標示為準。
- 加入教學流程示意；圖中的完整目標流程不代表已逐步實測。
