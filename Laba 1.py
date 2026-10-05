import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QCheckBox, QTextEdit, QMessageBox, QInputDialog, QComboBox)
from PyQt5.QtCore import Qt


# ==========================================
# ЗАДАНИЕ 1: Перекидыватель слов
# ==========================================
class Task1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 1: Перекидыватель слов")
        self.setGeometry(100, 100, 400, 150)
        self.is_forward = True  # Флаг направления

        layout = QVBoxLayout()

        # Поля ввода
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input2.setReadOnly(True)  # Второе поле только для чтения (или можно разрешить, но по логике оно приемник)

        # Кнопка
        self.btn = QPushButton("Перекинуть ->")
        self.btn.clicked.connect(self.transfer_text)

        layout.addWidget(QLabel("Первое поле:"))
        layout.addWidget(self.input1)
        layout.addWidget(QLabel("Второе поле:"))
        layout.addWidget(self.input2)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def transfer_text(self):
        if self.is_forward:
            # Из первого во второй
            text = self.input1.text()
            self.input2.setText(text)
            self.input1.clear()
            self.btn.setText("<- Перекинуть")
            self.is_forward = False
        else:
            # Из второго в первый
            text = self.input2.text()
            self.input1.setText(text)
            self.input2.clear()
            self.btn.setText("Перекинуть ->")
            self.is_forward = True


# ==========================================
# ЗАДАНИЕ 2: Калькулятор выражений (eval)
# ==========================================
class Task2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 2: Вычисление выражения")
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()

        self.input_expr = QLineEdit()
        self.input_expr.setPlaceholderText("Введите выражение, например: 1 + 2 * 3")

        self.btn_calc = QPushButton("Вычислить")
        self.btn_calc.clicked.connect(self.calculate)

        self.result_field = QLineEdit()
        self.result_field.setReadOnly(True)

        layout.addWidget(QLabel("Выражение:"))
        layout.addWidget(self.input_expr)
        layout.addWidget(self.btn_calc)
        layout.addWidget(QLabel("Результат:"))
        layout.addWidget(self.result_field)

        self.setLayout(layout)

    def calculate(self):
        expr = self.input_expr.text()
        try:
            # Используем eval, как указано в задании
            result = eval(expr)
            self.result_field.setText(str(result))
        except Exception as e:
            self.result_field.setText("Ошибка!")
            QMessageBox.warning(self, "Ошибка", f"Неверное выражение: {e}")


# ==========================================
# ЗАДАНИЕ 3: Чекбоксы и Виджеты
# ==========================================
class Task3(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 3: Управление видимостью")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Создаем чекбокс
        self.chk = QCheckBox("Показать/Скрыть элементы")
        self.chk.stateChanged.connect(self.toggle_widgets)

        # Создаем несколько виджетов для демонстрации
        self.label1 = QLabel("Это метка 1")
        self.btn1 = QPushButton("Это кнопка 1")
        self.input1 = QLineEdit("Это поле ввода")

        layout.addWidget(self.chk)
        layout.addWidget(self.label1)
        layout.addWidget(self.btn1)
        layout.addWidget(self.input1)

        self.setLayout(layout)

    def toggle_widgets(self):
        # Универсальный обработчик
        state = self.chk.isChecked()

        # Меняем видимость
        self.label1.setVisible(state)
        self.btn1.setVisible(state)
        self.input1.setVisible(state)

        # Или наоборот, в зависимости от логики.
        # В задании сказано "прячут и показывают", обычно галочка = показать.


# ==========================================
# ЗАДАНИЕ 4: Азбука Морзе
# ==========================================
class Task4(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 4: Азбука Морзе")
        self.setGeometry(100, 100, 500, 300)

        # Словарь Морзе (упрощенный)
        self.morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..'
        }

        layout = QVBoxLayout()

        # Поле вывода
        self.output = QLineEdit()
        self.output.setReadOnly(True)
        layout.addWidget(QLabel("Результат:"))
        layout.addWidget(self.output)

        # Сетка для кнопок
        grid_layout = QHBoxLayout()  # Или QGridLayout, но здесь просто в ряд
        # Создаем кнопки в цикле
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            btn = QPushButton(char)
            btn.setFixedSize(40, 40)
            # Используем лямбду, чтобы передать букву в функцию
            btn.clicked.connect(lambda checked, c=char: self.add_morse(c))
            grid_layout.addWidget(btn)

        # Чтобы кнопки влезли, можно использовать QGridLayout, но для простоты сделаем прокрутку или уменьшим
        # В данном примере просто добавим в layout (может быть тесно на экране)
        container = QWidget()
        container.setLayout(grid_layout)

        layout.addWidget(container)
        self.setLayout(layout)

    def add_morse(self, char):
        code = self.morse_dict.get(char, "")
        current_text = self.output.text()
        # Добавляем пробел между буквами для читаемости
        self.output.setText(current_text + code + " ")


# ==========================================
# ЗАДАНИЕ 5: Ресторан
# ==========================================
class Task5(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 5: Заказ в ресторане")
        self.setGeometry(100, 100, 500, 400)

        # Меню: Название -> Цена
        self.menu = {
            "Борщ": 350,
            "Пельмени": 420,
            "Стейк": 1200,
            "Салат Цезарь": 550,
            "Чай": 150,
            "Кофе": 200
        }

        self.checkboxes = {}  # Словарь для хранения чекбоксов и цен

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Выберите блюда:"))

        # Создаем чекбоксы
        for dish, price in self.menu.items():
            chk = QCheckBox(f"{dish} ({price} руб.)")
            chk.stateChanged.connect(self.update_order)  # При изменении обновляем заказ
            layout.addWidget(chk)
            self.checkboxes[dish] = (chk, price)

        # Поле вывода
        layout.addWidget(QLabel("Ваш заказ:"))
        self.order_text = QTextEdit()
        self.order_text.setReadOnly(True)
        layout.addWidget(self.order_text)

        self.setLayout(layout)

    def update_order(self):
        total = 0
        text = ""
        for dish, (chk, price) in self.checkboxes.items():
            if chk.isChecked():
                text += f"{dish} - {price} руб.\n"
                total += price

        text += f"\nИтого: {total} руб."
        self.order_text.setText(text)


# ==========================================
# ЗАДАНИЕ 6: Калькулятор
# ==========================================
class Task6(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 6: Калькулятор")
        self.setGeometry(100, 100, 300, 400)

        self.current_expression = ""  # Строка для хранения выражения

        layout = QVBoxLayout()

        # Дисплей
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 20px; padding: 10px;")
        layout.addWidget(self.display)

        # Сетка кнопок
        grid = QVBoxLayout()  # Используем вложенные layout'ы для рядов

        # Ряды кнопок
        rows = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['.', '0', '=', '+'],
            ['C']  # Очистка
        ]

        for row in rows:
            h_layout = QHBoxLayout()
            for label in row:
                btn = QPushButton(label)
                btn.setFixedSize(60, 60)
                btn.clicked.connect(lambda checked, l=label: self.on_button_click(l))
                h_layout.addWidget(btn)
            grid.addLayout(h_layout)

        layout.addLayout(grid)
        self.setLayout(layout)

    def on_button_click(self, char):
        if char == 'C':
            self.current_expression = ""
            self.display.setText("")
        elif char == '=':
            try:
                # Вычисляем
                result = eval(self.current_expression)
                self.display.setText(str(result))
                self.current_expression = str(result)  # Чтобы можно было продолжать считать
            except ZeroDivisionError:
                self.display.setText("Ошибка: деление на 0")
                self.current_expression = ""
            except Exception:
                self.display.setText("Ошибка")
                self.current_expression = ""
        else:
            self.current_expression += str(char)
            self.display.setText(self.current_expression)


# ==========================================
# ГЛАВНОЕ МЕНЮ
# ==========================================
class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 1 - Меню")
        self.setGeometry(300, 300, 300, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        label = QLabel("Выберите задание:")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Кнопки выбора задания
        for i in range(1, 7):
            btn = QPushButton(f"Задание {i}")
            btn.clicked.connect(lambda checked, n=i: self.open_task(n))
            layout.addWidget(btn)

        self.central_widget.setLayout(layout)
        self.windows = []  # Список для хранения ссылок на окна, чтобы они не закрывались

    def open_task(self, number):
        if number == 1:
            self.windows.append(Task1())
        elif number == 2:
            self.windows.append(Task2())
        elif number == 3:
            self.windows.append(Task3())
        elif number == 4:
            self.windows.append(Task4())
        elif number == 5:
            self.windows.append(Task5())
        elif number == 6:
            self.windows.append(Task6())

        self.windows[-1].show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())