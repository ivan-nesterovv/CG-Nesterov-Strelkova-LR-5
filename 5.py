import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Попиксельные преобразования - NetPBM")
        self.root.geometry("1400x700")

        self.source_image = None
        self.second_image = None
        self.processed_image = None
        self.overlay_image = None

        self.source_array = None
        self.second_array = None

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        tk.Button(control_frame, text="Загрузить первое изображение",
                  command=self.load_source_image, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Обесцветить на 50%",
                  command=self.desaturate_50, width=30).pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Загрузить второе изображение",
                  command=self.load_second_image, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Наложить жёсткий свет",
                  command=self.hard_light_overlay, width=30).pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Сохранить преобразованное",
                  command=self.save_processed, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Сохранить наложенное",
                  command=self.save_overlay, width=30).pack(side=tk.LEFT, padx=5)

        images_frame = tk.Frame(main_frame)
        images_frame.pack(fill=tk.BOTH, expand=True)

        for i in range(4):
            images_frame.columnconfigure(i, weight=1, uniform="equal")
        images_frame.rowconfigure(1, weight=1)

        tk.Label(images_frame, text="Первое изображение",
                 font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, sticky="ew")
        source_container = tk.Frame(images_frame, relief=tk.SUNKEN, bd=1)
        source_container.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        source_container.columnconfigure(0, weight=1)
        source_container.rowconfigure(0, weight=1)
        self.source_label = tk.Label(source_container, text="Первое изображение не загружено",
                                     bg='lightgray')
        self.source_label.grid(row=0, column=0, sticky="nsew")

        tk.Label(images_frame, text="Преобразованное изображение",
                 font=("Arial", 12, "bold")).grid(row=0, column=1, pady=5, sticky="ew")
        processed_container = tk.Frame(images_frame, relief=tk.SUNKEN, bd=1)
        processed_container.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        processed_container.columnconfigure(0, weight=1)
        processed_container.rowconfigure(0, weight=1)
        self.processed_label = tk.Label(processed_container, text="Нет преобразованного изображения",
                                        bg='lightgray')
        self.processed_label.grid(row=0, column=0, sticky="nsew")

        tk.Label(images_frame, text="Второе изображение",
                 font=("Arial", 12, "bold")).grid(row=0, column=2, pady=5, sticky="ew")
        second_container = tk.Frame(images_frame, relief=tk.SUNKEN, bd=1)
        second_container.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        second_container.columnconfigure(0, weight=1)
        second_container.rowconfigure(0, weight=1)
        self.second_label = tk.Label(second_container, text="Второе изображение не загружено",
                                     bg='lightgray')
        self.second_label.grid(row=0, column=0, sticky="nsew")

        tk.Label(images_frame, text="Наложенное изображение",
                 font=("Arial", 12, "bold")).grid(row=0, column=3, pady=5, sticky="ew")
        overlay_container = tk.Frame(images_frame, relief=tk.SUNKEN, bd=1)
        overlay_container.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")
        overlay_container.columnconfigure(0, weight=1)
        overlay_container.rowconfigure(0, weight=1)
        self.overlay_label = tk.Label(overlay_container, text="Нет наложенного изображения",
                                      bg='lightgray')
        self.overlay_label.grid(row=0, column=0, sticky="nsew")

        self.root.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        if self.source_image is not None:
            self.display_image(self.source_image, self.source_label)
        if self.processed_image is not None:
            self.display_image(self.processed_image, self.processed_label)
        if self.second_image is not None:
            self.display_image(self.second_image, self.second_label)
        if self.overlay_image is not None:
            self.display_image(self.overlay_image, self.overlay_label)

    def load_source_image(self):
        filename = filedialog.askopenfilename(
            title="Выберите первое изображение",
            filetypes=[("NetPBM files", "*.pbm *.pgm *.ppm"),
                       ("Все файлы", "*.*")]
        )
        if filename:
            try:
                self.source_image = Image.open(filename)
                self.source_array = np.array(self.source_image)
                self.display_image(self.source_image, self.source_label)
                messagebox.showinfo("Успех", f"Первое изображение загружено: {self.source_image.size}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def load_second_image(self):
        filename = filedialog.askopenfilename(
            title="Выберите второе изображение",
            filetypes=[("NetPBM files", "*.pbm *.pgm *.ppm"),
                       ("Все файлы", "*.*")]
        )
        if filename:
            try:
                self.second_image = Image.open(filename)
                self.second_array = np.array(self.second_image)
                self.display_image(self.second_image, self.second_label)
                messagebox.showinfo("Успех", f"Второе изображение загружено: {self.second_image.size}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def desaturate_50(self):
        if self.source_image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите первое изображение")
            return

        try:
            if self.source_image.mode != 'RGB':
                img_rgb = self.source_image.convert('RGB')
                source_array = np.array(img_rgb)
            else:
                source_array = self.source_array.copy()

            gray = np.dot(source_array[..., :3], [0.299, 0.587, 0.114])

            result_array = source_array.copy().astype(np.float32)
            for i in range(3):
                result_array[..., i] = result_array[..., i] * 0.5 + gray * 0.5

            result_array = np.clip(result_array, 0, 255).astype(np.uint8)
            self.processed_image = Image.fromarray(result_array)
            self.display_image(self.processed_image, self.processed_label)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Обесцвечивание 50% не удалось: {str(e)}")

    def hard_light_overlay(self):
        if self.source_image is None or self.second_image is None:
            messagebox.showwarning("Предупреждение", "Пожалуйста, загрузите оба изображения")
            return

        try:
            source_img = self.source_image.convert('RGB')
            second_img = self.second_image.convert('RGB')

            if source_img.size != second_img.size:
                second_img = second_img.resize(source_img.size, Image.Resampling.LANCZOS)
                messagebox.showinfo("Информация", "Второе изображение изменено под размер первого")

            source_array = np.array(source_img, dtype=np.float32) / 255.0
            second_array = np.array(second_img, dtype=np.float32) / 255.0

            # Hard Light blend mode
            result_array = np.zeros_like(source_array)

            for i in range(3):
                mask = second_array[..., i] > 0.5
                result_array[..., i] = np.where(
                    mask,
                    1.0 - (1.0 - source_array[..., i]) * (1.0 - (second_array[..., i] - 0.5) * 2.0),
                    source_array[..., i] * (second_array[..., i] * 2.0)
                )

            result_array = np.clip(result_array * 255, 0, 255).astype(np.uint8)
            self.overlay_image = Image.fromarray(result_array)
            self.display_image(self.overlay_image, self.overlay_label)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Наложение - жёсткий свет не удалось: {str(e)}")

    def display_image(self, image, label):
        container = label.master

        container.update_idletasks()
        container_width = container.winfo_width()
        container_height = container.winfo_height()

        if container_width < 10 or container_height < 10:
            container_width = 300
            container_height = 300

        img_ratio = image.width / image.height
        container_ratio = container_width / container_height

        if img_ratio > container_ratio:
            display_width = container_width - 10
            display_height = int(display_width / img_ratio)
        else:
            display_height = container_height - 10
            display_width = int(display_height * img_ratio)

        display_width = max(display_width, 50)
        display_height = max(display_height, 50)

        display_image = image.resize((display_width, display_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(display_image)
        label.configure(image=photo, text="")
        label.image = photo

    def save_processed(self):
        if self.processed_image is None:
            messagebox.showwarning("Предупреждение", "Нет преобразованного изображения для сохранения")
            return

        filename = filedialog.asksaveasfilename(
            title="Сохранить преобразованное изображение",
            defaultextension=".ppm",
            filetypes=[("PPM files", "*.ppm"),
                       ("PGM files", "*.pgm"),
                       ("PBM files", "*.pbm"),
                       ("Все файлы", "*.*")]
        )
        if filename:
            try:
                self.processed_image.save(filename)
                messagebox.showinfo("Успех", f"Преобразованное изображение сохранено как: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {str(e)}")

    def save_overlay(self):
        if self.overlay_image is None:
            messagebox.showwarning("Предупреждение", "Нет наложенного изображения для сохранения")
            return

        filename = filedialog.asksaveasfilename(
            title="Сохранить наложенное изображение",
            defaultextension=".ppm",
            filetypes=[("PPM files", "*.ppm"),
                       ("PGM files", "*.pgm"),
                       ("PBM files", "*.pbm"),
                       ("Все файлы", "*.*")]
        )
        if filename:
            try:
                self.overlay_image.save(filename)
                messagebox.showinfo("Успех", f"Наложенное изображение сохранено как: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {str(e)}")


def main():
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()


if __name__ == "__main__":
    main()