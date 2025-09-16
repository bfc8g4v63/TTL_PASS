好，我幫你把 **TTL\_PASS.py** 從 v1.0.0 \~ v1.1.5 的 15 次更新整理成一份更新紀錄，並排版成可以直接轉換成 **Try Markmap** 的巢狀結構心智圖格式。

---

# TTL\_PASS

## 功能簡介

* 自動提升為系統管理員執行
* 設定 TTL=65 並驗證
* 偵測並關閉 Apple Mobile Device Ethernet 的 IPv6

---

## 更新紀錄

### v1.1.5 — 改善穩定性

* 完整使用 **InterfaceDescription** 進行網卡鎖定，不受 `乙太網路 2`、中文名稱影響。
* IPv6 關閉檢查邏輯修正，已成功穩定執行。

### v1.1.4 — IPv6 狀態檢查

* 新增 `ipv6_status_by_desc()`，先檢查 IPv6 是否啟用。
* 若 IPv6 已關閉則跳過，不再報錯。

### v1.1.3 — 名稱引號處理

* `Disable-NetAdapterBinding` 的 `-Name` 參數改成單引號包裹，避免空白名稱（例：`乙太網路 2`）被切開。

### v1.1.2 — JSON 適配

* `Get-NetAdapter` → `ConvertTo-Json` → Python 解析，避免亂碼。
* 能正確處理中文、數字混合的網卡名稱。

### v1.1.1 — 找不到網卡提示

* 偵測不到 Apple 網卡時，回傳「找不到 Apple Mobile Device Ethernet」。
* 改善錯誤訊息易讀性。

### v1.1.0 — Apple 熱點 IPv6 偵測

* 新增 Apple Mobile Device Ethernet 偵測。
* 自動嘗試執行 `Disable-NetAdapterBinding` 關閉 IPv6。

### v1.0.9 — CLI 保持

* UAC 提權後改用 `/k`，確保 CLI 視窗保持開啟。

### v1.0.8 — 提權與執行分離

* `relaunch_as_admin()` 改善，避免無限重啟。
* CLI 參數 `--elevated` 用於區分已提權狀態。

### v1.0.7 — Wait 機制優化

* `wait_at_end()` 支援 `input()` 與 `os.system("pause")` 雙備援。
* 避免部分環境下閃退。

### v1.0.6 — TTL 驗證輸出

* 新增 `check_ttl()`，Ping `127.0.0.1` 驗證設定是否成功。
* CLI 顯示 TTL 值。

### v1.0.5 — 提權機制修正

* 改用 `ShellExecuteW` 方式啟動自身 Python 腳本。
* 避免「檔案名稱語法錯誤」問題。

### v1.0.4 — CLI 提權測試

* 新增提權後保持 CLI 視窗功能。
* 修正 Windows 下執行 `cmd.exe` 路徑問題。

### v1.0.3 — 多編碼解碼

* 增加 `errors="ignore"`，避免 `cp950` / UnicodeDecodeError。

### v1.0.2 — 子程序回傳檢查

* `set_ttl()` 與 `check_ttl()` 都改用 `subprocess.run`。
* 統一回傳 `(code, stdout, stderr)`。

### v1.0.1 — 自動提權雛形

* 檢查是否為管理員，不是則自動重啟自身並要求提權。

### v1.0.0 — 初版

* 設定 TTL=65。
* 基本 CLI 輸出。
* 停住等待 Enter。

---

要不要我幫你把這份直接轉換成 **Markdown Markmap 格式**，你就可以在 Try Markmap 中直接展開心智圖？
