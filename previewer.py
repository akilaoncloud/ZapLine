from tkinter import filedialog
from PIL import Image, ImageTk, UnidentifiedImageError  # pip install pillow

from settings import *

def insertImage(GUI):
    try:
        GUI.path = filedialog.askopenfile(filetypes=[(INSERT_IMAGE, IMAGE_TYPES)]).name

        file = Image.open(GUI.path)

        image_ratio = file.size[0] / file.size[1]
        canvas_ratio = GUI.canvas_w / GUI.canvas_h

        if canvas_ratio > image_ratio:  # Image is wider than the canvas
            image_h = int(GUI.canvas_h)
            image_w = int(image_h * image_ratio)
        else:  # Image is taller than canvas
            image_w = int(GUI.canvas_w)
            image_h = int(image_w / image_ratio)

        resized_image = file.resize((image_w, image_h))

        GUI.canvas_image = ImageTk.PhotoImage(resized_image)

        GUI.canvas.delete("all")  # Deletes the text, and adds an image
        GUI.canvas.create_image(GUI.canvas_w / 2, GUI.canvas_h / 2, image=GUI.canvas_image)

        GUI.type = 1  # image/video format
        GUI.checkAttachment()

    except AttributeError:
        return None

    except UnidentifiedImageError:
        GUI.issueHandler(FILE_IMAGE_ERROR)

def insertVideo(GUI):
    try:
        GUI.path = filedialog.askopenfile(filetypes=[(INSERT_VIDEO, VIDEO_TYPES)]).name

        GUI.canvas.delete("all")

        # Ícone único
        GUI.canvas.create_text(
            GUI.canvas_w / 2, GUI.canvas_h / 2 - 20,
            text="▶️",
            font=("Segoe UI Emoji", 48)
        )

        # Path do arquivo
        GUI.canvas.create_text(
            GUI.canvas_w / 2, GUI.canvas_h / 2 + 50,
            anchor='n',
            text=GUI.path,
            width=GUI.canvas_w - 25,
            font=("Segoe UI", 9),
            fill="#888"
        )

        GUI.type = 1  # image/video format
        GUI.checkAttachment()

    except AttributeError:
        return None

def insertAudio(GUI):
    try:
        GUI.path = filedialog.askopenfile(filetypes=[(INSERT_AUDIO, AUDIO_TYPES)]).name

        GUI.canvas.delete("all")

        # Ícone único
        GUI.canvas.create_text(
            GUI.canvas_w / 2, GUI.canvas_h / 2 - 20,
            text="🎵",
            font=("Segoe UI Emoji", 48)
        )

        # Path do arquivo
        GUI.canvas.create_text(
            GUI.canvas_w / 2, GUI.canvas_h / 2 + 50,
            anchor='n',
            text=GUI.path,
            width=GUI.canvas_w - 25,
            font=("Segoe UI", 9),
            fill="#888"
        )

        GUI.type = 2  # audio format
        GUI.checkAttachment()

    except AttributeError:
        return None

def insertFile(GUI):
    try:
        GUI.path = filedialog.askopenfile().name

        GUI.canvas.delete("all")

        # Ícone único
        GUI.canvas.create_text(
            GUI.canvas_w / 2, GUI.canvas_h / 2 - 20,
            text="📄",
            font=("Segoe UI Emoji", 48)
        )

        # Path do arquivo
        GUI.canvas.create_text(
            GUI.canvas_w / 2, GUI.canvas_h / 2 + 50,
            anchor='n',
            text=GUI.path,
            width=GUI.canvas_w - 25,
            font=("Segoe UI", 9),
            fill="#888"
        )

        GUI.type = 3  # file format
        GUI.checkAttachment()

    except AttributeError:
        return None