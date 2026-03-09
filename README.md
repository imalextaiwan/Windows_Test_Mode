# Windows 開機設定工具
**Windows Boot Configuration Tool** `v1.0`

> 一鍵查詢並切換 Secure Boot 狀態與 Windows Test Mode（測試模式）的圖形化工具。

![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Admin](https://img.shields.io/badge/Required-Administrator-red)

---

## 功能特色

- **Secure Boot 狀態查詢** — 即時偵測 UEFI Secure Boot 是否啟用
- **Test Mode 一鍵切換** — 透過 `bcdedit` 開啟／關閉 Windows 測試模式
- **BIOS 快速進入** — 使用 `shutdown /fw` 重開機直接進入 UEFI 設定介面
- **手動 BIOS 引導** — 無法自動進入時，提供各品牌主機板快捷鍵一覽
- **LOG 自動記錄** — 所有操作記錄於 `LOGS/` 資料夾，方便除錯追蹤
- **深色主題 UI** — 採用 Catppuccin Mocha 配色，介面簡潔清晰

---

## 系統需求

| 項目 | 需求 |
|------|------|
| 作業系統 | Windows 10 / 11 |
| Python 版本 | 3.8 或以上 |
| 執行權限 | **系統管理員（Administrator）** |
| 相依套件 | 僅使用 Python 標準函式庫（tkinter、subprocess、ctypes） |

---

## 安裝與執行

### 方法一：直接執行 Python 腳本

```bash
# 1. Clone 或下載本專案
git clone https://github.com/imalextaiwan/windows-boot-tool.git
cd windows-boot-tool

# 2. 以系統管理員身分執行
# 右鍵 → 以系統管理員身分執行 PowerShell，然後：
python boot_tool.py
```

### 方法二：打包為獨立執行檔（.exe）

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --uac-admin boot_tool.py
# 輸出位於 dist/boot_tool.exe
```

> 本工具需要 **管理員權限**。若以一般使用者身分執行，程式會自動觸發 UAC 提升請求。

---

## 使用說明

### 1. 查詢狀態
程式啟動後會自動查詢目前的 **Secure Boot** 與 **Test Mode** 狀態，並以色條指示：

| 顏色 | 意義 |
|------|------|
| 綠色 | Secure Boot 已關閉 ／ Test Mode 已開啟 |
| 紅色 | Secure Boot 已開啟（需進 BIOS 關閉才能開 Test Mode） |
| 灰色 | 無法判斷（通常為 Legacy BIOS 環境） |

### 2. 開啟 Test Mode
1. 確認 Secure Boot 已關閉（狀態列顯示綠色）
2. 點擊「**開啟 Test Mode**」按鈕
3. 依提示重新啟動電腦

> 啟用後桌面右下角會出現「Test Mode」浮水印，這是正常現象。

### 3. 進入 BIOS 關閉 Secure Boot
1. 點擊「**進入 BIOS**」按鈕
2. 電腦將在 3 秒後重開並自動進入 UEFI BIOS
3. 找到 `Secure Boot` 選項 → 設為 `Disabled`
4. 按 `F10` 儲存並離開
5. 重開機後再次執行本工具

---

## 專案結構

```
windows-boot-tool/
├── boot_tool.py        # 主程式
├── LOGS/               # 自動產生的操作記錄（.log）
├── README.md
└── readme.txt
```

---

## 注意事項

- 切換 Test Mode 後**必須重新啟動**電腦才會生效
- 在 Secure Boot 啟用的狀態下，無法開啟 Test Mode
- 本工具僅修改 BCD（開機設定資料）中的 `testsigning` 項目，不會變更任何系統檔案
- 建議在了解用途後再行操作，如有疑慮請先備份 BCD：
  ```cmd
  bcdedit /export C:\bcd_backup
  ```

---

## 授權條款（License）

```
MIT License

Copyright (c) 2025 Alex Huang (https://github.com/imalextaiwan)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

## 貢獻方式

歡迎提交 Issue 或 Pull Request！

1. Fork 本專案
2. 建立你的功能分支：`git checkout -b feature/your-feature`
3. 提交變更：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 開啟 Pull Request

---

## 常見問題

**Q: 為什麼需要管理員權限？**  
A: `bcdedit` 屬於系統層級指令，修改開機設定必須有管理員身分。

**Q: 關閉 Test Mode 後浮水印還在？**  
A: 需要重新啟動電腦後才會移除。

**Q: `shutdown /fw` 無法自動進入 BIOS？**  
A: 部分較舊主機板不支援此指令，程式會自動顯示手動引導視窗，提供各品牌 BIOS 快捷鍵。

**Q: Legacy BIOS 能使用嗎？**  
A: Secure Boot 為 UEFI 專屬功能，Legacy BIOS 環境下此項目會顯示「無法判斷」，但 Test Mode 切換功能仍可正常使用。

---

<p align="center">
  Made by <a href="https://github.com/imalextaiwan">Alex Huang</a>
</p>
