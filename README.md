# TTL\_PASS

## 功能簡介

* 自動提升為系統管理員執行  
* 進行系統網路優化（TTL 檢查與設定）  
* 自動偵測 Apple Mobile Device Ethernet 或 Wi-Fi 熱點介面  
* 自動關閉偵測到的 IPv6 並驗證設定結果  
* 優化完成後顯示「連線介面已完成優化設定」  

---

## 更新紀錄

### v1.1.8 — 修正亂碼與介面偵測

* 修正 PowerShell 輸出亂碼導致「乙太網路 2」顯示異常（例如「AӺ 2」或「^Ц」）。  
* 改用 **InterfaceDescription** 全域識別，完全不依賴網卡名稱。  
* 強化 Windows 語系環境兼容（支援中文/英文混合顯示）。  
* 優化輸出順序與 CLI 顯示格式，確保「狀態檢查」與「連線介面」輸出一致。  

### v1.1.7 — IPv6 關閉狀態回報與 Wi-Fi 偵測

* 新增 Wi-Fi 熱點介面自動偵測機制，當未偵測到 Apple Mobile Device Ethernet 時，會自動偵測目前連線的 Wi-Fi 網卡。  
* 新增 IPv6 關閉成功與已關閉狀態分別提示。  
* 增加多層次 Try/Except 防呆，避免 PowerShell 執行中斷。  
* 改善 log 顯示順序，確保 CLI 一致性。  

### v1.1.6 — 網卡清單防呆

* 增加空清單檢查：若找不到任何介面則顯示「未偵測到任何網卡」。  
* 修正部分環境下 `json.loads()` 錯誤的例外處理邏輯。  
* 增加回傳結果驗證與錯誤代碼對應。  

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