# ======================= IMPORTS =======================
from tkinter import *
from tkinter import messagebox, filedialog, colorchooser
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image, ImageTk
import time
import os
import re

# ======================= MAIN CLASS =======================
class AdvancedQRCodeApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced QR Code Generator | J Charitha Shree")
        self.root.geometry("780x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F172A")

        # Variables
        self.qr_data = StringVar()
        self.file_name = StringVar()
        self.status_text = StringVar(value="Ready")
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.logo_path = None
        self.error_level = StringVar(value="Medium")

        self.create_ui()

    # ======================= UI SETUP =======================
    def create_ui(self):
        self.create_header()
        self.create_input_section()
        self.create_controls()
        self.create_qr_display()
        self.create_status_bar()

    def create_header(self):
        header = Frame(self.root, bg="#020617", height=80)
        header.pack(fill=X)

        Label(header, text="Advanced QR Code Generator",
              fg="white", bg="#020617",
              font=("Segoe UI", 26, "bold")).pack(pady=8)

        Label(header, text="Designed by J Charitha Shree",
              fg="#94A3B8", bg="#020617",
              font=("Segoe UI", 11)).pack()

    def create_input_section(self):
        frame = Frame(self.root, bg="#0F172A", pady=15)
        frame.pack(fill=X)

        Label(frame, text="Enter Text / URL",
              fg="white", bg="#0F172A",
              font=("Segoe UI", 12, "bold")).grid(row=0, column=0, padx=20, sticky="w")

        Entry(frame, textvariable=self.qr_data,
              width=55, font=("Segoe UI", 12)).grid(row=1, column=0, padx=20, pady=6)

        Label(frame, text="File Name",
              fg="white", bg="#0F172A",
              font=("Segoe UI", 12, "bold")).grid(row=2, column=0, padx=20, sticky="w")

        Entry(frame, textvariable=self.file_name,
              width=30, font=("Segoe UI", 11)).grid(row=3, column=0, padx=20, pady=5, sticky="w")

    # ======================= CONTROLS =======================
    def create_controls(self):
        frame = Frame(self.root, bg="#0F172A")
        frame.pack(pady=10)

        Label(frame, text="Error Correction",
              fg="white", bg="#0F172A").grid(row=0, column=0)

        OptionMenu(frame, self.error_level,
                   "Low", "Medium", "Quartile", "High").grid(row=0, column=1)

        Button(frame, text="QR Color",
               command=self.pick_fill_color).grid(row=0, column=2, padx=5)

        Button(frame, text="Background",
               command=self.pick_bg_color).grid(row=0, column=3, padx=5)

        Button(frame, text="Add Logo",
               command=self.load_logo).grid(row=0, column=4, padx=5)

        Button(frame, text="Generate",
               bg="#1E293B", fg="white",
               command=self.generate_qr, width=12).grid(row=0, column=5, padx=10)

        Button(frame, text="Save",
               bg="#166534", fg="white",
               command=self.save_qr, width=10).grid(row=0, column=6, padx=5)

        Button(frame, text="Clear",
               bg="#7F1D1D", fg="white",
               command=self.clear_all, width=10).grid(row=0, column=7, padx=5)

    # ======================= DISPLAY =======================
    def create_qr_display(self):
        frame = Frame(self.root, bg="#020617", width=320, height=320)
        frame.pack(pady=15)
        frame.pack_propagate(False)

        self.qr_label = Label(frame, bg="#020617")
        self.qr_label.pack(expand=True)

    # ======================= STATUS BAR =======================
    def create_status_bar(self):
        status = Frame(self.root, bg="#020617", height=28)
        status.pack(fill=X, side=BOTTOM)

        Label(status, textvariable=self.status_text,
              fg="#CBD5E1", bg="#020617",
              font=("Segoe UI", 10),
              anchor="w").pack(fill=X, padx=10)

    # ======================= LOGIC =======================
    def get_error_level(self):
        return {
            "Low": ERROR_CORRECT_L,
            "Medium": ERROR_CORRECT_M,
            "Quartile": ERROR_CORRECT_Q,
            "High": ERROR_CORRECT_H
        }[self.error_level.get()]

    def generate_qr(self):
        data = self.qr_data.get().strip()
        if not data:
            messagebox.showwarning("Error", "Input cannot be empty")
            return

        qr = qrcode.QRCode(
            version=None,
            error_correction=self.get_error_level(),
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=self.fill_color,
                            back_color=self.back_color).convert("RGB")

        if self.logo_path:
            logo = Image.open(self.logo_path)
            logo = logo.resize((70, 70))
            pos = ((img.size[0] - logo.size[0]) // 2,
                   (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, pos)

        img = img.resize((300, 300))
        self.final_qr = img

        self.qr_image = ImageTk.PhotoImage(img)
        self.qr_label.config(image=self.qr_image)
        self.status_text.set("QR Code Generated Successfully")

    def save_qr(self):
        if not hasattr(self, 'final_qr'):
            messagebox.showerror("Error", "Generate QR first")
            return

        name = self.file_name.get().strip() or f"qr_{int(time.time())}"
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("SVG File", "*.svg")],
            initialfile=name
        )

        if path:
            self.final_qr.save(path)
            self.status_text.set(f"Saved: {os.path.basename(path)}")

    def pick_fill_color(self):
        self.fill_color = colorchooser.askcolor()[1]

    def pick_bg_color(self):
        self.back_color = colorchooser.askcolor()[1]

    def load_logo(self):
        self.logo_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )

    def clear_all(self):
        self.qr_data.set("")
        self.file_name.set("")
        self.qr_label.config(image="")
        self.logo_path = None
        self.status_text.set("Cleared All")

# ======================= RUN =======================
if __name__ == "__main__":
    root = Tk()
    AdvancedQRCodeApp(root)
    root.mainloop()
