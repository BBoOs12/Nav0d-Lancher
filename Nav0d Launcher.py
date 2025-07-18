import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,QHBoxLayout, QPushButton,
    QLineEdit, QMessageBox, QCheckBox,
    QLabel, QSlider, QComboBox, QFileDialog, QPlainTextEdit
)
from PyQt5.QtCore import Qt, QTimer, QProcess
from PyQt5 import QtGui
from minecraft_launcher_lib import install, command, utils
import webbrowser

translations = {
    "en": {
        "username": "Enter Username",
        "version": "Minecraft Version (e.g. 1.20.1)",
        "launch": "Launch",
        "Donate": "Donate",
        "settings": "Settings",
        "logs": "Minecraft logs will appear here...",
        "save_settings": "Save Settings",
        "ram": "RAM: {} GB",
        "language": "Language",
        "fullscreen": "Launch in Fullscreen",
        "settings_title": "Settings",
        "settings_saved": "Settings saved successfully!",
        "error_version": "Minecraft Version is required!",
        "error_username": "Username is required in offline mode!",
        "launching": "Launching Minecraft...\n",
        "started": "Minecraft started...\n",
        "exited": "\nMinecraft exited with code {}",
        "select_skin": "Select Skin PNG",
        "no_skin_selected": "No skin selected",
    },
    "el": {
        "username": "Όνομα χρήστη",
        "version": "Έκδοση Minecraft (π.χ. 1.20.1)",
        "launch": "Εκκίνηση",
        "Donate": "Donate",
        "settings": "Ρυθμίσεις",
        "logs": "Τα αρχεία καταγραφής Minecraft θα εμφανιστούν εδώ...",
        "save_settings": "Αποθήκευση Ρυθμίσεων",
        "ram": "RAM: {} GB",
        "language": "Γλώσσα",
        "fullscreen": "Πλήρης οθόνη",
        "settings_title": "Ρυθμίσεις",
        "settings_saved": "Οι ρυθμίσεις αποθηκεύτηκαν!",
        "error_version": "Η έκδοση Minecraft είναι υποχρεωτική!",
        "error_username": "Το όνομα χρήστη είναι απαραίτητο σε offline λειτουργία!",
        "launching": "Εκκίνηση Minecraft...\n",
        "started": "Το Minecraft ξεκίνησε...\n",
        "exited": "\nΤο Minecraft τερματίστηκε με κωδικό {}",
        "select_skin": "Επιλέξτε Skin PNG",
        "no_skin_selected": "Δεν έχει επιλεχθεί skin",
    },
    "es": {
        "username": "Introducir nombre de usuario",
        "version": "Versión de Minecraft (ej. 1.20.1)",
        "launch": "Iniciar",
        "Donate": "Donate",
        "settings": "Configuración",
        "logs": "Los registros de Minecraft aparecerán aquí...",
        "save_settings": "Guardar configuración",
        "ram": "RAM: {} GB",
        "language": "Idioma",
        "fullscreen": "Iniciar en pantalla completa",
        "settings_title": "Configuración",
        "settings_saved": "¡Configuración guardada correctamente!",
        "error_version": "¡Se requiere la versión de Minecraft!",
        "error_username": "¡Se requiere el nombre de usuario en modo sin conexión!",
        "launching": "Iniciando Minecraft...\n",
        "started": "Minecraft iniciado...\n",
        "exited": "\nMinecraft finalizado con código {}",
        "select_skin": "Seleccionar skin PNG",
        "no_skin_selected": "No se ha seleccionado ninguna skin",
    },
    "fr": {
        "username": "Entrez le nom d'utilisateur",
        "version": "Version de Minecraft (par exemple 1.20.1)",
        "launch": "Lancer",
        "Donate": "Donate",
        "settings": "Paramètres",
        "logs": "Les journaux Minecraft apparaîtront ici...",
        "save_settings": "Enregistrer les paramètres",
        "ram": "RAM : {} Go",
        "language": "Langue",
        "fullscreen": "Lancer en plein écran",
        "settings_title": "Paramètres",
        "settings_saved": "Paramètres enregistrés avec succès !",
        "error_version": "La version de Minecraft est requise !",
        "error_username": "Le nom d'utilisateur est requis en mode hors ligne !",
        "launching": "Lancement de Minecraft...\n",
        "started": "Minecraft démarré...\n",
        "exited": "\nMinecraft fermé avec le code {}",
        "select_skin": "Sélectionner un skin PNG",
        "no_skin_selected": "Aucun skin sélectionné",
    },
    "de": {
        "username": "Benutzernamen eingeben",
        "version": "Minecraft-Version (z.B. 1.20.1)",
        "launch": "starten",
        "Donate": "Donate",
        "settings": "Einstellungen",
        "logs": "Minecraft-Protokolle werden hier angezeigt...",
        "save_settings": "Einstellungen speichern",
        "ram": "RAM: {} GB",
        "language": "Sprache",
        "fullscreen": "Im Vollbildmodus starten",
        "settings_title": "Einstellungen",
        "settings_saved": "Einstellungen erfolgreich gespeichert!",
        "error_version": "Minecraft-Version erforderlich!",
        "error_username": "Benutzername erforderlich im Offline-Modus!",
        "launching": "Starte Minecraft...\n",
        "started": "Minecraft gestartet...\n",
        "exited": "\nMinecraft beendet mit Code {}",
        "select_skin": "Wähle Skin PNG",
        "no_skin_selected": "Kein Skin ausgewählt",
    },
    "pt": {
        "username": "Digite o nome de usuário",
        "version": "Versão do Minecraft (ex: 1.20.1)",
        "launch": "Iniciar",
        "Donate": "Donate",
        "settings": "Configurações",
        "logs": "Os registros do Minecraft aparecerão aqui...",
        "save_settings": "Salvar Configurações",
        "ram": "RAM: {} GB",
        "language": "Idioma",
        "fullscreen": "Iniciar em Tela Cheia",
        "settings_title": "Configurações",
        "settings_saved": "Configurações salvas com sucesso!",
        "error_version": "Versão do Minecraft é obrigatória!",
        "error_username": "Nome de usuário é obrigatório no modo offline!",
        "launching": "Iniciando Minecraft...\n",
        "started": "Minecraft iniciado...\n",
        "exited": "\nMinecraft encerrado com código {}",
        "select_skin": "Selecionar Skin PNG",
        "no_skin_selected": "Nenhuma skin selecionada",
    },
    "ru": {
        "username": "Введите имя пользователя",
        "version": "Версия Minecraft (например, 1.20.1)",
        "launch": "Запустить",
        "Donate": "Donate",
        "settings": "Настройки",
        "logs": "Логи Minecraft будут отображаться здесь...",
        "save_settings": "Сохранить настройки",
        "ram": "ОЗУ: {} ГБ",
        "language": "Язык",
        "fullscreen": "Запуск в полноэкранном режиме",
        "settings_title": "Настройки",
        "settings_saved": "Настройки успешно сохранены!",
        "error_version": "Требуется версия Minecraft!",
        "error_username": "Имя пользователя обязательно в автономном режиме!",
        "launching": "Запуск Minecraft...\n",
        "started": "Minecraft запущен...\n",
        "exited": "\nMinecraft завершился с кодом {}",
        "select_skin": "Выберите скин PNG",
        "no_skin_selected": "Скин не выбран",
    }
}

class MinecraftLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle("Nav0d Launcher")
        self.setFixedSize(500, 480)
        self.log_buffer = []
        self.process = None
        self.selected_skin_path = None
        self.log_window = None

        self.initUI()

        self.log_timer = QTimer()
        self.log_timer.setInterval(100)
        self.log_timer.timeout.connect(self.flush_log_buffer)
        self.log_timer.start()

        self.current_language = "en"
        self.load_language_from_settings()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # add margins around the main layout
        layout.setSpacing(15)  # spacing between elements

        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(30)
        self.username_input.setStyleSheet("padding: 5px; font-size: 14px;")
        layout.addWidget(self.username_input)

        self.mc_versions = [
            "1.21.7", "1.21.6", "1.21.5", "1.21.4", "1.21.3",
            "1.21.2", "1.21.1", "1.21",
            "1.20.1", "1.20", "1.19.4", "1.19.3", "1.19.2",
            "1.18.2", "1.18.1", "1.17.1", "1.16.5", "1.12.2",
            "1.11", "1.10", "1.9", "1.8.9", "1.7.10"
        ]

        self.version_input = QComboBox()
        self.version_input.addItems(self.mc_versions)
        self.version_input.setFixedHeight(30)
        self.version_input.setStyleSheet("padding: 5px; font-size: 14px;")
        layout.addWidget(self.version_input)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # reduce space between buttons

        self.launch_button = QPushButton()
        self.launch_button.clicked.connect(self.launch_minecraft)
        self.launch_button.setFixedWidth(120)
        self.launch_button.setFixedHeight(35)
        self.launch_button.setStyleSheet("""
            QPushButton {
                background-color: #3b7ddd;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #2a5bb8;
            }
            QPushButton:pressed {
                background-color: #1d3d80;
            }
        """)
        button_layout.addWidget(self.launch_button)

        self.donate = QPushButton()
        self.donate.clicked.connect(self.donate_me)
        self.donate.setFixedWidth(120)
        self.donate.setFixedHeight(35)
        self.donate.setStyleSheet("""
            QPushButton {
                background-color: #fac84f;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #ffb500;
            }
            QPushButton:pressed {
                background-color: #ffb500;
            }
        """)
        button_layout.addWidget(self.donate)

        self.settings_button = QPushButton()
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setFixedWidth(120)
        self.settings_button.setFixedHeight(35)
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #4e555b;
            }
        """)
        button_layout.addWidget(self.settings_button)

        # Add a spacer at the end to push buttons left if needed
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def apply_language(self, lang_code):
        tr = translations.get(lang_code, translations["en"])
        self.username_input.setPlaceholderText(tr["username"])
        self.version_input.setPlaceholderText(tr["version"])
        self.launch_button.setText(tr["launch"])
        self.donate.setText(tr["Donate"])
        self.settings_button.setText(tr["settings"])

    def donate_me(self):
        webbrowser.open_new_tab("https://buy.stripe.com/test_00wdRbekg1gr1QDd7r7EQ00")


    def load_language_from_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.current_language = settings.get("language", "en")
        self.apply_language(self.current_language)

    def launch_minecraft(self):
        tr = translations.get(self.current_language, translations["en"])

        version = self.version_input.currentText().strip()
        username = self.username_input.text().strip()

        if not version:
            QMessageBox.warning(self, "Input Error", tr["error_version"])
            return

        if not username:
            QMessageBox.warning(self, "Input Error", tr["error_username"])
            return

        options = {
            "username": username,
            "uuid": "12345678-1234-5678-1234-567812345678",
            "token": "12345678-1234-5678-1234-567812345678"
        }


        settings_path = "settings.json"
        ram = 2048
        lang = "en"
        fullscreen = False
        skin_path = None
        show_log_window = False

        if os.path.exists(settings_path):
            with open(settings_path, "r") as f:
                settings = json.load(f)
                ram = int(settings.get("ram", 2048))
                lang = settings.get("language", "en")
                fullscreen = settings.get("fullscreen", False)
                skin_path = settings.get("skin_path", None)
                show_log_window = settings.get("show_log_window", False)

        options["jvmArguments"] = [f"-Xmx{ram}M", f"-Xms{ram}M"]

        game_args = []
        if fullscreen:
            game_args.extend(["--fullscreen", "true"])
        if lang:
            game_args.extend(["--lang", lang])
        if game_args:
            options["gameArguments"] = game_args

        game_directory = utils.get_minecraft_directory()

        try:
            install.install_minecraft_version(version, game_directory)
            minecraft_cmd = command.get_minecraft_command(version, game_directory, options)

            self.append_log(tr["launching"])

            if show_log_window:
                self.open_log_window()

            self.process = QProcess(self)
            self.process.setProgram(minecraft_cmd[0])
            self.process.setArguments(minecraft_cmd[1:])
            self.process.setWorkingDirectory(game_directory)

            self.process.readyReadStandardOutput.connect(self.read_stdout)
            self.process.readyReadStandardError.connect(self.read_stderr)
            self.process.started.connect(lambda: self.append_log(tr["started"]))
            self.process.finished.connect(lambda code, status: self.append_log(tr["exited"].format(code)))

            self.process.start()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def read_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.log_buffer.append(data)

    def read_stderr(self):
        data = self.process.readAllStandardError().data().decode()
        self.log_buffer.append(data)

    def flush_log_buffer(self):
        if self.log_buffer and self.log_window:
            self.log_output.appendPlainText(''.join(self.log_buffer))
            self.log_buffer.clear()

    def append_log(self, text):
        self.log_buffer.append(text)
        if self.log_window:
            self.flush_log_buffer()

    def open_log_window(self):
        if self.log_window is None:
            self.log_window = QWidget()
            self.log_window.setWindowTitle("Logs")
            self.log_window.setFixedSize(600, 400)

            layout = QVBoxLayout()
            
            # Log output text box
            self.log_output = QPlainTextEdit()
            self.log_output.setReadOnly(True)
            layout.addWidget(self.log_output)

            # Clear Text button
            clear_text_button = QPushButton("Clear Logs")
            clear_text_button.setFixedHeight(30)
            clear_text_button.clicked.connect(self.log_output.clear)
            layout.addWidget(clear_text_button)

            self.log_window.setLayout(layout)

        self.log_window.show()
        self.log_window.raise_()


    def open_settings(self):
        tr = translations.get(self.current_language, translations["en"])

        self.settings_window = QWidget()
        self.settings_window.setWindowTitle(tr["settings_title"])
        self.settings_window.setFixedSize(360, 400)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # RAM slider with label on top
        ram_layout = QVBoxLayout()
        ram_layout.setSpacing(8)

        self.ram_label = QLabel(tr["ram"].format(4096))
        self.ram_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.ram_slider = QSlider(Qt.Horizontal)
        self.ram_slider.setMinimum(512)
        self.ram_slider.setMaximum(32768)
        self.ram_slider.setValue(4096)
        self.ram_slider.setTickInterval(512)
        self.ram_slider.setTickPosition(QSlider.TicksBelow)
        self.ram_slider.valueChanged.connect(
            lambda value: self.ram_label.setText(tr["ram"].format(value))
        )
        ram_layout.addWidget(self.ram_label)
        ram_layout.addWidget(self.ram_slider)
        main_layout.addLayout(ram_layout)

        # Language dropdown with label
        lang_label = QLabel(tr["language"])
        lang_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(lang_label)

        self.language_dropdown = QComboBox()
        self.language_dropdown.addItem("English", "en")
        self.language_dropdown.addItem("Greek", "el")
        self.language_dropdown.addItem("Spanish", "es")
        self.language_dropdown.addItem("French", "fr")
        self.language_dropdown.addItem("German", "de")
        self.language_dropdown.addItem("Russian", "ru")
        self.language_dropdown.addItem("Portuguese", "pt")
        self.language_dropdown.setFixedHeight(28)
        main_layout.addWidget(self.language_dropdown)

        # Checkboxes with some spacing and consistent style
        self.fullscreen_checkbox = QCheckBox(tr["fullscreen"])
        self.fullscreen_checkbox.setStyleSheet("font-size: 13px;")
        main_layout.addWidget(self.fullscreen_checkbox)

        self.show_log_checkbox = QCheckBox("Show log window on launch")
        self.show_log_checkbox.setStyleSheet("font-size: 13px;")
        main_layout.addWidget(self.show_log_checkbox)

        # Skin selection layout with label and button side by side
        skin_layout = QHBoxLayout()
        self.skin_path_label = QLabel(tr["no_skin_selected"])
        self.skin_path_label.setStyleSheet("font-style: italic; color: gray;")
        self.skin_path_label.setMinimumWidth(180)
        self.skin_select_button = QPushButton(tr["select_skin"])
        self.skin_select_button.setFixedWidth(120)
        skin_layout.addWidget(self.skin_path_label)
        skin_layout.addWidget(self.skin_select_button)
        main_layout.addLayout(skin_layout)

        def select_skin_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self.settings_window, tr["select_skin"], "", "PNG Images (*.png)"
            )
            if file_path:
                self.skin_path_label.setText(file_path)
                self.selected_skin_path = file_path

        self.skin_select_button.clicked.connect(select_skin_file)

        # Save button centered and styled
        save_button = QPushButton(tr["save_settings"])
        save_button.setFixedHeight(32)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #3b7ddd;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2a5bb8;
            }
            QPushButton:pressed {
                background-color: #1d3d80;
            }
        """)
        save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(save_button, alignment=Qt.AlignCenter)

        self.settings_window.setLayout(main_layout)

        # Load saved settings if available
        self.selected_skin_path = None
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.ram_slider.setValue(int(settings.get("ram", 4096)))
                lang = settings.get("language", "en")
                index = self.language_dropdown.findData(lang)
                if index != -1:
                    self.language_dropdown.setCurrentIndex(index)
                self.fullscreen_checkbox.setChecked(settings.get("fullscreen", False))
                skin_path = settings.get("skin_path", None)
                if skin_path and os.path.isfile(skin_path):
                    self.selected_skin_path = skin_path
                    self.skin_path_label.setText(skin_path)
                else:
                    self.selected_skin_path = None
                    self.skin_path_label.setText(tr["no_skin_selected"])
                self.show_log_checkbox.setChecked(settings.get("show_log_window", False))

        self.settings_window.show()


    def save_settings(self):
        tr = translations.get(self.current_language, translations["en"])
        ram = self.ram_slider.value()
        language = self.language_dropdown.currentData()
        fullscreen = self.fullscreen_checkbox.isChecked()
        show_log_window = self.show_log_checkbox.isChecked()

        settings = {
            "ram": ram,
            "language": language,
            "fullscreen": fullscreen,
            "skin_path": self.selected_skin_path,
            "show_log_window": show_log_window
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

        QMessageBox.information(self.settings_window, tr["settings_title"], tr["settings_saved"])

        self.current_language = language
        self.apply_language(language)
        self.settings_window.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinecraftLauncher()
    window.show()
    sys.exit(app.exec_())
