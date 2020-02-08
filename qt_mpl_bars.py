from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.create_main_frame()
        self.canvas.draw()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.canvas.mpl_connect('pick_event', self.on_pick)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        #
        self.textbox = QLineEdit()
        self.textbox.setMinimumWidth(200)
        self.textbox.editingFinished.connect(self.on_draw)

        self.draw_button = QPushButton("&Draw")
        self.draw_button.clicked.connect(self.on_draw)

        self.grid_cb = QCheckBox("Show &Grid")
        self.grid_cb.setChecked(False)
        self.grid_cb.stateChanged.connect(self.on_draw)

        slider_label = QLabel('Bar width (%):')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(20)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.on_draw)

        settings_menu_label = QLabel('Settings menu:')
        #self.settings_menu = QComboBox(self)
        #self.settings_menu.addItem("Data")
        #self.settings_menu.addItem("Line")
        #self.settings_menu.addItem("Marker")
        #self.settings_menu.currentIndexChanged.connect(lambda: self.create_menu(self.settings_menu.currentText()))
        #self.settings_menu.setCurrentIndex(1)

        delta_scripts_label = QLabel("Delta Scripts")
        self.delta_scripts = QPlainTextEdit(self)

        # Box-Layer = 1
        vbox_canvas = QVBoxLayout()
        for w in [self.canvas, self.mpl_toolbar]:
            vbox_canvas.addWidget(w)

        vbox_settings_wrapper = QVBoxLayout()
        vbox_settings_wrapper.addWidget(self.settings_tabs)

        vbox_scripts = QVBoxLayout()
        for w in [delta_scripts_label, self.delta_scripts]:
            vbox_scripts.addWidget(w)

        # Box-Layer = 0
        hbox = QHBoxLayout()
        for l in [vbox_canvas, vbox_settings_wrapper, vbox_scripts]:
            hbox.addLayout(l)
            hbox.setAlignment(l, Qt.AlignVCenter)

        self.main_frame.setLayout(hbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("This is a demo")
        self.statusBar().addWidget(self.status_text, 1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot,
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close,
            shortcut="Ctrl+Q", tip="Close the application")

        self.add_actions(self.file_menu,
            (load_file_action, None, quit_action))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
            shortcut='F1', slot=self.on_about,
            tip='About the demo')

        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None,
                        icon=None, tip=None, checkable=False):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
