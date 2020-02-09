# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from FigureEditorUI import Ui_Form as FrameUi
from ScatterSettingsUI import Ui_Form as ScatterUi

class FigureEditor(QtWidgets.QWidget):

    # create Signals and Slots
    figureUpdated = QtCore.pyqtSignal()

    def __init__(self, fig, parent=None):

        # Initialize the instance
        super().__init__()

        # create figure window
        self.frame_ui = FrameUi()
        self.frame_ui.setupUi(self)

        # create matplotlib figure
        self.update_fig(fig)

        # create matplotlib canvas
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        for w in [self.canvas, self.mpl_toolbar]:
            self.frame_ui.verticalLayout_left.addWidget(w)
        self.update_draw()

        # Connect Signals and Slots
        self.frame_ui.AxsSelector.currentIndexChanged.connect(self.update_elements)
        self.frame_ui.ElementsSelector.currentIndexChanged.connect(self.update_settings)

    def update_draw(self):
        self.canvas.draw()
        self.figureUpdated.emit()

    def update_fig(self, fig):
        self.fig = fig
        if not self.fig.axes:
            self.fig.add_subplot(1, 1, 1)
        if not self.fig.axes[0].collections:
            self.fig.axes[0].scatter([0, 1, 2], [0, 2, 4], label="test")
        self.frame_ui.AxsSelector.clear()
        self.update_axs()

    def update_axs(self):
        self.axs = [{"collections": [], "lines": []} for i in self.fig.axes]
        for i, ax in enumerate(self.axs):
            for collection in self.fig.axes[i].collections:
                ax["collections"].append(collection._label)
            for line in self.fig.axes[i].lines:
                ax["lines"].append(line._label)
        self.frame_ui.AxsSelector.addItems(["ax"+str(i+1) for i, ax in enumerate(self.axs)])
        self.frame_ui.ElementsSelector.clear()
        self.update_elements()

    def update_elements(self):
        self.current_ax_idx = self.frame_ui.AxsSelector.currentIndex()
        self.current_ax_ctn = self.axs[self.current_ax_idx]
        for i, collection in enumerate(self.current_ax_ctn["collections"]):
            self.frame_ui.ElementsSelector.addItem(collection, ["collection", i])
        for i, line in enumerate(self.current_ax_ctn["lines"]):
            self.frame_ui.ElementsSelector.addItem(line, ["line", i])
        self.update_settings()

    def update_settings(self):
        self.current_element_idx = self.frame_ui.ElementsSelector.currentIndex()
        print(self.current_element_idx)
        self.current_element_cat = self.frame_ui.ElementsSelector.itemData(self.current_element_idx)[0]
        self.current_element_num = self.frame_ui.ElementsSelector.itemData(self.current_element_idx)[1]

        if self.current_element_cat == "collection":
            current_collection = self.fig.axes[self.current_ax_idx].collections[self.current_element_num]
            collection_params = {"label": current_collection._label,
                                 "sizes": current_collection._sizes[0],
                                }
            self.open_scatter_settings(collection_params)

        if self.current_element_cat == "line":
            current_line = self.fig.axes[self.current_ax_idx].lines[current_element_num]
            label = current_line._label
            linewidth = current_line._linewidth

    def open_scatter_settings(self, params):
        self.scatter_ui = ScatterUi()
        self.scatter_ui.setupUi(self.frame_ui.Settings)
        #print(params)
        self.scatter_ui.SBox_marker_size.setValue(params["sizes"])
        self.scatter_ui.SBox_marker_size.valueChanged.connect(lambda:self.change_scatter_marker_sizes(self.scatter_ui.SBox_marker_size.value()))
        #self.settings_ui.ElementsSelector.currentIndexChanged.connect(self.update_settings)

    def change_scatter_marker_sizes(self, size):
        _sizes = [size,]
        self.fig.axes[self.current_ax_idx].collections[self.current_element_idx]._sizes = _sizes
        self.update_draw()

    def change_line_sizes(self, ax_num, line_num, width):
        _linewidth = width
        self.fig.axes[ax_num].lines[line_num]._linewidth = _width
        #self.edit_script()
        #self.execute_script()
