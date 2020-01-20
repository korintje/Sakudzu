
"""
This demo demonstrates how to embed a matplotlib (mpl) plot
into a PyQt5 GUI application, including:
* Using the navigation toolbar
* Adding data to the plot
* Dynamically modifying the plot's properties
* Processing mpl events
* Saving the plot to a file from a menu
The main goal is to serve as a basis for developing rich PyQt GUI
applications featuring mpl plots (using the mpl OO API).
Eli Bendersky (eliben@gmail.com), updated by Ondrej Holesovsky.
License: this code is in the public domain
Last modified: 23.12.2019
"""
import sys, os, random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib
#import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from scipy.interpolate import interp1d
import numpy as np

class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Demo: PyQt with matplotlib')

        self.line_params = {"markersize": 128, "linewidth": 10}
        self.curve_params = {"markersize": 128, "linewidth": 10}
        self.scatter_params = {"markersize": 128, "linewidth": 10}

        #self.markersize = 128

        self.create_settings_tabs()
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        self.textbox.setText('1 2 3 4')
        self.on_draw()

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"

        path, ext = QFileDialog.getSaveFileName(self,
                        'Save file', '',
                        file_choices)
        path = path.encode('utf-8')
        if not path[-4:] == file_choices[-4:].encode('utf-8'):
            path += file_choices[-4:].encode('utf-8')
        print(path)
        if path:
            self.canvas.print_figure(path.decode(), dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def on_about(self):
        msg = """ A demo of using PyQt with matplotlib:

         * Use the matplotlib navigation bar
         * Add values to the text box and press Enter (or click "Draw")
         * Show or hide the grid
         * Drag the slider to modify the width of the bars
         * Save the plot to a file using the File menu
         * Click on a bar to receive an informative message
        """
        QMessageBox.about(self, "About the demo", msg.strip())

    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        #
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points

        QMessageBox.information(self, "Click!", msg)

    def change_scatter_params(self, target, value):
        self.scatter_params[target] = value
        self.on_draw()

    def change_line_params(self, target, value):
        self.line_params[target] = value
        self.on_draw()

    def change_curve_params(self, target, value):
        self.curve_params[target] = value
        self.on_draw()

    def on_draw(self):
        """ Redraws the figure
        """
        str = self.textbox.text().encode('utf-8')
        self.data = [int(s) for s in str.split()]

        x = range(len(self.data))
        y = [random.randrange(len(self.data)) for item in x]

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()
        self.axes.grid(self.grid_cb.isChecked())

        self.axes.plot(
            x,
            y,
            )

        f = interp1d(x, y, kind='cubic')
        resolution = 51
        start_x = x[0]
        end_x = x[-1]
        xnew = np.linspace(start_x, end_x, num=resolution)
        self.axes.plot(
            xnew,
            f(xnew),
            linewidth = self.curve_params["linewidth"],
            )

        self.axes.scatter(
            x=x,
            y=y,
            s=self.scatter_params["markersize"],
            c="pink",
            marker='o',
            cmap=None,
            norm=None,
            vmin=None,
            vmax=None,
            alpha=1,
            linewidths=None,
            verts=None,
            edgecolors=None,
            )

        self.canvas.draw()

    def create_main_frame(self):
        self.main_frame = QWidget()

        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Since we have only one plot, we can use add_axes
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)

        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.on_pick)

        # Create the navigation toolbar, tied to the canvas
        #
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

    def create_settings_tabs(self):

        # Initialize tab screen
        self.settings_tabs = QTabWidget()
        self.tab_data = QWidget()
        self.tab_line = QWidget()
        self.tab_marker = QWidget()
        self.settings_tabs.resize(300,200)

        # Add tabs
        self.settings_tabs.addTab(self.tab_data,"Data")
        self.settings_tabs.addTab(self.tab_line,"Line")
        self.settings_tabs.addTab(self.tab_marker,"Marker")

        # Create first tab
        self.tab_data.layout = QVBoxLayout(self)
        settings_label_x = QLabel('X-Data:')
        self.settings_data_x = QLineEdit(self)
        settings_label_y = QLabel('Y-Data:')
        self.settings_data_y = QLineEdit(self)
        settings_data_list = [settings_label_x, self.settings_data_x, settings_label_y, self.settings_data_y]
        for w in settings_data_list:
            self.tab_data.layout.addWidget(w)
        self.tab_data.setLayout(self.tab_data.layout)

        # Create first tab
        self.tab_line.layout = QVBoxLayout(self)
        settings_label_line_width = QLabel('Line Width:')
        self.settings_line_width = QLineEdit(self)
        self.settings_line_width.setValidator(QDoubleValidator())
        self.settings_line_width.setText(str(self.curve_params["linewidth"]))
        self.settings_line_width.editingFinished.connect(lambda:self.change_curve_params("linewidth", int(self.settings_line_width.text())))
        settings_label_line_color = QLabel('Line Color:')
        self.settings_line_color = QLineEdit(self)
        settings_line_list = [settings_label_line_width, self.settings_line_width, settings_label_line_color, self.settings_line_color]
        for w in settings_line_list:
            self.tab_line.layout.addWidget(w)
        self.tab_line.setLayout(self.tab_line.layout)

        # Create first tab
        self.tab_marker.layout = QVBoxLayout(self)
        settings_label_marker_size = QLabel('Marker Size:')
        self.settings_marker_size = QLineEdit(self)
        self.settings_marker_size.setValidator(QDoubleValidator())
        self.settings_marker_size.setText(str(self.scatter_params["markersize"]))
        self.settings_marker_size.editingFinished.connect(lambda:self.change_scatter_params("markersize", int(self.settings_marker_size.text())))
        settings_label_marker_color = QLabel('Marker Color:')
        self.settings_marker_color = QLineEdit(self)
        settings_marker_list = [settings_label_marker_size, self.settings_marker_size, settings_label_marker_color, self.settings_marker_color]
        for w in settings_marker_list:
            self.tab_marker.layout.addWidget(w)
        self.tab_marker.setLayout(self.tab_marker.layout)

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
