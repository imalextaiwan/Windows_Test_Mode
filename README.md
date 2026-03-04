# Windows_Test_Mode
A GUI tool for Windows to check &amp; toggle Secure Boot and Test Mode (testsigning) via bcdedit. Features auto UAC elevation, reboot-to-UEFI, dual-state verification, and timestamped logging. Requires administrator privileges.
```
================================================================
  Windows 開機設定工具  v1.0
  Windows Boot Configuration Tool  v1.0
================================================================

【系統需求 / System Requirements】
  - Windows OS（需支援 UEFI / UEFI support required）
  - Python 3.x（含 tkinter / tkinter included）
  - 系統管理員權限 / Administrator privileges

================================================================
【啟動方式 / How to Launch】
================================================================

  1. 雙擊執行 Test_Mode.py
     Double-click to run Test_Mode.py

  2. 出現 UAC 視窗時，點選「是」
     When the UAC prompt appears, click "Yes"

  3. 若自動提權失敗，右鍵 -> 以系統管理員身分執行
     If auto-elevation fails, right-click
     -> Run as administrator

  程式啟動後自動建立 Log 檔：
  On startup, the program automatically creates:
    LOGS\boot_tool_YYYYMMDD_HHMMSS.log

================================================================
【主介面說明 / Main Interface Overview】
================================================================

  介面分為三個區塊：
  The interface is divided into three sections:

  +--------------------------------------------------+
  |  Section 1：Secure Boot 狀態卡片 Status Card      |
  |  Section 2：Test Mode 狀態卡片 Status Card        |
  |  Section 3：操作按鈕列 Action Buttons             |
  +--------------------------------------------------+

  --[ Secure Boot 狀態卡片 / Status Card ]--

  左側色條 / Left color bar：
    紅色 Red   = Secure Boot 已開啟 (Enabled)
    綠色 Green = Secure Boot 已關閉 (Disabled)
    灰色 Gray  = 無法判斷 / Cannot detect (Legacy BIOS)

  Secure Boot 開啟時顯示警告 / Warning when ON:
    "需先關閉 Secure Boot 才能啟用 Test Mode"
    "Secure Boot must be disabled before enabling
     Test Mode"
  並顯示「進入 BIOS」按鈕
  "Enter BIOS" button appears in the action row.

  --[ Test Mode 狀態卡片 / Status Card ]--

  左側色條 / Left color bar：
    綠色 Green = Test Mode 已啟用 (Enabled)
    灰色 Gray  = Test Mode 已關閉 (Disabled)

  啟用時顯示提示 / Notice when enabled:
    "已啟用時桌面右下角會顯示 Test Mode 浮水印"
    "Watermark will appear at bottom-right of desktop"

  --[ 操作按鈕列 / Action Buttons ]--

  [進入 BIOS / Enter BIOS]
    Secure Boot 開啟時才顯示
    Shown only when Secure Boot is ON
    確認後 3 秒重開機自動進入 UEFI BIOS
    Reboots into UEFI BIOS in 3 seconds after confirm

  [開啟 Test Mode / Enable Test Mode]  (藍色 Blue)
    Secure Boot 已關閉且 Test Mode 目前為關閉時顯示
    Shown when Secure Boot is OFF, Test Mode is OFF

  [關閉 Test Mode / Disable Test Mode]  (紅色 Red)
    Test Mode 目前開啟時顯示
    Shown when Test Mode is currently enabled

  [重新整理 / Refresh]
    手動重新查詢兩項狀態，查詢中顯示旋轉動畫
    Manually re-queries both statuses with spinner

================================================================
【標準操作流程 / Standard Operating Procedures】
================================================================

  情境 A / Scenario A：
  啟用 Test Mode（Secure Boot 已關閉）
  Enable Test Mode (Secure Boot already OFF)
  -------------------------------------------
  1. 啟動程式，確認 Secure Boot 色條為綠色
     Launch the program; confirm Secure Boot bar is Green
  2. 點擊「開啟 Test Mode」（藍色按鈕）
     Click "Enable Test Mode" (blue button)
  3. 程式執行 bcdedit 並自動驗證結果
     Program runs bcdedit and auto-verifies the result
  4. 驗證成功後選擇「是」立即重新啟動
     On success, select "Yes" to reboot immediately
  5. 重開後桌面右下角出現浮水印 = 成功
     Watermark appears at bottom-right after reboot = done

  情境 B / Scenario B：
  啟用 Test Mode（Secure Boot 仍開啟）
  Enable Test Mode (Secure Boot still ON)
  -------------------------------------------
  1. Secure Boot 色條為紅色，點擊「進入 BIOS」
     Secure Boot bar is Red, click "Enter BIOS"
  2. 確認後電腦重開並自動進入 UEFI BIOS
     Confirm, system reboots directly into UEFI BIOS
  3. 找到 Secure Boot -> 設為 Disabled
     Find Secure Boot -> set to Disabled
  4. 按 F10 儲存並離開 / Press F10 to save and exit
  5. 重開後再執行程式，依情境 A 操作
     Run the program again and follow Scenario A

  情境 C / Scenario C：
  關閉 Test Mode / Disable Test Mode
  -------------------------------------------
  1. 確認 Test Mode 色條為綠色
     Confirm Test Mode bar is Green
  2. 點擊「關閉 Test Mode」（紅色按鈕）
     Click "Disable Test Mode" (red button)
  3. 驗證成功後重新啟動，浮水印消失
     After verification, reboot; watermark disappears

================================================================
【自動進入 BIOS 失敗時 / If Auto BIOS Reboot Fails】
================================================================

  程式顯示手動引導視窗，常見品牌快捷鍵如下：
  A manual guide window appears with BIOS hotkeys:

    ASUS      Del / F2       MSI       Del
    Gigabyte  Del / F2       ASRock    F2 / Del
    HP        F10 / Esc      Dell      F2 / F12
    Lenovo    F1 / F2        Acer      F2 / Del

  步驟 Steps：
  1. 手動重新啟動電腦 / Manually restart your computer
  2. 開機時連續按下對應快捷鍵
     Repeatedly press your brand's hotkey during POST
  3. 找到 Secure Boot -> 設為 Disabled
     Find Secure Boot -> set to Disabled
  4. F10 儲存離開 / F10 to save and exit
  5. 重開後再次執行本程式
     Run the program again after reboot

================================================================
【LOG 說明 / Log Files】
================================================================

  位置 Location : LOGS\ 資料夾（程式同目錄）
                  LOGS\ folder (same directory as program)
  格式 Filename  : boot_tool_YYYYMMDD_HHMMSS.log
  內容 Contents  : 所有操作、查詢結果、錯誤訊息
                  All operations, results, error messages
  開啟 Access    : 點擊底部「開啟 LOG」開啟資料夾
                  Click "Open LOG" to open the folder

================================================================
【常見問題 / FAQ】
================================================================

  Q: Test Mode 按鈕是灰色，無法點擊？
     The Test Mode button is grayed out?
  A: Secure Boot 仍開啟，請先進入 BIOS 關閉。
     Secure Boot is still ON. Disable it in BIOS first.

  Q: 切換後狀態沒有變化？
     Status did not change after toggling?
  A: 點擊「重新整理」，或確認電腦已重新啟動。
     Click "Refresh", or confirm the PC has rebooted.

  Q: 驗證失敗訊息出現？
     Verification failed message appears?
  A: 可能 Secure Boot 未完全關閉，或需重開機後再驗證。
     Secure Boot may not be fully disabled, or a reboot
     is required before verification.

  Q: 程式閃一下就消失？
     Window flashes and disappears immediately?
  A: UAC 提權被取消，請右鍵以系統管理員身分執行。
     UAC was cancelled. Right-click -> Run as administrator.

================================================================
  版本 Version : v1.0
  作者 Author  : imalextaiwan
================================================================
```
