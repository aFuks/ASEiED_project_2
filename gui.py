import sys
import os
import folium
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QLabel, \
    QGroupBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ustawienia okna
        self.setWindowTitle("Analiza lotów")
        self.setFixedWidth(1200)  # Stała szerokość okna w pikselach
        self.setFixedHeight(800)  # Stała wysokość okna w pikselach

        # Inicjalizacja interfejsu użytkownika
        self.initUI()
        self.display_default([52.404018184379126, 20.753517547628764], [52.0770061643252, 21.387170972121773])

    def initUI(self):
        # Tworzenie głównego widgetu
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Tworzenie głównego layoutu
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Ustawienie marginesów

        # Tworzenie layoutu dla lewego panelu
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)  # Brak odstępów między elementami

        # Tworzenie przeglądarki do wyświetlania mapy
        self.map_view = QWebEngineView()
        self.map_view.setFixedSize(800, 500)  # Ustawienie stałego rozmiaru

        # Dodanie przeglądarki do layoutu lewego panelu
        left_layout.addWidget(self.map_view, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Tworzenie przycisku "Generuj wykres"
        generate_button = QPushButton("Generuj wykres")
        generate_button.setFixedWidth(800)  # Ustawienie szerokości przycisku
        generate_button.clicked.connect(self.generate_plot)

        # Dodanie przycisku do layoutu lewego panelu
        left_layout.addWidget(generate_button)

        # Dodanie lewego panelu do głównego layoutu
        main_layout.addLayout(left_layout)

        # Tworzenie layoutu dla przycisków radiowych
        radio_layout = QVBoxLayout()
        radio_layout.setContentsMargins(20, 10, 10, 10)  # Ustawienie marginesów

        # Tworzenie grupy "Obszar"
        obszar_group = QGroupBox("Obszar")
        obszar_layout = QVBoxLayout(obszar_group)

        self.radio_button_2 = QRadioButton("Warszawa")
        self.radio_button_2.toggled.connect(lambda: self.display_map('w', [52.404018184379126, 20.753517547628764], [52.0770061643252, 21.387170972121773]))
        self.radio_button_3 = QRadioButton("Ukraina")
        self.radio_button_3.toggled.connect(lambda: self.display_map('u', [47.9525254824843, 24.04518269949129], [52.24749063117518, 38.78179587580102]))
        self.radio_button_4 = QRadioButton("południe Luizjany")
        self.radio_button_4.toggled.connect(lambda: self.display_map('l', [30.721262954175135, -91.39241969038389], [29.348298442498482, -89.42478394412178]))

        obszar_layout.addWidget(self.radio_button_2)
        obszar_layout.addWidget(self.radio_button_3)
        obszar_layout.addWidget(self.radio_button_4)

        # Tworzenie grupy "Data"
        data_group = QGroupBox("Data")
        data_layout = QVBoxLayout(data_group)

        self.radio_button_5 = QRadioButton("29.11.2021 - erupcja Wulkanu Cumbre")
        self.radio_button_6 = QRadioButton("29.06.2020 - Początek pandemii COVID19")
        self.radio_button_7 = QRadioButton("28.02.2022 - Start wojny na Ukrainie")
        self.radio_button_8 = QRadioButton("30.08.2021 - Huragan Ida")
        self.radio_button_9 = QRadioButton("20.12.2021")

        data_layout.addWidget(self.radio_button_5)
        data_layout.addWidget(self.radio_button_6)
        data_layout.addWidget(self.radio_button_7)
        data_layout.addWidget(self.radio_button_8)
        data_layout.addWidget(self.radio_button_9)

        # Dodanie grup do layoutu przycisków radiowych
        radio_layout.addWidget(obszar_group)
        radio_layout.addSpacing(20)  # Odstęp między grupami
        radio_layout.addWidget(data_group)

        # Dodanie layoutu z przyciskami radiowymi do głównego layoutu
        main_layout.addLayout(radio_layout)

    def get_selected_region(self):
        if self.radio_button_2.isChecked():
            return "warszawa"
        elif self.radio_button_3.isChecked():
            return "ukraine"
        elif self.radio_button_4.isChecked():
            return "louisiana"
        return None

    def get_selected_date(self):
        if self.radio_button_5.isChecked():
            return "2021-11-29"
        elif self.radio_button_6.isChecked():
            return "2020-06-29"
        elif self.radio_button_7.isChecked():
            return "2022-02-28"
        elif self.radio_button_8.isChecked():
            return "2021-08-30"
        elif self.radio_button_9.isChecked():
            return "2021-12-20"
        return None

    def generate_plot(self):
        selected_region = self.get_selected_region()
        selected_date = self.get_selected_date()

        if selected_region and selected_date:
            if selected_region == "warszawa":
                nw, se = [52.404018184379126, 20.753517547628764], [52.0770061643252, 21.387170972121773]
            elif selected_region == "ukraine":
                nw, se = [47.9525254824843, 24.04518269949129], [52.24749063117518, 38.78179587580102]
            elif selected_region == "louisiana":
                nw, se = [30.721262954175135, -91.39241969038389], [29.348298442498482, -89.42478394412178]
            self.plot_flights(selected_region, selected_date, nw, se)
        else:
            self.show_message("Wybierz region i datę")

    def plot_flights(self, region, date, nw, se):
        df = pd.read_csv('part2.csv')
        filtered_df = df[(df['region'] == region) & (df['date'] == date)]

        if filtered_df.empty:
            self.show_message("Brak danych z wybranego dnia.")
            return

        zoom = 10 if region == 'warszawa' else 6 if region == 'ukraine' else 8
        m = folium.Map(location=[filtered_df['lat'].mean(), filtered_df['lon'].mean()], zoom_start=zoom)

        # Dodawanie prostokąta dla określonego obszaru
        folium.Rectangle(bounds=[nw, se], color='cyan', fill=True, fill_opacity=0).add_to(m)

        for icao24 in filtered_df['icao24'].unique():
            aircraft_data = filtered_df[filtered_df['icao24'] == icao24]
            flight_path = [(row['lat'], row['lon']) for _, row in aircraft_data.iterrows() if not row['onground']]

            if flight_path:
                folium.PolyLine(
                    flight_path,
                    color='blue',
                    weight=2.5,
                    opacity=1
                ).add_to(m)

        # Zapisz mapę jako plik HTML
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'flight_map.html'))
        m.save(file_path)

        # Załaduj mapę w przeglądarce
        self.map_view.setUrl(QUrl.fromLocalFile(file_path))

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Informacja")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

    def display_map(self, region, nw, se):
        zoom = 10 if region == 'w' else 6 if region == 'u' else 8
        # Tworzenie mapy przy użyciu folium
        m = folium.Map(location=[(nw[0] + se[0]) / 2, (nw[1] + se[1]) / 2], zoom_start=zoom)

        # Dodawanie prostokąta dla określonego obszaru
        folium.Rectangle(bounds=[nw, se], color='cyan', fill=True, fill_opacity=0).add_to(m)

        # Zapisz mapę jako plik HTML
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'map.html'))
        m.save(file_path)

        # Załaduj mapę w przeglądarce
        self.map_view.setUrl(QUrl.fromLocalFile(file_path))

    def display_default(self, nw, se):
        # Tworzenie mapy przy użyciu folium
        m = folium.Map(location=[(nw[0] + se[0]) / 2, (nw[1] + se[1]) / 2], zoom_start=5)

        # Zapisz mapę jako plik HTML
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'map.html'))
        m.save(file_path)

        # Załaduj mapę w przeglądarce
        self.map_view.setUrl(QUrl.fromLocalFile(file_path))


def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_cyan.xml')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
