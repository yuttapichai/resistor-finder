import tkinter as tk
from tkinter import ttk
import os
import sys

# สำหรับให้ PyInstaller หาไฟล์ ico ได้
def resource_path(relative_path):
    try:
        # เมื่อรันจาก .exe
        base_path = sys._MEIPASS
    except Exception:
        # ตอนรันปกติ
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ข้อมูลค่ามาตรฐาน E-series
E_SERIES = {
    'E6':  [10, 15, 22, 33, 47, 68],
    'E12': [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82],
    'E24': [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30,
            33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91],
    'E96': [
        100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130,
        133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174,
        178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232,
        237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309,
        316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412,
        422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549,
        562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732,
        750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976
    ]
}

DECADES = [1, 10, 100, 1_000, 10_000]

# สร้างตารางค่าตัวต้านทาน
def build_resistor_list(series_name):
    base = E_SERIES[series_name]
    if series_name == 'E96':
        base = [v / 10 for v in base]
    result = sorted(set(round(b * d, 2) for b in base for d in DECADES))
    result.insert(0, 0)
    return result

# หาค่าที่อยู่ระหว่าง
def find_between(value, series):
    for i in range(len(series) - 1):
        if series[i] <= value <= series[i + 1]:
            return series[i], series[i + 1]
    return None, None

# เริ่ม GUI
def launch_gui():
    root = tk.Tk()
    root.title("Resistor Finder")
    root.geometry("360x230")
    root.configure(bg="#f9f9f9")

    # ตั้ง icon
    try:
        icon_path = resource_path("resistor_icon.ico")
        root.iconbitmap(icon_path)
    except:
        pass

    # ฟอนต์และธีม
    font = ("Segoe UI", 10)
    fg_color = "#222222"
    bg_color = "#f9f9f9"
    entry_bg = "#ffffff"

    style = ttk.Style()
    style.theme_use('clam')
    style.configure(".", background=bg_color, foreground=fg_color, font=font)
    style.configure("TButton", background="#dddddd", padding=6)
    style.map("TButton", background=[('active', '#cccccc')])
    style.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color)

    # E-Series dropdown
    ttk.Label(root, text="E-Series:").pack(pady=(10, 2))
    series_var = tk.StringVar(value="E24")
    series_cb = ttk.Combobox(root, textvariable=series_var, values=list(E_SERIES.keys()), state="readonly")
    series_cb.pack()

    # ค่า input
    ttk.Label(root, text="Enter value (Ω):").pack(pady=(12, 2))
    value_entry = ttk.Entry(root, justify="center")
    value_entry.pack()

    # แสดงผลลัพธ์
    result_var = tk.StringVar()
    result_label = ttk.Label(root, textvariable=result_var, foreground="#008800")
    result_label.pack(pady=(14, 0))

    def on_search():
        try:
            val = float(value_entry.get())
            series = build_resistor_list(series_var.get())
            low, high = find_between(val, series)
            if low is not None:
                result_var.set(f"{val} Ω is between {low} and {high} Ω")
            else:
                result_var.set("Out of range.")
        except:
            result_var.set("Invalid input.")

    ttk.Button(root, text="Find", command=on_search).pack(pady=10)
    root.mainloop()

# เรียก GUI
if __name__ == "__main__":
    launch_gui()
