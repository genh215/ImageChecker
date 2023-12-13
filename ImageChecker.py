import numpy as np
import cv2
import os
import tkinter as tk
from tkinter import filedialog, Scale, Label, Button, HORIZONTAL, Frame
from PIL import Image, ImageTk

class SinWaveFilterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Data Checker")
        self.geometry("800x600")

        self.original_image = None
        self.filtered_image = None
        self.preview_image = None
        self.file_path = None

        self.img_frame = Frame(self)
        self.img_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        self.label = Label(self.img_frame)
        self.label.pack(expand=True)

        self.scale = Scale(self, from_=1, to_=16, orient=HORIZONTAL, label="Periods", command=self.update_filter)
        self.scale.pack(padx=10, pady=10, fill=tk.X)

        self.load_button = Button(self, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10, side=tk.LEFT, padx=5)

        self.save_button = Button(self, text="Save Filtered Image", command=self.save_image)
        self.save_button.pack(pady=10, side=tk.LEFT, padx=5)

    def resize_image_to_fit(self, image):
        target_width, target_height = 780, 440  # consider some padding
        h, w, _ = image.shape
        scale = min(target_width / w, target_height / h)
        return cv2.resize(image, (int(w * scale), int(h * scale)))

    def load_image(self):
        self.file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.tiff;*.jpeg;*.jpg;*.png"), ("All files", "*.*")]
        )
        if not self.file_path:
            return

        self.original_image = cv2.imread(self.file_path, cv2.IMREAD_COLOR)
        self.update_filter()

    def save_image(self):
        if self.filtered_image is None or self.file_path is None:
            return

        directory, filename = os.path.split(self.file_path)
        name, ext = os.path.splitext(filename)
        save_path = os.path.join(directory, f"{name}_filtered{ext}")

        cv2.imwrite(save_path, self.filtered_image)

    def update_filter(self, value=None):
        if self.original_image is None:
            return

        periods = self.scale.get()
        resized_image = self.resize_image_to_fit(self.original_image)
        self.filtered_image = apply_filter(self.original_image, periods)

        # Convert to RGB for Tkinter display
        img_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image and then to ImageTk.PhotoImage for displaying in Tkinter
        pil_img = Image.fromarray(apply_filter(img_rgb, periods))
        self.preview_image = ImageTk.PhotoImage(pil_img)

        self.label.config(image=self.preview_image)
        self.label.update()

def apply_filter(img, periods):
    img_normalized = img / 255.0
    img_filtered = np.sin(img_normalized * 2 * np.pi * periods) * 0.5 + 0.5
    return (img_filtered * 255).astype(np.uint8)

if __name__ == "__main__":
    app = SinWaveFilterApp()
    app.mainloop()
