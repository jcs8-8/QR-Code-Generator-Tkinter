"""
Advanced QR Code Generator Application

Enhanced & Designed by J Charitha Shree
"""

# ======================= IMPORTS =======================
from tkinter import *
from tkinter import messagebox
import time
import pyqrcode

# ======================= MAIN CLASS =======================
class QRCodeApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced QR Code Generator | J Charitha Shree")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F172A")  # Dark UI background

        # Variables
        self.qr_data = StringVar()
        self.file_name = StringVar()
        self.status_text = StringVar(value="Ready")

        self.create_ui()

    # ======================= UI SETUP =======================
    def create_ui(self):
        self.create_header()
        self.create_input_section()
        self.create_buttons()
        self.create_qr_display()
        self.create_status_bar()

    def create_header(self):
        header = Frame(self.root, bg="#020617", height=80)
        header.pack(fill=X)

        Label(
            header,
            text="QR Code Generator",
            fg="#E5E7EB",
            bg="#020617",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=10)

        Label(
            header,
            text="Designed by J Charitha Shree",
            fg="#94A3B8",
            bg="#020617",
            font=("Segoe UI", 11)
        ).pack()

    def create_input_section(self):
        input_frame = Frame(self.root, bg="#0F172A", pady=20)
        input_frame.pack(fill=X)

        Label(
            input_frame,
            text="Enter Text / URL",
            fg="#F8FAFC",
            bg="#0F172A",
            font=("Segoe UI", 12, "bold")
        ).grid(row=0, column=0, padx=20, sticky="w")

        Entry(
            input_frame,
            textvariable=self.qr_data,
            width=50,
            font=("Segoe UI", 12)
        ).grid(row=1, column=0, padx=20, pady=8)

        Label(
            input_frame,
            text="File Name (optional)",
            fg="#F8FAFC",
            bg="#0F172A",
            font=("Segoe UI", 12, "bold")
        ).grid(row=2, column=0, padx=20, sticky="w")

        Entry(
            input_frame,
            textvariable=self.file_name,
            width=30,
            font=("Segoe UI", 11)
        ).grid(row=3, column=0, padx=20, pady=5, sticky="w")

    # ======================= BUTTONS =======================
    def create_buttons(self):
        btn_frame = Frame(self.root, bg="#0F172A")
        btn_frame.pack(pady=10)

        Button(
            btn_frame,
            text="Generate QR",
            command=self.generate_qr,
            bg="#1E293B",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=15
        ).grid(row=0, column=0, padx=10)

        Button(
            btn_frame,
            text="Save QR",
            command=self.save_qr,
            bg="#166534",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=15
        ).grid(row=0, column=1, padx=10)

        Button(
            btn_frame,
            text="Clear",
            command=self.clear_all,
            bg="#7F1D1D",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=15
        ).grid(row=0, column=2, padx=10)

    # ======================= QR DISPLAY =======================
    def create_qr_display(self):
        display = Frame(self.root, bg="#020617", height=200)
        display.pack(fill=BOTH, padx=20, pady=10, expand=True)

        self.qr_label = Label(display, bg="#020617")
        self.qr_label.pack(pady=20)

    # ======================= STATUS BAR =======================
    def create_status_bar(self):
        status = Frame(self.root, bg="#020617", height=30)
        status.pack(fill=X, side=BOTTOM)

        Label(
            status,
            textvariable=self.status_text,
            fg="#CBD5E1",
            bg="#020617",
            anchor="w",
            font=("Segoe UI", 10)
        ).pack(fill=X, padx=10)

    # ======================= FUNCTIONALITY =======================
    def generate_qr(self):
        data = self.qr_data.get().strip()

        if not data:
            messagebox.showwarning("Input Error", "Please enter text or URL!")
            self.status_text.set("Error: Empty input")
            return

        self.qr = pyqrcode.create(data)

        # BLACK & WHITE QR CODE
        xbm_data = self.qr.xbm(scale=6)

        self.qr_image = BitmapImage(
            data=xbm_data,
            foreground="black",
            background="white"
        )

        self.qr_label.config(image=self.qr_image)
        self.status_text.set("QR Code generated (Black & White)")

    def save_qr(self):
        if not hasattr(self, 'qr'):
            messagebox.showerror("Error", "Generate QR code first!")
            return

        name = self.file_name.get().strip()
        if not name:
            name = f"qr_{int(time.time())}"

        self.qr.png(f"{name}.png", scale=8)
        self.status_text.set(f"Saved as {name}.png")
        messagebox.showinfo("Saved", f"QR Code saved as {name}.png")

    def clear_all(self):
        self.qr_data.set("")
        self.file_name.set("")
        self.qr_label.config(image="")
        self.status_text.set("Cleared all fields")

# ======================= RUN APP =======================
if __name__ == "__main__":
    root = Tk()
    app = QRCodeApp(root)
    root.mainloop()
