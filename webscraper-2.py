# -*- coding: utf-8 -*-
"""
Website to PDF Downloader
Prepared by Deepjyoti Das Technologies
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pdfkit
import threading
import os

# ==================================================
# WKHTMLTOPDF CONFIGURATION
# ==================================================

# Your installed path
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

# Check if file exists
if not os.path.exists(WKHTMLTOPDF_PATH):

    message = (
        "wkhtmltopdf.exe not found.\n\n"
        "Check installation path:\n"
        f"{WKHTMLTOPDF_PATH}"
    )

    print(message)

    config = None

else:
    config = pdfkit.configuration(
        wkhtmltopdf=WKHTMLTOPDF_PATH
    )

# ==================================================
# DOWNLOAD FUNCTION
# ==================================================

def generate_pdf():

    url = url_entry.get().strip()

    # Validate URL
    if not url:
        messagebox.showerror(
            "Error",
            "Please enter website URL"
        )
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        messagebox.showerror(
            "Invalid URL",
            "URL must start with:\nhttp:// or https://"
        )
        return

    # Check configuration
    if config is None:
        messagebox.showerror(
            "wkhtmltopdf Missing",
            "wkhtmltopdf not found.\nCheck installation path."
        )
        return

    # Save file dialog
    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save PDF As"
    )

    if not save_path:
        return

    # Start background thread
    threading.Thread(
        target=download_task,
        args=(url, save_path),
        daemon=True
    ).start()

# ==================================================
# BACKGROUND TASK
# ==================================================

def download_task(url, save_path):

    try:

        update_status("Generating PDF...", "blue")
        disable_button()

        options = {
            "page-size": "A4",
            "encoding": "UTF-8",
            "margin-top": "10mm",
            "margin-right": "10mm",
            "margin-bottom": "10mm",
            "margin-left": "10mm",
            "enable-local-file-access": ""
        }

        pdfkit.from_url(
            url,
            save_path,
            configuration=config,
            options=options
        )

        update_status(
            "PDF Downloaded Successfully!",
            "green"
        )

        messagebox.showinfo(
            "Success",
            f"PDF saved successfully:\n\n{save_path}"
        )

    except Exception as e:

        update_status("Failed!", "red")

        messagebox.showerror(
            "Download Error",
            str(e)
        )

    finally:
        enable_button()

# ==================================================
# GUI HELPERS
# ==================================================

def update_status(text, color):
    status_label.config(text=text, foreground=color)

def disable_button():
    download_btn.config(state="disabled")

def enable_button():
    download_btn.config(state="normal")

# ==================================================
# GUI
# ==================================================

root = tk.Tk()

root.title("Website to PDF Downloader")
root.geometry("700x350")
root.configure(bg="#f4f4f4")
root.resizable(False, False)

# Title
title = tk.Label(
    root,
    text="Website to PDF Downloader",
    font=("Arial", 22, "bold"),
    bg="#f4f4f4",
    fg="#222"
)

title.pack(pady=20)

# URL Label
url_label = tk.Label(
    root,
    text="Paste Website URL",
    font=("Arial", 12),
    bg="#f4f4f4"
)

url_label.pack()

# URL Entry
url_entry = tk.Entry(
    root,
    width=70,
    font=("Arial", 12),
    relief="solid",
    bd=1
)

url_entry.pack(pady=10, ipady=6)

# Download Button
download_btn = tk.Button(
    root,
    text="Download PDF",
    font=("Arial", 13, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=25,
    pady=10,
    relief="flat",
    command=generate_pdf
)

download_btn.pack(pady=15)

# Status Label
status_label = ttk.Label(
    root,
    text="Ready",
    font=("Arial", 11)
)

status_label.pack(pady=10)

# Footer
footer = tk.Label(
    root,
    text="Prepared by Deepjyoti Das Technologies",
    font=("Arial", 9),
    bg="#f4f4f4",
    fg="gray"
)

footer.pack(side="bottom", pady=10)

# ==================================================
# START APP
# ==================================================

root.mainloop()