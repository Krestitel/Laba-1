import sys
import os
import math
import random

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QFileDialog, QMessageBox, QTextBrowser,
                             QRadioButton, QButtonGroup, QSlider, QInputDialog,
                             QColorDialog, QDialog, QGridLayout)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QBrush, QPen, QTransform
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSound


# ==========================================
# ЗАДАНИЕ 1: Min/Max/Среднее из файла
# ==========================================
class Task1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 1: Min/Max/Среднее из файла")
        self.resize(400, 250)

        layout = QVBoxLayout()

        self.btn_load = QPushButton("📂 Загрузить файл")
        self.btn_load.clicked.connect(self.load_file)

        self.label_max = QLabel("Максимум: —")
        self.label_min = QLabel("Минимум: —")
        self.label_avg = QLabel("Среднее: —")

        self.btn_save = QPushButton("💾 Сохранить результат")
        self.btn_save.clicked.connect(self.save_file)

        layout.addWidget(self.btn_load)
        layout.addWidget(self.label_max)
        layout.addWidget(self.label_min)
        layout.addWidget(self.label_avg)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)
        self.max_val = self.min_val = self.avg_val = None

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Text (*.txt)"
        )
        if not file_name:
            return
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()

            numbers = []
            for word in content.split():
                numbers.append(int(word))

            if not numbers:
                raise ValueError("Файл не содержит чисел")

            self.max_val = max(numbers)
            self.min_val = min(numbers)
            self.avg_val = sum(numbers) / len(numbers)

            self.label_max.setText(f"Максимум: {self.max_val}")
            self.label_min.setText(f"Минимум: {self.min_val}")
            self.label_avg.setText(f"Среднее: {self.avg_val:.2f}")

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка",
                f"Файл содержит неверные данные!\n\n{e}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def save_file(self):
        if self.max_val is None:
            QMessageBox.warning(self, "Ошибка", "Сначала загрузите файл!")
            return
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Text (*.txt)"
        )
        if not file_name:
            return
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(f"Максимум: {self.max_val}\n")
                f.write(f"Минимум: {self.min_val}\n")
                f.write(f"Среднее: {self.avg_val:.2f}\n")
            QMessageBox.information(self, "Готово", "Файл сохранён!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))


# ==========================================
# ЗАДАНИЕ 2: Текстовый редактор
# ==========================================
class Task2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 2: Текстовый редактор")
        self.resize(600, 400)

        layout = QVBoxLayout()

        buttons_layout = QHBoxLayout()
        self.btn_new = QPushButton("🆕 Новый")
        self.btn_open = QPushButton("📂 Открыть")
        self.btn_save = QPushButton("💾 Сохранить")
        buttons_layout.addWidget(self.btn_new)
        buttons_layout.addWidget(self.btn_open)
        buttons_layout.addWidget(self.btn_save)

        self.text_browser = QTextBrowser()

        layout.addLayout(buttons_layout)
        layout.addWidget(self.text_browser)
        self.setLayout(layout)

        self.current_file = None
        self.btn_new.clicked.connect(self.new_file)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save.clicked.connect(self.save_file)

    def new_file(self):
        self.text_browser.clear()
        self.current_file = None
        self.setWindowTitle("Задание 2: Текстовый редактор — Новый файл")

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть", "", "Text (*.txt);;All (*)"
        )
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    self.text_browser.setText(f.read())
                self.current_file = file_name
                self.setWindowTitle(f"Задание 2: {os.path.basename(file_name)}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def save_file(self):
        if self.current_file:
            target = self.current_file
        else:
            target, _ = QFileDialog.getSaveFileName(
                self, "Сохранить", "", "Text (*.txt)"
            )
            if not target:
                return
            self.current_file = target
        try:
            with open(target, 'w', encoding='utf-8') as f:
                f.write(self.text_browser.toPlainText())
            QMessageBox.information(self, "Готово", "Файл сохранён!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))


# ==========================================
# ЗАДАНИЕ 3: Работа с изображением
# ==========================================
class Task3(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 3: Работа с изображением")
        self.resize(600, 600)

        layout = QVBoxLayout()

        self.label_image = QLabel("Изображение не загружено")
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setMinimumSize(400, 400)
        self.label_image.setStyleSheet("border: 1px solid gray;")

        # Радиокнопки для каналов
        channels_layout = QHBoxLayout()
        self.rb_r = QRadioButton("Красный")
        self.rb_g = QRadioButton("Зелёный")
        self.rb_b = QRadioButton("Синий")
        self.rb_none = QRadioButton("Оригинал")
        self.rb_none.setChecked(True)

        self.channel_group = QButtonGroup(self)
        self.channel_group.addButton(self.rb_none, 0)
        self.channel_group.addButton(self.rb_r, 1)
        self.channel_group.addButton(self.rb_g, 2)
        self.channel_group.addButton(self.rb_b, 3)
        self.channel_group.buttonClicked.connect(self.update_view)

        channels_layout.addWidget(self.rb_none)
        channels_layout.addWidget(self.rb_r)
        channels_layout.addWidget(self.rb_g)
        channels_layout.addWidget(self.rb_b)

        # Кнопки поворота
        rotate_layout = QHBoxLayout()
        self.btn_rotate_left = QPushButton("↺ Влево на 90°")
        self.btn_rotate_right = QPushButton("↻ Вправо на 90°")
        self.btn_rotate_left.clicked.connect(lambda: self.rotate(-90))
        self.btn_rotate_right.clicked.connect(lambda: self.rotate(90))
        rotate_layout.addWidget(self.btn_rotate_left)
        rotate_layout.addWidget(self.btn_rotate_right)

        # Кнопка загрузки
        self.btn_open = QPushButton("📂 Загрузить изображение")
        self.btn_open.clicked.connect(self.open_image)

        layout.addWidget(self.label_image)
        layout.addLayout(channels_layout)
        layout.addLayout(rotate_layout)
        layout.addWidget(self.btn_open)
        self.setLayout(layout)

        self.original_image = None
        self.rotation = 0

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_name:
            return
        self.original_image = QImage(file_name)
        self.rotation = 0
        self.rb_none.setChecked(True)
        self.update_view()

    def update_view(self):
        if self.original_image is None:
            return

        img = self.original_image.copy()
        channel = self.channel_group.checkedId()

        # Применяем цветовой канал
        if channel != 0:
            for x in range(img.width()):
                for y in range(img.height()):
                    pixel = img.pixelColor(x, y)
                    r, g, b = pixel.red(), pixel.green(), pixel.blue()
                    if channel == 1:      # R
                        img.setPixelColor(x, y, QColor(r, 0, 0))
                    elif channel == 2:    # G
                        img.setPixelColor(x, y, QColor(0, g, 0))
                    elif channel == 3:    # B
                        img.setPixelColor(x, y, QColor(0, 0, b))

        # Применяем поворот
        pixmap = QPixmap.fromImage(img)
        if self.rotation != 0:
            pixmap = pixmap.transformed(QTransform().rotate(self.rotation))

        self.label_image.setPixmap(
            pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def rotate(self, angle):
        if self.original_image is None:
            return
        self.rotation = (self.rotation + angle) % 360
        self.update_view()


# ==========================================
# ЗАДАНИЕ 4: Прозрачность
# ==========================================
class Task4(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 4: Прозрачность")
        self.resize(600, 600)

        layout = QVBoxLayout()

        self.btn_open = QPushButton("📂 Открыть изображение")
        self.btn_open.clicked.connect(self.open_image)

        self.label_image = QLabel("Изображение не загружено")
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setMinimumSize(400, 400)
        self.label_image.setStyleSheet("border: 1px solid gray; background: white;")

        self.label_alpha = QLabel("Прозрачность: 255")

        self.slider_alpha = QSlider(Qt.Horizontal)
        self.slider_alpha.setRange(0, 255)
        self.slider_alpha.setValue(255)
        self.slider_alpha.valueChanged.connect(self.update_alpha)

        layout.addWidget(self.btn_open)
        layout.addWidget(self.label_image)
        layout.addWidget(self.label_alpha)
        layout.addWidget(self.slider_alpha)
        self.setLayout(layout)

        self.original_pixmap = None

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_name:
            return
        self.original_pixmap = QPixmap(file_name)
        self.update_alpha()

    def update_alpha(self):
        if self.original_pixmap is None:
            return
        alpha = self.slider_alpha.value()
        self.label_alpha.setText(f"Прозрачность: {alpha}")

        img = self.original_pixmap.toImage().convertToFormat(QImage.Format_ARGB32)
        for x in range(img.width()):
            for y in range(img.height()):
                pixel = img.pixelColor(x, y)
                pixel.setAlpha(alpha)
                img.setPixelColor(x, y, pixel)

        self.label_image.setPixmap(
            QPixmap.fromImage(img).scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )


# ==========================================
# ЗАДАНИЕ 5: Полосатый флаг
# ==========================================
class Task5(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 5: Полосатый флаг")
        self.resize(500, 400)

        layout = QVBoxLayout()

        self.btn_generate = QPushButton("🎨 Сгенерировать флаг")
        self.btn_generate.clicked.connect(self.generate)

        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setMinimumSize(400, 300)
        self.label_image.setStyleSheet("border: 1px solid gray;")

        layout.addWidget(self.btn_generate)
        layout.addWidget(self.label_image)
        self.setLayout(layout)

    def generate(self):
        n, ok = QInputDialog.getInt(
            self, "Количество цветов",
            "Сколько цветов в флаге?", 3, 2, 20
        )
        if not ok:
            return

        width, height = 400, 300
        pixmap = QPixmap(width, height)
        painter = QPainter(pixmap)
        stripe_height = height / n

        for i in range(n):
            color = QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            painter.fillRect(0, int(i * stripe_height),
                             width, int(stripe_height + 1), color)
        painter.end()
        self.label_image.setPixmap(pixmap)


# ==========================================
# ЗАДАНИЕ 6: Смайлик
# ==========================================
class Task6(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 6: Смайлик")
        self.resize(550, 600)

        layout = QVBoxLayout()

        self.label_canvas = QLabel()
        self.label_canvas.setAlignment(Qt.AlignCenter)
        self.label_canvas.setMinimumSize(500, 500)
        self.label_canvas.setStyleSheet("border: 1px solid gray; background: white;")

        self.btn_color = QPushButton("🎨 Выбрать цвет смайлика")

        self.label_size = QLabel("Масштаб: 200")

        self.slider_size = QSlider(Qt.Horizontal)
        self.slider_size.setRange(50, 400)
        self.slider_size.setValue(200)
        self.slider_size.valueChanged.connect(self.update_size)

        layout.addWidget(self.label_canvas)
        layout.addWidget(self.btn_color)
        layout.addWidget(self.label_size)
        layout.addWidget(self.slider_size)
        self.setLayout(layout)

        self.color = QColor(255, 220, 0)
        self.size = 200

        self.btn_color.clicked.connect(self.choose_color)
        self.draw_smiley()

    def choose_color(self):
        color = QColorDialog.getColor(self.color, self, "Выберите цвет")
        if color.isValid():
            self.color = color
            self.draw_smiley()

    def update_size(self, value):
        self.size = value
        self.label_size.setText(f"Масштаб: {value}")
        self.draw_smiley()

    def draw_smiley(self):
        pixmap = QPixmap(500, 500)
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = 250, 250
        r = self.size // 2

        # Лицо
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(Qt.black, 3))
        painter.drawEllipse(cx - r, cy - r, self.size, self.size)

        # Глаза
        eye_size = max(5, self.size // 8)
        painter.setBrush(QBrush(Qt.black))
        painter.drawEllipse(cx - r // 2 - eye_size // 2, cy - r // 3, eye_size, eye_size)
        painter.drawEllipse(cx + r // 2 - eye_size // 2, cy - r // 3, eye_size, eye_size)

        # Улыбка
        painter.setPen(QPen(Qt.black, max(2, self.size // 50)))
        painter.drawArc(cx - r // 2, cy - r // 4,
                        r, r // 2, 0, -180 * 16)

        painter.end()
        self.label_canvas.setPixmap(pixmap)


# ==========================================
# ЗАДАНИЕ 7: Фортепиано
# ==========================================
class Task7(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 7: Фортепиано")
        self.resize(700, 400)

        layout = QVBoxLayout()

        # Кнопки нот
        keys_layout = QHBoxLayout()

        self.notes = ["do", "re", "mi", "fa", "sol", "la", "si"]
        self.buttons = []
        self.sounds = {}

        for note in self.notes:
            btn = QPushButton(note.upper())
            btn.setFixedSize(80, 200)
            btn.setStyleSheet(
                "QPushButton { background: white; border: 2px solid black; "
                "font-size: 18px; font-weight: bold; }"
                "QPushButton:pressed { background: #ddd; }"
            )
            btn.clicked.connect(lambda checked, n=note: self.play(n))
            keys_layout.addWidget(btn)
            self.buttons.append(btn)

            # Загружаем звук
            sound_path = f"sounds/{note}.wav"
            if os.path.exists(sound_path):
                self.sounds[note] = QSound(sound_path)

        layout.addLayout(keys_layout)

        self.label_info = QLabel(
            "Нажимайте клавиши для воспроизведения нот.\n"
            "Звуковые файлы (.wav) должны лежать в папке sounds/ рядом с программой."
        )
        self.label_info.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label_info)
        self.setLayout(layout)

    def play(self, note):
        if note in self.sounds:
            self.sounds[note].play()
            self.label_info.setText(f"🎵 Играет нота: {note.upper()}")
        else:
            self.label_info.setText(
                f"⚠️ Файл sounds/{note}.wav не найден.\n"
                "Скачайте звуки с https://philharmonia.co.uk/resources/sound-samples/"
            )


# ==========================================
# ЗАДАНИЕ 8: L-система
# ==========================================
class Task8(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 8: L-система")
        self.resize(700, 700)

        layout = QVBoxLayout()

        self.btn_open = QPushButton("📂 Открыть L-систему (.txt)")
        self.btn_open.clicked.connect(self.open_file)

        self.label_canvas = QLabel()
        self.label_canvas.setAlignment(Qt.AlignCenter)
        self.label_canvas.setMinimumSize(600, 500)
        self.label_canvas.setStyleSheet("border: 1px solid gray; background: white;")

        self.label_step = QLabel("Шаг: 0")

        self.slider_iter = QSlider(Qt.Horizontal)
        self.slider_iter.setRange(0, 0)
        self.slider_iter.valueChanged.connect(self.draw)

        layout.addWidget(self.btn_open)
        layout.addWidget(self.label_canvas)
        layout.addWidget(self.label_step)
        layout.addWidget(self.slider_iter)
        self.setLayout(layout)

        self.rules = {}
        self.axiom = ""
        self.angle = 25
        self.iterations = []

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть L-систему", "", "Text (*.txt)"
        )
        if not file_name:
            return

        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if len(lines) < 3:
                raise ValueError("Файл должен содержать минимум 3 строки")

            self.name = lines[0]
            self.angle = int(lines[1])
            self.axiom = lines[2]

            # Разбираем правила
            self.rules = {}
            for line in lines[3:]:
                parts = line.split()
                if len(parts) >= 2:
                    self.rules[parts[0]] = parts[1]

            # Генерируем итерации
            self.iterations = [self.axiom]
            current = self.axiom
            for _ in range(5):  # 5 шагов эволюции
                next_str = "".join(self.rules.get(c, c) for c in current)
                self.iterations.append(next_str)
                current = next_str

            self.slider_iter.setRange(0, len(self.iterations) - 1)
            self.slider_iter.setValue(0)
            self.draw()

            self.setWindowTitle(f"Задание 8: {self.name}")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Неверный файл:\n{e}")

    def draw(self):
        if not self.iterations:
            return

        step = self.slider_iter.value()
        self.label_step.setText(f"Шаг: {step} / {len(self.iterations) - 1}")

        pixmap = QPixmap(600, 500)
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 1))

        # Turtle graphics
        x, y = 300, 400
        angle = -90  # смотрим вверх

        for char in self.iterations[step]:
            if char == 'F':
                new_x = x + 4 * math.cos(math.radians(angle))
                new_y = y + 4 * math.sin(math.radians(angle))
                painter.drawLine(int(x), int(y), int(new_x), int(new_y))
                x, y = new_x, new_y
            elif char == '+':
                angle += self.angle
            elif char == '-':
                angle -= self.angle

        painter.end()
        self.label_canvas.setPixmap(pixmap)


# ==========================================
# ГЛАВНОЕ МЕНЮ
# ==========================================
class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 3 - Меню")
        self.setGeometry(300, 300, 400, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        title = QLabel("Выберите задание:")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)

        tasks = [
            ("Задание 1: Min/Max/Среднее из файла", Task1),
            ("Задание 2: Текстовый редактор", Task2),
            ("Задание 3: Работа с изображением", Task3),
            ("Задание 4: Прозрачность изображения", Task4),
            ("Задание 5: Полосатый флаг", Task5),
            ("Задание 6: Смайлик", Task6),
            ("Задание 7: Фортепиано", Task7),
            ("Задание 8: L-система", Task8),
        ]

        self.windows = []
        for name, cls in tasks:
            btn = QPushButton(name)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, c=cls: self.open_task(c))
            layout.addWidget(btn)

        central.setLayout(layout)

    def open_task(self, cls):
        window = cls()
        self.windows.append(window)
        window.show()


# ==========================================
# ЗАПУСК
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())