import tkinter as tk
from tkinter import messagebox
import subprocess
import ctypes
import sys
import time
import logging
import threading
from datetime import datetime
from pathlib import Path


# 色彩主題
BG       = "#1e1e2e"
CARD_BG  = "#2a2a3e"
BORDER   = "#3a3a5c"
TEXT_PRI = "#cdd6f4"
TEXT_SEC = "#6c7086"
GREEN    = "#a6e3a1"
YELLOW   = "#f9e2af"
BTN_FG   = "#1e1e2e"
ACCENT   = "#89dceb"

FONT    = "微軟正黑體"
VERSION = "v1.0"


# ============ LOG ============
def init_logger():
    base_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
    log_dir  = base_dir / "LOGS"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"go_bios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  [%(levelname)s]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(log_file, encoding="utf-8")]
    )
    logging.info("═" * 50)
    logging.info("Go_BIOS 程式啟動")
    logging.info(f"Log 路徑：{log_file}")
    logging.info("═" * 50)
    return log_file


# ============ 管理員權限 ============
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
                "無法自動取得管理員權限。\n請右鍵 → 以系統管理員身分執行。"
            )
        sys.exit(0)
    logging.info("管理員權限確認 OK")


# ============ 視窗置中 ============
def _center_window(win, w=None, h=None):
    win.update_idletasks()
    w = w or win.winfo_reqwidth()
    h = h or win.winfo_reqheight()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x  = (sw - w) // 2
    y  = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


# ============ UI 工具 ============
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


def make_btn(parent, text, command, color=ACCENT, width=16):
    return tk.Button(
        parent,
        text=text,
        font=(FONT, 11, "bold"),
        bg=color,
        fg=BTN_FG,
        activebackground=color,
        activeforeground=BTN_FG,
        relief="flat",
        bd=0,
        padx=12,
        pady=8,
        width=width,
        cursor="hand2",
        command=command
    )


def make_card(parent, **kwargs):
    return tk.Frame(
        parent,
        bg=CARD_BG,
        highlightbackground=BORDER,
        highlightthickness=1,
        **kwargs
    )


# ============ Fallback 手動引導 ============
def fallback_guide(reason: str = ""):
    logging.warning(f"顯示手動 BIOS 引導視窗，原因：{reason}")
    win = tk.Toplevel(root)
    win.withdraw()
    win.title("請手動進入 BIOS")
    win.resizable(False, False)
    win.configure(bg=BG)
    win.grab_set()

    tk.Frame(win, bg=YELLOW, height=4).pack(fill="x")
    make_label(win, "⚠️  無法自動進入 UEFI", size=12, bold=True, color=YELLOW).pack(pady=(14, 2))
    if reason:
        make_label(win, f"原因：{reason}", size=9, color=TEXT_SEC, wraplength=460).pack()

    steps_card = make_card(win)
    steps_card.pack(fill="x", padx=24, pady=10)

    for num, desc in [
        ("1", "手動重新啟動電腦"),
        ("2", "開機時連續按下對應 BIOS 快捷鍵"),
        ("3", "找到「Secure Boot」→ 設為 Disabled（如有需要）"),
        ("4", "按 F10 儲存並離開"),
    ]:
        row = tk.Frame(steps_card, bg=CARD_BG)
        row.pack(fill="x", padx=14, pady=3)
        make_label(row, num, size=10, bold=True, color=YELLOW).pack(side="left", padx=(0, 10))
        make_label(row, desc, size=10, color=TEXT_PRI).pack(side="left")

    key_card = make_card(win)
    key_card.pack(fill="x", padx=24, pady=(0, 10))
    make_label(key_card, "常見 BIOS 快捷鍵", size=9, bold=True, color=TEXT_SEC).pack(
        anchor="w", padx=14, pady=(8, 4)
    )

    keys_frame = tk.Frame(key_card, bg=CARD_BG)
    keys_frame.pack(padx=14, pady=(0, 10))

    for i, (brand, key) in enumerate([
        ("ASUS", "Del / F2"), ("MSI", "Del"),
        ("Gigabyte", "Del / F2"), ("ASRock", "F2 / Del"),
        ("HP", "F10 / Esc"), ("Dell", "F2 / F12"),
        ("Lenovo", "F1 / F2"), ("Acer", "F2 / Del"),
    ]):
        cell = tk.Frame(keys_frame, bg=BORDER, padx=6, pady=3)
        cell.grid(row=i // 4, column=i % 4, padx=3, pady=2)
        make_label(cell, brand, size=9, bold=True, color=TEXT_PRI).pack()
        make_label(cell, key, size=8, color=TEXT_SEC).pack()

    close_btn = make_btn(win, "關閉", win.destroy, color=BORDER, width=10)
    close_btn.config(fg=TEXT_PRI)
    close_btn.pack(pady=6)

    _center_window(win)
    win.deiconify()


# ============ 主視窗 ============
def build_gui(log_file: Path):
    global root
    root = tk.Tk()
    root.withdraw()
    root.title(f"Go BIOS 工具  {VERSION}")
    root.resizable(False, False)
    root.configure(bg=BG)

    tk.Frame(root, bg=ACCENT, height=4).pack(fill="x")

    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=24, pady=(14, 4))
    make_label(header, "重開機進入 BIOS / UEFI", size=13, bold=True).pack(side="left")
    make_label(header, "Go BIOS Utility", size=9, color=TEXT_SEC).pack(
        side="left", padx=(8, 0), pady=(3, 0)
    )
    make_label(header, VERSION, size=8, color=TEXT_SEC).pack(side="right")

    card = make_card(root)
    card.pack(fill="x", padx=24, pady=(10, 8))

    make_label(card, "說明", size=11, bold=True, color=TEXT_PRI).pack(
        anchor="w", padx=16, pady=(10, 4)
    )
    make_label(
        card,
        "此工具會呼叫系統指令：\n"
        "shutdown /r /fw /t 3\n\n"
        "支援 UEFI 的主機板會在重開機後直接進入 BIOS 設定畫面。\n"
        "若主機板或系統不支援 /fw，將顯示手動進入 BIOS 的引導。",
        size=9, color=TEXT_SEC, justify="left", anchor="w", wraplength=480
    ).pack(anchor="w", padx=16, pady=(0, 12))

    btn_area = tk.Frame(root, bg=BG)
    btn_area.pack(pady=(4, 4))

    # ── go_btn 透過 closure 讓 reboot_to_uefi 存取 ──
    go_btn = None

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
                    logging.warning(f"第 1 次失敗，retry：{(result.stderr or result.stdout).strip()}")
                    time.sleep(1)
                    _attempt(retry=True)
                else:
                    err = (result.stderr or result.stdout).strip()
                    logging.error(f"shutdown /fw 第 2 次仍失敗：{err}")
                    root.after(0, lambda: _on_fail(err))
            except Exception as e:
                logging.error(f"shutdown /fw 例外：{e}")
                if not retry:
                    time.sleep(1)
                    _attempt(retry=True)
                else:
                    root.after(0, lambda: _on_fail(str(e)))

        def _on_fail(reason: str):
            go_btn.config(state="normal", text="🔁  重開機到 UEFI / BIOS")
            fallback_guide(reason)

        logging.info("使用者按下按鈕：重開機進入 UEFI")
        go_btn.config(state="disabled", text="⏳ 指令已送出，3 秒後重開機...")
        threading.Thread(target=_attempt, daemon=True).start()

    go_btn = make_btn(btn_area, "🔁  重開機到 UEFI / BIOS", reboot_to_uefi, color=GREEN, width=24)
    go_btn.pack()

    footer = tk.Frame(root, bg=BG)
    footer.pack(fill="x", padx=24, pady=(10, 8))
    make_label(footer, "⚠️  重開機前請先儲存所有未儲存的工作內容", size=9, color=TEXT_SEC).pack(
        side="left"
    )
    make_label(footer, f"📄 {log_file.name}", size=8, color=TEXT_SEC).pack(side="right")

    _center_window(root, 560, 320)
    root.deiconify()

    root.protocol("WM_DELETE_WINDOW", lambda: (logging.info("程式關閉"), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    log_file = init_logger()
    require_admin()
    build_gui(log_file)
