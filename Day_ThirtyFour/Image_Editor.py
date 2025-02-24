import cv2
import numpy as np
import torch
import tkinter as tk
from tkinter import filedialog
from rembg import remove
from PIL import Image, ImageTk
import customtkinter as ctk


def remove_background(input_path):
    """Removes background from an image using rembg and returns the output image."""
    with open(input_path, "rb") as f:
        input_image = f.read()
    return remove(input_image)


def advanced_background_remover(input_path, blur=True, sharpen=True, enhance=True):
    """Advanced background remover with additional image enhancements."""
    image = Image.open(input_path)
    image_no_bg = remove(image)
    image_cv = np.array(image_no_bg)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGBA2BGRA)

    if blur:
        image_cv = cv2.GaussianBlur(image_cv, (5, 5), 0)
    if sharpen:
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        image_cv = cv2.filter2D(image_cv, -1, kernel)
    if enhance:
        alpha, beta = 1.2, 10
        image_cv = cv2.convertScaleAbs(image_cv, alpha=alpha, beta=beta)

    return Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGRA2RGBA))


def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        processed_image = advanced_background_remover(file_path)
        processed_image.thumbnail((400, 400))
        img_display = ImageTk.PhotoImage(processed_image)
        img_label.config(image=img_display)
        img_label.image = img_display


def save_file():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
                                             ("PNG files", "*.png"), ("All Files", "*.*")])
    if save_path:
        img_label.image._PhotoImage__photo.write(save_path)


# GUI Setup
ctk.set_appearance_mode("Dark")
app = ctk.CTk()
app.title("Advanced Background Remover")
app.geometry("500x600")

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

img_label = tk.Label(frame)
img_label.pack(pady=10)

btn_open = ctk.CTkButton(app, text="Open Image", command=open_file)
btn_open.pack(pady=10)

btn_save = ctk.CTkButton(app, text="Save Image", command=save_file)
btn_save.pack(pady=10)

app.mainloop()
