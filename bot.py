import customtkinter as ctk
import threading
import time
import pyautogui
import keyboard
import json
import os
from tkinter import messagebox
import tkinter as tk

# ─── Tema Ayarları ───────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SAVE_FILE = "timers.json"

# ─── Renk Paleti ─────────────────────────────────────────────────────────────
BG_DARK      = "#0d0f1a"
BG_CARD      = "#131626"
BG_CARD2     = "#1a1e35"
ACCENT       = "#5865f2"
ACCENT_HOVER = "#4752c4"
ACCENT2      = "#eb459e"
SUCCESS      = "#23d18b"
DANGER       = "#ed4245"
TEXT         = "#e8eaf6"
TEXT_MUTED   = "#7b7f9e"
BORDER       = "#2a2d4a"


# ─── Timer Satırı Widget ──────────────────────────────────────────────────────
class TimerRow(ctk.CTkFrame):
    def __init__(self, master, index, on_delete, **kwargs):
        super().__init__(master, fg_color=BG_CARD2, corner_radius=12, **kwargs)
        self.index     = index
        self.on_delete = on_delete
        self.running   = False
        self.thread    = None
        self.enabled   = True
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=0)  # numara
        self.columnconfigure(1, weight=1)  # mesaj
        self.columnconfigure(2, weight=0)  # dk
        self.columnconfigure(3, weight=0)  # sn
        self.columnconfigure(4, weight=0)  # toggle
        self.columnconfigure(5, weight=0)  # durum
        self.columnconfigure(6, weight=0)  # sil

        # ── Numara ──
        self.num_label = ctk.CTkLabel(
            self, text=f"#{self.index + 1}",
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            text_color=ACCENT, width=35
        )
        self.num_label.grid(row=0, column=0, padx=(12, 6), pady=12)

        # ── Mesaj ──
        self.msg_entry = ctk.CTkEntry(
            self, placeholder_text="Albion'da yazılacak mesaj...",
            font=ctk.CTkFont("Segoe UI", 13),
            fg_color="#0d0f1a", border_color=BORDER,
            text_color=TEXT, placeholder_text_color=TEXT_MUTED,
            height=38
        )
        self.msg_entry.grid(row=0, column=1, padx=6, pady=12, sticky="ew")

        # ── Dakika ──
        self.min_label = ctk.CTkLabel(self, text="dk:", text_color=TEXT_MUTED,
                                      font=ctk.CTkFont("Segoe UI", 12))
        self.min_label.grid(row=0, column=2, padx=(6, 2))
        self.min_var = ctk.StringVar(value="0")
        self.min_spin = ctk.CTkEntry(
            self, textvariable=self.min_var, width=55,
            font=ctk.CTkFont("Segoe UI", 13),
            fg_color="#0d0f1a", border_color=BORDER,
            text_color=TEXT, justify="center", height=38
        )
        self.min_spin.grid(row=0, column=2, padx=(30, 4), pady=12)

        # ── Saniye ──
        self.sec_label = ctk.CTkLabel(self, text="sn:", text_color=TEXT_MUTED,
                                      font=ctk.CTkFont("Segoe UI", 12))
        self.sec_label.grid(row=0, column=3, padx=(2, 2))
        self.sec_var = ctk.StringVar(value="30")
        self.sec_spin = ctk.CTkEntry(
            self, textvariable=self.sec_var, width=55,
            font=ctk.CTkFont("Segoe UI", 13),
            fg_color="#0d0f1a", border_color=BORDER,
            text_color=TEXT, justify="center", height=38
        )
        self.sec_spin.grid(row=0, column=3, padx=(30, 8), pady=12)

        # ── Aktif Toggle ──
        self.toggle_var = ctk.BooleanVar(value=True)
        self.toggle = ctk.CTkSwitch(
            self, text="", variable=self.toggle_var,
            onvalue=True, offvalue=False,
            button_color=SUCCESS, button_hover_color="#1aab6d",
            progress_color=SUCCESS, width=44, height=24
        )
        self.toggle.grid(row=0, column=4, padx=8)

        # ── Durum ──
        self.status_label = ctk.CTkLabel(
            self, text="⏸ Bekliyor", width=90,
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_MUTED
        )
        self.status_label.grid(row=0, column=5, padx=6)

        # ── Sil ──
        self.del_btn = ctk.CTkButton(
            self, text="✕", width=34, height=34,
            fg_color=DANGER, hover_color="#b83232",
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            corner_radius=8,
            command=self._delete
        )
        self.del_btn.grid(row=0, column=6, padx=(4, 12), pady=12)

    def _delete(self):
        self.stop()
        self.on_delete(self)

    def get_interval(self):
        try:
            mins = int(self.min_var.get())
        except ValueError:
            mins = 0
        try:
            secs = int(self.sec_var.get())
        except ValueError:
            secs = 30
        total = mins * 60 + secs
        return max(total, 1)

    def get_message(self):
        return self.msg_entry.get().strip()

    def set_status(self, text, color=TEXT_MUTED):
        self.status_label.configure(text=text, text_color=color)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            if not self.toggle_var.get():
                self.set_status("⏸ Devre dışı", TEXT_MUTED)
                time.sleep(1)
                continue

            msg = self.get_message()
            if not msg:
                self.set_status("⚠ Mesaj yok", "#f0a500")
                time.sleep(1)
                continue

            interval = self.get_interval()
            # Geri sayım
            for remaining in range(interval, 0, -1):
                if not self.running or not self.toggle_var.get():
                    break
                mins, secs = divmod(remaining, 60)
                self.set_status(f"⏱ {mins:02d}:{secs:02d}", ACCENT)
                time.sleep(1)

            if not self.running:
                break

            if self.toggle_var.get():
                msg = self.get_message()
                if msg:
                    self.set_status("✉ Gönderiliyor...", ACCENT2)
                    self._send_message(msg)
                    time.sleep(0.5)

        self.set_status("⏹ Durduruldu", TEXT_MUTED)

    def _send_message(self, msg):
        try:
            # Enter'a bas (chat açmak için), mesajı yaz, Enter'a bas
            keyboard.press_and_release("enter")
            time.sleep(0.3)
            pyautogui.typewrite(msg, interval=0.03)
            time.sleep(0.1)
            keyboard.press_and_release("enter")
        except Exception as e:
            print(f"Mesaj gönderilemedi: {e}")

    def to_dict(self):
        return {
            "message":  self.msg_entry.get(),
            "minutes":  self.min_var.get(),
            "seconds":  self.sec_var.get(),
            "enabled":  self.toggle_var.get(),
        }

    def from_dict(self, data):
        self.msg_entry.delete(0, "end")
        self.msg_entry.insert(0, data.get("message", ""))
        self.min_var.set(data.get("minutes", "0"))
        self.sec_var.set(data.get("seconds", "30"))
        self.toggle_var.set(data.get("enabled", True))


# ─── Ana Uygulama ─────────────────────────────────────────────────────────────
class AlbionBot(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Albion Recruit Bot")
        self.geometry("900x680")
        self.minsize(820, 500)
        self.configure(fg_color=BG_DARK)
        self.resizable(True, True)

        self.rows: list[TimerRow] = []
        self.bot_running = False

        self._build_ui()
        self._load_timers()
        self._bind_hotkeys()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── UI İnşası ────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header ──
        header = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=24, pady=10)

        ctk.CTkLabel(
            title_frame, text="⚔  Albion Recruit Bot",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color=TEXT
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame, text="  v1.0",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=TEXT_MUTED
        ).pack(side="left", padx=(4, 0), pady=(6, 0))

        # Hotkey bilgisi
        ctk.CTkLabel(
            header, text="F9: Başlat/Durdur   F10: Hepsini Durdur",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_MUTED
        ).pack(side="right", padx=24)

        # ── Toolbar ──
        toolbar = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=56)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)

        self.start_btn = ctk.CTkButton(
            toolbar, text="▶  BAŞLAT", width=130, height=38,
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            fg_color=SUCCESS, hover_color="#1aab6d",
            corner_radius=10, command=self._toggle_bot
        )
        self.start_btn.pack(side="left", padx=(16, 8), pady=9)

        ctk.CTkButton(
            toolbar, text="＋  Timer Ekle", width=130, height=38,
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            corner_radius=10, command=self._add_row
        ).pack(side="left", padx=4, pady=9)

        ctk.CTkButton(
            toolbar, text="💾  Kaydet", width=110, height=38,
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=BG_CARD2, hover_color=BORDER,
            corner_radius=10, command=self._save_timers
        ).pack(side="left", padx=4, pady=9)

        ctk.CTkButton(
            toolbar, text="🗑  Hepsini Sil", width=120, height=38,
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=DANGER, hover_color="#b83232",
            corner_radius=10, command=self._clear_all
        ).pack(side="right", padx=16, pady=9)

        # ── İnfo Bandı ──
        info = ctk.CTkFrame(self, fg_color="#0f1525", corner_radius=0, height=38)
        info.pack(fill="x")
        info.pack_propagate(False)
        ctk.CTkLabel(
            info,
            text="ℹ  Albion Online'ı açın, pencereye odaklanın, sonra botu başlatın. Bot Enter'a basarak chat'e yazar.",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_MUTED
        ).pack(side="left", padx=20, pady=8)

        # ── Scroll Alan ──
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color=BG_DARK, scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT
        )
        self.scroll.pack(fill="both", expand=True, padx=16, pady=(12, 4))
        self.scroll.columnconfigure(0, weight=1)

        # ── Status Bar ──
        statusbar = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=32)
        statusbar.pack(fill="x", side="bottom")
        statusbar.pack_propagate(False)
        self.status_bar = ctk.CTkLabel(
            statusbar, text="● Bot durdu",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_MUTED
        )
        self.status_bar.pack(side="left", padx=16)

        self.row_count_label = ctk.CTkLabel(
            statusbar, text="Timer: 0",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_MUTED
        )
        self.row_count_label.pack(side="right", padx=16)

    # ── Timer Satırı Ekle ─────────────────────────────────────────────────────
    def _add_row(self, data=None):
        row = TimerRow(self.scroll, index=len(self.rows), on_delete=self._delete_row)
        row.grid(row=len(self.rows), column=0, sticky="ew", pady=(0, 8), padx=4)
        self.rows.append(row)

        if data:
            row.from_dict(data)

        if self.bot_running:
            row.start()

        self._update_count()

    def _delete_row(self, row: TimerRow):
        row.stop()
        row.grid_forget()
        row.destroy()
        self.rows.remove(row)
        self._reindex()
        self._update_count()

    def _reindex(self):
        for i, row in enumerate(self.rows):
            row.index = i
            row.num_label.configure(text=f"#{i + 1}")
            row.grid(row=i, column=0)

    def _clear_all(self):
        if messagebox.askyesno("Onayla", "Tüm timer'lar silinsin mi?"):
            for row in self.rows[:]:
                row.stop()
                row.grid_forget()
                row.destroy()
            self.rows.clear()
            self._update_count()

    # ── Bot Başlat / Durdur ───────────────────────────────────────────────────
    def _toggle_bot(self):
        if self.bot_running:
            self._stop_bot()
        else:
            self._start_bot()

    def _start_bot(self):
        if not self.rows:
            messagebox.showwarning("Uyarı", "Önce en az bir timer ekleyin!")
            return
        self.bot_running = True
        self.start_btn.configure(text="⏹  DURDUR", fg_color=DANGER, hover_color="#b83232")
        self.status_bar.configure(text="● Bot çalışıyor", text_color=SUCCESS)
        for row in self.rows:
            row.start()

    def _stop_bot(self):
        self.bot_running = False
        self.start_btn.configure(text="▶  BAŞLAT", fg_color=SUCCESS, hover_color="#1aab6d")
        self.status_bar.configure(text="● Bot durdu", text_color=TEXT_MUTED)
        for row in self.rows:
            row.stop()

    # ── Hotkey ───────────────────────────────────────────────────────────────
    def _bind_hotkeys(self):
        keyboard.add_hotkey("f9", self._toggle_bot)
        keyboard.add_hotkey("f10", self._stop_bot)

    # ── Kaydet / Yükle ────────────────────────────────────────────────────────
    def _save_timers(self):
        data = [r.to_dict() for r in self.rows]
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.status_bar.configure(text=f"✔ {len(data)} timer kaydedildi", text_color=SUCCESS)
        self.after(3000, lambda: self.status_bar.configure(
            text="● Bot durdu" if not self.bot_running else "● Bot çalışıyor",
            text_color=TEXT_MUTED if not self.bot_running else SUCCESS
        ))

    def _load_timers(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    self._add_row(data=item)
            except Exception:
                pass
        if not self.rows:
            self._add_row()

    def _update_count(self):
        self.row_count_label.configure(text=f"Timer: {len(self.rows)}")

    def _on_close(self):
        self._stop_bot()
        self._save_timers()
        keyboard.unhook_all()
        self.destroy()


# ─── Giriş Noktası ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = AlbionBot()
    app.mainloop()
