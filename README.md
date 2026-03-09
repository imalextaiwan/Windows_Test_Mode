[import tkinter as tk_from tkinter import messagebo.md](https://github.com/user-attachments/files/25840983/import.tkinter.as.tk_from.tkinter.import.messagebo.md)
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# import tkinter as tk

from tkinter import messagebox
import subprocess
import ctypes
import sys
import re
import time
import threading
import logging
from datetime import datetime
from pathlib import Path

# ══════════════════════════════════════════════

# 色彩主題

# ══════════════════════════════════════════════

BG         = "\#1e1e2e"
CARD_BG    = "\#2a2a3e"
BORDER     = "\#3a3a5c"
TEXT_PRI   = "\#cdd6f4"
TEXT_SEC   = "\#6c7086"
GREEN      = "\#a6e3a1"
RED        = "\#f38ba8"
YELLOW     = "\#f9e2af"
BLUE       = "\#89dceb"
ORANGE     = "\#fab387"
BTN_DANGER = "\#f38ba8"
BTN_FG     = "\#1e1e2e"
ACCENT     = "\#89dceb"

FONT       = "微軟正黑體"
VERSION    = "v1.0"

# ══════════════════════════════════════════════

# LOG 初始化

# ══════════════════════════════════════════════

def init_logger():
base_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
log_dir  = base_dir / "LOGS"
log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"boot_tool_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  [%(levelname)s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
        ]
    )
    logging.info("═" * 50)
    logging.info("程式啟動")
    logging.info(f"Log 路徑：{log_file}")
    logging.info("═" * 50)
    return log_file
    
# ══════════════════════════════════════════════

# 管理員權限

# ══════════════════════════════════════════════

def is_admin():
try:
return ctypes.windll.shell32.IsUserAnAdmin()
except:
return False

def require_admin():
if not is_admin():
logging.warning("非管理員身分，嘗試自動提升權限...")
try:
if getattr(sys, "frozen", False):
script = sys.executable
params = " ".join(sys.argv[1:])
else:
script = sys.executable
params = " ".join([sys.argv[0]] + sys.argv[1:])

            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", script, params, None, 1
            )
            logging.info("已送出 UAC 提升請求，原程序退出")
        except Exception as e:
            logging.error(f"UAC 提升失敗：{e}")
            messagebox.showerror(
                "權限不足",
                "無法自動取得管理員權限。\\n請右鍵 → 以系統管理員身分執行。"
            )
        sys.exit(0)
    logging.info("管理員權限確認 OK")
    
# ══════════════════════════════════════════════

# 視窗置中

# ══════════════════════════════════════════════

def _center_window(win, w, h):
win.update_idletasks()
sw = win.winfo_screenwidth()
sh = win.winfo_screenheight()
x  = (sw - w) // 2
y  = (sh - h) // 2
win.geometry(f"{w}x{h}+{x}+{y}")

# ══════════════════════════════════════════════

# Tooltip

# ══════════════════════════════════════════════

class Tooltip:
def __init__(self, widget, text):
self.widget = widget
self.text   = text
self.tw     = None
widget.bind("<Enter>", self._show)
widget.bind("<Leave>", self._hide)

    def _show(self, _=None):
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        tk.Label(
            self.tw, text=self.text,
            font=(FONT, 9), bg="#313244", fg=TEXT_PRI,
            relief="flat", padx=8, pady=4
        ).pack()
    
    def _hide(self, _=None):
        if self.tw:
            self.tw.destroy()
            self.tw = None
    
# ══════════════════════════════════════════════

# Hover 效果

# ══════════════════════════════════════════════

def add_hover(btn, normal_color, hover_color=None):
if hover_color is None:
try:
r = min(255, int(normal_color[1:3], 16) + 30)
g = min(255, int(normal_color[3:5], 16) + 30)
b = min(255, int(normal_color[5:7], 16) + 30)
hover_color = f"\#{r:02x}{g:02x}{b:02x}"
except:
hover_color = normal_color

    btn.bind("<Enter>", lambda _: btn.config(bg=hover_color) if str(btn["state"]) != "disabled" else None)
    btn.bind("<Leave>", lambda _: btn.config(bg=normal_color) if str(btn["state"]) != "disabled" else None)
    
# ══════════════════════════════════════════════

# 系統查詢

# ══════════════════════════════════════════════

def check_secure_boot():
logging.info("查詢 Secure Boot 狀態...")
try:
result = subprocess.run(
["powershell", "-NoProfile", "-NonInteractive",
"-ExecutionPolicy", "Bypass",
"-Command", "Confirm-SecureBootUEFI"],
capture_output=True, text=True, timeout=10
)
output = result.stdout.strip().lower()
if output == "true":
logging.info("Secure Boot：Enabled")
return True
elif output == "false":
logging.info("Secure Boot：Disabled")
return False
logging.warning(f"Secure Boot 無法判斷，輸出：{output!r}")
return None
except Exception as e:
logging.error(f"Secure Boot 查詢失敗：{e}")
return None

def get_test_mode_status():
logging.info("查詢 Test Mode 狀態...")
try:
result = subprocess.run(
["powershell", "-NoProfile", "-NonInteractive",
"-ExecutionPolicy", "Bypass",
"-Command",
"(bcdedit /enum '{current}' | Select-String 'testsigning') -match 'Yes'"],
capture_output=True, text=True, timeout=10
)
ps_out = result.stdout.strip().lower()
logging.info(f"PowerShell testsigning 查詢結果：{ps_out!r}")

        if ps_out == "true":
            logging.info("Test Mode：Enabled")
            return True
        elif ps_out == "false":
            logging.info("Test Mode：Disabled")
            return False
    
        logging.warning("PowerShell 查詢無法判斷，改用 bcdedit fallback")
        fallback = subprocess.run(
            [r"C:\\Windows\\System32\\bcdedit.exe", "/enum", "{current}"],
            capture_output=True, timeout=10
        )
        output = fallback.stdout.decode("cp950", errors="replace").lower()
        logging.info(f"bcdedit fallback 輸出（前300字）：{output[:300]!r}")
        status = re.search(r"testsigning\\s+yes", output) is not None
        logging.info(f"Test Mode（fallback）：{'Enabled' if status else 'Disabled'}")
        return status
    
    except Exception as e:
        logging.error(f"Test Mode 查詢失敗：{e}")
        return False
    
# ══════════════════════════════════════════════

# UI 元件工廠

# ══════════════════════════════════════════════

def make_card(parent, **kwargs):
return tk.Frame(
parent,
bg=CARD_BG,
highlightbackground=BORDER,
highlightthickness=1,
**kwargs
)

def make_label(parent, text, size=10, bold=False, color=TEXT_PRI, **kwargs):
weight = "bold" if bold else "normal"
return tk.Label(
parent,
text=text,
font=(FONT, size, weight),
bg=parent["bg"],
fg=color,
**kwargs
)

def make_btn(parent, text, command, color=BLUE, width=16):
btn = tk.Button(
parent,
text=text,
font=(FONT, 10, "bold"),
bg=color,
fg=BTN_FG,
activebackground=color,
activeforeground=BTN_FG,
relief="flat",
bd=0,
padx=10,
pady=7,
width=width,
cursor="hand2",
command=command
)
add_hover(btn, color)
return btn

# ══════════════════════════════════════════════

# 狀態卡片（Secure Boot）含左側色條

# ══════════════════════════════════════════════

def build_secure_boot_card(parent):
outer = tk.Frame(parent, bg=BG)
outer.pack(fill="x", padx=24, pady=(16, 8))

    sb_bar = tk.Frame(outer, bg=BORDER, width=4)
    sb_bar.pack(side="left", fill="y")
    
    card = tk.Frame(outer, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
    card.pack(side="left", fill="x", expand=True)
    
    header = tk.Frame(card, bg=CARD_BG)
    header.pack(fill="x", padx=16, pady=(10, 4))
    make_label(header, "🔒  Secure Boot", size=11, bold=True).pack(side="left")
    
    body = tk.Frame(card, bg=CARD_BG)
    body.pack(fill="x", padx=16, pady=(0, 10))
    
    sb_icon = make_label(body, "●", size=13, color=TEXT_SEC)
    sb_icon.pack(side="left")
    sb_text = make_label(body, "查詢中...", size=10, color=TEXT_SEC)
    sb_text.pack(side="left", padx=(6, 0))
    sb_hint = make_label(body, "", size=9, color=TEXT_SEC)
    sb_hint.pack(side="right")
    
    return sb_icon, sb_text, sb_hint, sb_bar
    
# ══════════════════════════════════════════════

# 狀態卡片（Test Mode）含左側色條

# ══════════════════════════════════════════════

def build_test_mode_card(parent):
outer = tk.Frame(parent, bg=BG)
outer.pack(fill="x", padx=24, pady=(0, 8))

    tm_bar = tk.Frame(outer, bg=BORDER, width=4)
    tm_bar.pack(side="left", fill="y")
    
    card = tk.Frame(outer, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
    card.pack(side="left", fill="x", expand=True)
    
    header = tk.Frame(card, bg=CARD_BG)
    header.pack(fill="x", padx=16, pady=(10, 4))
    make_label(header, "🧪  Test Mode", size=11, bold=True).pack(side="left")
    
    body = tk.Frame(card, bg=CARD_BG)
    body.pack(fill="x", padx=16, pady=(0, 4))
    
    tm_icon = make_label(body, "●", size=13, color=TEXT_SEC)
    tm_icon.pack(side="left")
    tm_text = make_label(body, "查詢中...", size=10, color=TEXT_SEC)
    tm_text.pack(side="left", padx=(6, 0))
    
    tm_warn = make_label(card, "⚠  已啟用時桌面右下角會顯示 Test Mode 浮水印", size=8, color=ORANGE)
    tm_warn.pack(anchor="w", padx=16, pady=(0, 8))
    tm_warn.pack_forget()
    
    return tm_icon, tm_text, tm_bar, tm_warn
    
# ══════════════════════════════════════════════

# 操作區

# ══════════════════════════════════════════════

def build_action_area(parent):
area = tk.Frame(parent, bg=BG)
area.pack(fill="x", padx=24, pady=(4, 0))

    bios_btn = make_btn(
        area, "⚙️  進入 BIOS",
        command=guide_disable_secure_boot,
        color=YELLOW, width=13
    )
    bios_btn.config(fg=BTN_FG)
    Tooltip(bios_btn, "重開機並自動進入 BIOS 設定介面")
    
    toggle_btn = make_btn(area, "⏳  載入中...", command=lambda: None, color=TEXT_SEC)
    Tooltip(toggle_btn, "開啟或關閉 Windows Test Mode（測試模式）")
    
    spacer = tk.Frame(area, bg=BG)
    
    refresh_btn = make_btn(
        area, "🔄  重新整理",
        command=lambda: threading.Thread(target=refresh_status, daemon=True).start(),
        color=BORDER, width=11
    )
    refresh_btn.config(fg=TEXT_PRI)
    Tooltip(refresh_btn, "重新查詢 Secure Boot 與 Test Mode 狀態")
    
    bios_btn.pack(side="left")
    bios_btn.pack_forget()
    toggle_btn.pack(side="left")
    spacer.pack(side="left", expand=True, fill="x")
    refresh_btn.pack(side="left")
    
    return toggle_btn, bios_btn, refresh_btn
    
# ══════════════════════════════════════════════

# 底部提示 + 上次更新時間 + LOG 開啟按鈕

# ══════════════════════════════════════════════

def build_footer(parent, log_file: Path):
footer = tk.Frame(parent, bg=BG)
footer.pack(fill="x", padx=24, pady=(10, 4))

    make_label(footer, "⚠  切換後需重新啟動電腦才會生效", size=9, color=TEXT_SEC).pack(side="left")
    
    log_btn = tk.Label(
        footer,
        text="📂 開啟 LOG",
        font=(FONT, 8, "underline"),
        bg=BG, fg=TEXT_SEC,
        cursor="hand2"
    )
    log_btn.pack(side="right", padx=(8, 0))
    log_btn.bind("<Button-1>", lambda _: open_log_folder(log_file))
    Tooltip(log_btn, f"開啟 LOG 資料夾：{log_file.parent}")
    
    footer2 = tk.Frame(parent, bg=BG)
    footer2.pack(fill="x", padx=24, pady=(0, 12))
    
    global last_update_lbl
    last_update_lbl = make_label(footer2, "上次更新：--:--:--", size=8, color=TEXT_SEC)
    last_update_lbl.pack(side="left")
    make_label(footer2, f"📄 {log_file.name}", size=8, color=TEXT_SEC).pack(side="right")
    def open_log_folder(log_file: Path):
logging.info(f"開啟 LOG 資料夾：{log_file.parent}")
subprocess.Popen(["explorer", str(log_file.parent)])

# ══════════════════════════════════════════════

# 旋轉動畫

# ══════════════════════════════════════════════

_spin_idx = 0
_spin_job = None

def _start_spin():
global _spin_idx, _spin_job
_spin_idx = 0

    def _tick():
        global _spin_idx, _spin_job
        frames = ["◐", "◓", "◑", "◒"]
        refresh_btn.config(text=f"{frames[_spin_idx % 4]}  重新整理")
        _spin_idx += 1
        _spin_job = root.after(150, _tick)
    
    _tick()
    def _stop_spin():
global _spin_job
if _spin_job:
root.after_cancel(_spin_job)
_spin_job = None
refresh_btn.config(text="🔄  重新整理")

# ══════════════════════════════════════════════

# 閃爍 feedback

# ══════════════════════════════════════════════

def flash_card(bar_widget, color, times=3):
def _blink(n, on):
if n <= 0:
bar_widget.config(bg=color)
return
bar_widget.config(bg=color if on else BORDER)
root.after(120, lambda: _blink(n - 1, not on))
_blink(times * 2, True)

# ══════════════════════════════════════════════

# 重開機詢問（系統原生視窗）

# ══════════════════════════════════════════════

def _ask_reboot(action: str):
ans = messagebox.askyesno(
"需要重新啟動",
f"Test Mode 已{action}。\\n\\n"
"需要重新啟動電腦才會生效。\\n\\n"
"是否立即重新啟動？"
)
if ans:
logging.info("使用者選擇立即重開機")
subprocess.run(["shutdown", "/r", "/t", "3"])
else:
logging.info("使用者選擇稍後手動重開機")

# ══════════════════════════════════════════════

# 刷新狀態

# ══════════════════════════════════════════════

def refresh_status():
root.after(0, _set_loading)
logging.info("── 刷新狀態 ──")

    sb_result = [None]
    tm_result = [None]
    
    def _query_sb():
        sb_result[0] = check_secure_boot()
    
    def _query_tm():
        tm_result[0] = get_test_mode_status()
    
    t1 = threading.Thread(target=_query_sb, daemon=True)
    t2 = threading.Thread(target=_query_tm, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    root.after(0, lambda: _apply_status(sb_result[0], tm_result[0]))
    def _set_loading():
_start_spin()
sb_icon_lbl.config(text="●", fg=TEXT_SEC)
sb_text_lbl.config(text="查詢中...", fg=TEXT_SEC)
sb_hint_lbl.config(text="")
tm_icon_lbl.config(text="●", fg=TEXT_SEC)
tm_text_lbl.config(text="查詢中...", fg=TEXT_SEC)
toggle_btn.config(text="⏳  載入中...", bg=TEXT_SEC, state="disabled")
bios_btn.pack_forget()
tm_warn_lbl.pack_forget()

def _apply_status(sb, tm):
_stop_spin()
last_update_lbl.config(text=f"上次更新：{datetime.now().strftime('%H:%M:%S')}")
logging.info(f"_apply_status 呼叫：sb={sb}, tm={tm}")

    # ── Secure Boot ──
    if sb is True:
        sb_icon_lbl.config(fg=RED)
        sb_text_lbl.config(text="已開啟 (Enabled)", fg=RED)
        sb_hint_lbl.config(text="⚠ 需先進BIOS後關閉 Secure Boot 才能啟用 Test Mode", fg=YELLOW)
        sb_bar.config(bg=RED)
        bios_btn.pack(side="left")
    elif sb is False:
        sb_icon_lbl.config(fg=GREEN)
        sb_text_lbl.config(text="已關閉 (Disabled)", fg=GREEN)
        sb_hint_lbl.config(text="")
        sb_bar.config(bg=GREEN)
        bios_btn.pack_forget()
    else:
        sb_icon_lbl.config(fg=TEXT_SEC)
        sb_text_lbl.config(text="無法判斷（Legacy BIOS）", fg=TEXT_SEC)
        sb_hint_lbl.config(text="")
        sb_bar.config(bg=BORDER)
        bios_btn.pack_forget()
    
    # ── Test Mode 狀態文字 + 色條 + 浮水印提示 ──
    if tm:
        tm_icon_lbl.config(fg=GREEN)
        tm_text_lbl.config(text="已啟用 (Enabled)", fg=GREEN)
        tm_bar.config(bg=GREEN)
        tm_warn_lbl.pack(anchor="w", padx=16, pady=(0, 8))
    else:
        tm_icon_lbl.config(fg=TEXT_SEC)
        tm_text_lbl.config(text="已關閉 (Disabled)", fg=TEXT_SEC)
        tm_bar.config(bg=BORDER)
        tm_warn_lbl.pack_forget()
    
    # ── Test Mode 按鈕 ──
    if sb is True:
        toggle_btn.config(
            text="開啟 Test Mode",
            bg=BORDER, fg=TEXT_SEC,
            state="disabled",
            cursor="arrow"
        )
        add_hover(toggle_btn, BORDER)
    elif tm:
        toggle_btn.config(
            text="關閉 Test Mode",
            bg=BTN_DANGER, fg=BTN_FG,
            state="normal",
            cursor="hand2",
            command=lambda: toggle_test_mode(False)
        )
        add_hover(toggle_btn, BTN_DANGER)
    else:
        toggle_btn.config(
            text="開啟 Test Mode",
            bg=BLUE, fg=BTN_FG,
            state="normal",
            cursor="hand2",
            command=lambda: toggle_test_mode(True)
        )
        add_hover(toggle_btn, BLUE)
    
# ══════════════════════════════════════════════

# 切換 Test Mode

# ══════════════════════════════════════════════

def toggle_test_mode(enable: bool):
action = "開啟" if enable else "關閉"
logging.info(f"使用者操作：{action} Test Mode")

    value = "on" if enable else "off"
    try:
        result = subprocess.run(
            [r"C:\\Windows\\System32\\bcdedit.exe", "/set", "{current}", "testsigning", value],
            capture_output=True, timeout=10
        )
        output = result.stdout.decode("cp950", errors="replace")
        logging.info(f"bcdedit /set 輸出：{output.strip()!r}")
    
        if result.returncode == 0:
            verify = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive",
                 "-ExecutionPolicy", "Bypass",
                 "-Command",
                 "(bcdedit /enum '{current}' | Select-String 'testsigning') -match 'Yes'"],
                capture_output=True, text=True, timeout=10
            )
            ps_verify = verify.stdout.strip().lower()
            logging.info(f"驗證 PowerShell 結果：{ps_verify!r}")
    
            if ps_verify not in ("true", "false"):
                fb = subprocess.run(
                    [r"C:\\Windows\\System32\\bcdedit.exe", "/enum", "{current}"],
                    capture_output=True, timeout=10
                )
                fb_out = fb.stdout.decode("cp950", errors="replace").lower()
                actual_enabled = re.search(r"testsigning\\s+yes", fb_out) is not None
            else:
                actual_enabled = (ps_verify == "true")
    
            actual = actual_enabled if enable else not actual_enabled
    
            if actual:
                logging.info(f"Test Mode {action}驗證成功")
                flash_card(tm_bar, GREEN if enable else BORDER)
                threading.Thread(target=refresh_status, daemon=True).start()
                # 閃爍完畢後跳系統原生重開機詢問視窗
                root.after(600, lambda: _ask_reboot(action))
            else:
                logging.error(f"Test Mode {action}指令成功但驗證失敗")
                messagebox.showerror(
                    "驗證失敗",
                    f"指令執行成功，但驗證後 Test Mode 狀態未改變。\\n\\n"
                    "可能原因：\\n"
                    "• Secure Boot 仍開啟\\n"
                    "• 系統保護機制阻擋\\n"
                    "• 需要重開機後才能驗證"
                )
        else:
            err = result.stdout.decode("cp950", errors="replace").strip()
            logging.error(f"bcdedit 失敗 (code {result.returncode})：{err}")
            messagebox.showerror("操作失敗", f"指令失敗 (code {result.returncode})：\\n{err}")
    except Exception as e:
        logging.exception(f"toggle_test_mode 例外：{e}")
        messagebox.showerror("錯誤", str(e))
    
# ══════════════════════════════════════════════

# 重開機進入 UEFI BIOS

# ══════════════════════════════════════════════

def reboot_to_uefi():
def _attempt(retry=False):
attempt_no = 2 if retry else 1
logging.info(f"執行 shutdown /r /fw /t 3（第 {attempt_no} 次）")
try:
result = subprocess.run(
["shutdown", "/r", "/fw", "/t", "3"],
capture_output=True, text=True, timeout=10
)
if result.returncode == 0:
logging.info("shutdown /fw 送出成功")
return
if not retry:
logging.warning(f"第 1 次失敗，retry：{result.stderr.strip()}")
subprocess.run(["shutdown", "/a"], capture_output=True)
time.sleep(1)
_attempt(retry=True)
else:
err = result.stderr.strip() or result.stdout.strip()
logging.error(f"shutdown /fw 第 2 次仍失敗：{err}")
root.after(0, lambda: fallback_guide(err))
except Exception as e:
logging.error(f"shutdown /fw 例外：{e}")
if not retry:
time.sleep(1)
_attempt(retry=True)
else:
root.after(0, lambda: fallback_guide(str(e)))

    threading.Thread(target=_attempt, daemon=True).start()
    
# ══════════════════════════════════════════════

# Secure Boot 引導視窗

# ══════════════════════════════════════════════

def guide_disable_secure_boot():
logging.info("顯示 Secure Boot 引導視窗")
guide = tk.Toplevel(root)
guide.withdraw()
guide.title("需要關閉 Secure Boot")
guide.resizable(False, False)
guide.configure(bg=BG)
guide.grab_set()

    tk.Frame(guide, bg=RED, height=4).pack(fill="x")
    make_label(guide, "🔒  需要關閉 Secure Boot", size=12, bold=True, color=RED).pack(pady=(14, 2))
    make_label(guide, "啟用 Test Mode 前，必須先在 BIOS 中關閉 Secure Boot",
               size=9, color=TEXT_SEC).pack()
    
    steps_card = make_card(guide)
    steps_card.pack(fill="x", padx=24, pady=10)
    
    for num, desc in [
        ("1", "點擊下方按鈕，電腦將重開並自動進入 BIOS"),
        ("2", "在 BIOS 中找到「Secure Boot」→ 設為 Disabled"),
        ("3", "按 F10 儲存並離開 BIOS"),
        ("4", "重開後再次執行本程式，開啟 Test Mode"),
    ]:
        row = tk.Frame(steps_card, bg=CARD_BG)
        row.pack(fill="x", padx=14, pady=3)
        make_label(row, num, size=10, bold=True, color=BLUE).pack(side="left", padx=(0, 10))
        make_label(row, desc, size=10, color=TEXT_PRI).pack(side="left")
    
    btn_area = tk.Frame(guide, bg=BG)
    btn_area.pack(pady=10)
    
    def do_reboot():
        guide.destroy()
        logging.info("使用者確認：重開機進入 BIOS")
        reboot_to_uefi()
    
    make_btn(btn_area, "🔁  重開機到 BIOS", do_reboot, color=RED, width=18).pack(side="left", padx=8)
    cancel_btn = make_btn(btn_area, "取消", guide.destroy, color=BORDER, width=8)
    cancel_btn.config(fg=TEXT_PRI)
    cancel_btn.pack(side="left", padx=8)
    
    _center_window(guide, 520, 350)
    guide.deiconify()
    
# ══════════════════════════════════════════════

# Fallback 手動引導

# ══════════════════════════════════════════════

def fallback_guide(reason: str = ""):
logging.warning(f"顯示手動 BIOS 引導視窗，原因：{reason}")
win = tk.Toplevel(root)
win.withdraw()
win.title("請手動進入 BIOS")
win.resizable(False, False)
win.configure(bg=BG)
win.grab_set()

    tk.Frame(win, bg=YELLOW, height=4).pack(fill="x")
    make_label(win, "⚠️  無法自動進入 BIOS", size=12, bold=True, color=YELLOW).pack(pady=(14, 2))
    if reason:
        make_label(win, f"原因：{reason}", size=9, color=TEXT_SEC, wraplength=460).pack()
    
    steps_card = make_card(win)
    steps_card.pack(fill="x", padx=24, pady=10)
    
    for num, desc in [
        ("1", "手動重新啟動電腦"),
        ("2", "開機時連續按下對應 BIOS 快捷鍵"),
        ("3", "找到「Secure Boot」→ 設為 Disabled"),
        ("4", "按 F10 儲存並離開"),
        ("5", "重開後再次執行本程式"),
    ]:
        row = tk.Frame(steps_card, bg=CARD_BG)
        row.pack(fill="x", padx=14, pady=3)
        make_label(row, num, size=10, bold=True, color=YELLOW).pack(side="left", padx=(0, 10))
        make_label(row, desc, size=10, color=TEXT_PRI).pack(side="left")
    
    key_card = make_card(win)
    key_card.pack(fill="x", padx=24, pady=(0, 10))
    make_label(key_card, "常見 BIOS 快捷鍵", size=9, bold=True, color=TEXT_SEC).pack(
        anchor="w", padx=14, pady=(8, 4))
    
    keys_frame = tk.Frame(key_card, bg=CARD_BG)
    keys_frame.pack(padx=14, pady=(0, 10))
    
    for i, (brand, key) in enumerate([
        ("ASUS", "Del/F2"), ("MSI", "Del"),
        ("Gigabyte", "Del/F2"), ("ASRock", "F2/Del"),
        ("HP", "F10/Esc"), ("Dell", "F2/F12"),
        ("Lenovo", "F1/F2"), ("Acer", "F2/Del"),
    ]):
        cell = tk.Frame(keys_frame, bg=BORDER, padx=6, pady=3)
        cell.grid(row=i // 4, column=i % 4, padx=3, pady=2)
        make_label(cell, brand, size=9, bold=True, color=TEXT_PRI).pack()
        make_label(cell, key, size=8, color=TEXT_SEC).pack()
    
    close_btn = make_btn(win, "關閉", win.destroy, color=BORDER, width=10)
    close_btn.config(fg=TEXT_PRI)
    close_btn.pack(pady=6)
    
    _center_window(win, 500, 430)
    win.deiconify()
    
# ══════════════════════════════════════════════

# 主視窗

# ══════════════════════════════════════════════

def build_gui(log_file: Path):
global root
global sb_icon_lbl, sb_text_lbl, sb_hint_lbl, sb_bar
global tm_icon_lbl, tm_text_lbl, tm_bar, tm_warn_lbl
global toggle_btn, bios_btn, refresh_btn
global last_update_lbl

    root = tk.Tk()
    root.withdraw()
    root.title(f"Windows 開機設定工具  {VERSION}")
    root.resizable(False, False)
    root.configure(bg=BG)
    
    tk.Frame(root, bg=ACCENT, height=4).pack(fill="x")
    
    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=24, pady=(14, 0))
    make_label(header, "Windows 開機設定工具", size=13, bold=True).pack(side="left")
    make_label(header, "Boot Configuration", size=9, color=TEXT_SEC).pack(
        side="left", padx=(8, 0), pady=(3, 0))
    make_label(header, VERSION, size=8, color=TEXT_SEC).pack(side="right")
    
    sb_icon_lbl, sb_text_lbl, sb_hint_lbl, sb_bar = build_secure_boot_card(root)
    tm_icon_lbl, tm_text_lbl, tm_bar, tm_warn_lbl = build_test_mode_card(root)
    
    toggle_btn, bios_btn, refresh_btn = build_action_area(root)
    
    build_footer(root, log_file)
    
    _center_window(root, 580, 420)
    root.deiconify()
    
    threading.Thread(target=refresh_status, daemon=True).start()
    
    root.protocol("WM_DELETE_WINDOW", lambda: (logging.info("程式關閉"), root.destroy()))
    root.mainloop()
    
# ══════════════════════════════════════════════

# 入口

# ══════════════════════════════════════════════

if __name__ == "__main__":
log_file = init_logger()
require_admin()
build_gui(log_file)
自由軟體 readme

以下是為這個工具撰寫的完整 **README.md**，採用 MIT 授權（自由軟體最常見的寬鬆授權）：

***

```markdown
# 🛠️ Windows 開機設定工具
**Windows Boot Configuration Tool** `v1.0`

> 一鍵查詢並切換 Secure Boot 狀態與 Windows Test Mode（測試模式）的圖形化工具。

![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Admin](https://img.shields.io/badge/Required-Administrator-red)

---

## 📋 功能特色

- 🔒 **Secure Boot 狀態查詢** — 即時偵測 UEFI Secure Boot 是否啟用
- 🧪 **Test Mode 一鍵切換** — 透過 `bcdedit` 開啟／關閉 Windows 測試模式
- ⚙️ **BIOS 快速進入** — 使用 `shutdown /fw` 重開機直接進入 UEFI 設定介面
- 🪟 **手動 BIOS 引導** — 無法自動進入時，提供各品牌主機板快捷鍵一覽
- 📂 **LOG 自動記錄** — 所有操作記錄於 `LOGS/` 資料夾，方便除錯追蹤
- 🎨 **深色主題 UI** — 採用 Catppuccin Mocha 配色，介面簡潔清晰

---

## 🖥️ 系統需求

| 項目 | 需求 |
|------|------|
| 作業系統 | Windows 10 / 11 |
| Python 版本 | 3.8 或以上 |
| 執行權限 | **系統管理員（Administrator）** |
| 相依套件 | 僅使用 Python 標準函式庫（tkinter、subprocess、ctypes） |

---

## 🚀 安裝與執行

### 方法一：直接執行 Python 腳本

```bash
# 1. Clone 或下載本專案
git clone https://github.com/your-username/windows-boot-tool.git
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

> ⚠️ 本工具需要 **管理員權限**。若以一般使用者身分執行，程式會自動觸發 UAC 提升請求。

---

## 📖 使用說明

### 1. 查詢狀態

程式啟動後會自動查詢目前的 **Secure Boot** 與 **Test Mode** 狀態，並以色條指示：


| 顏色 | 意義 |
| :-- | :-- |
| 🟢 綠色 | Secure Boot 已關閉 ／ Test Mode 已開啟 |
| 🔴 紅色 | Secure Boot 已開啟（需進 BIOS 關閉才能開 Test Mode） |
| ⬜ 灰色 | 無法判斷（通常為 Legacy BIOS 環境） |

### 2. 開啟 Test Mode

1. 確認 Secure Boot 已關閉（狀態列顯示綠色）
2. 點擊「**開啟 Test Mode**」按鈕
3. 依提示重新啟動電腦

> 啟用後桌面右下角會出現「Test Mode」浮水印，這是正常現象。

### 3. 進入 BIOS 關閉 Secure Boot

1. 點擊「**⚙️ 進入 BIOS**」按鈕
2. 電腦將在 3 秒後重開並自動進入 UEFI BIOS
3. 找到 `Secure Boot` 選項 → 設為 `Disabled`
4. 按 `F10` 儲存並離開
5. 重開機後再次執行本工具

---

## 📁 專案結構

```
windows-boot-tool/
├── boot_tool.py        # 主程式
├── LOGS/               # 自動產生的操作記錄（.log）
└── README.md
```


---

## ⚠️ 注意事項

- 切換 Test Mode 後**必須重新啟動**電腦才會生效
- 在 Secure Boot 啟用的狀態下，無法開啟 Test Mode
- 本工具僅修改 BCD（開機設定資料）中的 `testsigning` 項目，不會變更任何系統檔案
- 建議在了解用途後再行操作，如有疑慮請先備份 BCD：

```cmd
bcdedit /export C:\bcd_backup
```


---

## 📜 授權條款（License）

```
MIT License

Copyright (c) 2025 [Your Name]

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

## 🤝 貢獻方式

歡迎提交 Issue 或 Pull Request！

1. Fork 本專案
2. 建立你的功能分支：`git checkout -b feature/your-feature`
3. 提交變更：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 開啟 Pull Request

---

## 🙋 常見問題

**Q: 為什麼需要管理員權限？**
A: `bcdedit` 屬於系統層級指令，修改開機設定必須有管理員身分。

**Q: 關閉 Test Mode 後浮水印還在？**
A: 需要重新啟動電腦才會移除。

**Q: `shutdown /fw` 無法自動進入 BIOS？**
A: 部分較舊主機板不支援此指令，程式會自動顯示手動引導視窗，提供各品牌 BIOS 快捷鍵。

**Q: Legacy BIOS 能使用嗎？**
A: Secure Boot 為 UEFI 專屬功能，Legacy BIOS 環境下此項目會顯示「無法判斷」，但 Test Mode 切換功能仍可正常使用。

```

***

### 幾點補充說明

- **授權選擇**：MIT 是最適合個人工具專案的自由軟體授權，允許任何人自由使用、修改、再散布，包含商業用途，限制最少。若你希望衍生作品也必須開源，可改用 **GPL-3.0**。
- **Badges**：`README` 頂部的 shields.io 徽章可以換成你的實際 GitHub repo 路徑，會自動顯示 build 狀態、stars 等資訊。
- **PyInstaller 打包**：加入 `--uac-admin` 參數可讓打包後的 `.exe` 在執行時自動要求管理員權限，不需要程式內部再手動觸發 UAC。```

