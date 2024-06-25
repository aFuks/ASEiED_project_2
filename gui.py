import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QLabel, QGroupBox, QSlider, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ustawienia okna
        self.setWindowTitle("Stała szerokość okna")
        self.setFixedWidth(1200)  # Stała szerokość okna w pikselach
        self.setFixedHeight(800)  # Stała wysokość okna w pikselach

        self.initUI()

    def initUI(self):
        # Tworzenie głównego widgetu
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)

        self.map_label = QLabel(self)
        self.map_label.setFixedSize(800, 400)
        self.map_label.setStyleSheet("background-color: gray;")
        # Dodanie QLabel do layoutu lewego panelu
        left_layout.addWidget(self.map_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Tworzenie slidera dla godzin
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 23)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.update_label)
        self.slider.setFixedWidth(800)  # Ustawienie szerokości slidera

        left_layout.addWidget(self.slider)

        self.label = QLabel("00")
        self.label.setAlignment(Qt.AlignCenter)

        left_layout.addWidget(self.label)

        generate_button = QPushButton("Generuj wykres")
        generate_button.setFixedWidth(800)

        left_layout.addWidget(generate_button)

        main_layout.addLayout(left_layout)

        radio_layout = QVBoxLayout()
        radio_layout.setContentsMargins(20, 10, 10, 10)  # Ustawienie marginesów

        # Tworzenie grupy "Obszar"
        obszar_group = QGroupBox("Obszar")
        obszar_layout = QVBoxLayout(obszar_group)

        radio_button_1 = QRadioButton("La Palma")
        radio_button_2 = QRadioButton("Lotnisko Warszawa")
        radio_button_3 = QRadioButton("Ukraina")
        radio_button_4 = QRadioButton("Luizjana")

        radio_button_1.toggled.connect(lambda: self.display_map("la_palma.jpg"))
        radio_button_2.toggled.connect(lambda: self.display_map("lotnisko_warszawa.jpg"))
        radio_button_3.toggled.connect(lambda: self.display_map("ukraina.jpg"))
        radio_button_4.toggled.connect(lambda: self.display_map("luizjana.jpg"))

        obszar_layout.addWidget(radio_button_1)
        obszar_layout.addWidget(radio_button_2)
        obszar_layout.addWidget(radio_button_3)
        obszar_layout.addWidget(radio_button_4)

        # Tworzenie grupy "Data"
        data_group = QGroupBox("Data")
        data_layout = QVBoxLayout(data_group)

        radio_button_5 = QRadioButton("Opcja 5")
        radio_button_6 = QRadioButton("Opcja 6")
        radio_button_7 = QRadioButton("Opcja 7")
        radio_button_8 = QRadioButton("Opcja 8")
        radio_button_9 = QRadioButton("Opcja 9")
        radio_button_10 = QRadioButton("Opcja 10")

        data_layout.addWidget(radio_button_5)
        data_layout.addWidget(radio_button_6)
        data_layout.addWidget(radio_button_7)
        data_layout.addWidget(radio_button_8)
        data_layout.addWidget(radio_button_9)
        data_layout.addWidget(radio_button_10)


        radio_layout.addWidget(obszar_group)
        radio_layout.addSpacing(20)
        radio_layout.addWidget(data_group)

        main_layout.addLayout(radio_layout)

    def update_label(self, value):
        self.label.setText(f"{value:02d}")

    def display_map(self, image_path):

        pixmap = QPixmap(image_path)
        self.map_label.setPixmap(pixmap.scaled(self.map_label.size(), Qt.KeepAspectRatio))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
