# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from FigureEditorUI import Ui_Form as FrameUi
from ScatterSettingsUI import Ui_Form as ScatterUi

class FigureEditor(QtWidgets.QWidget):

    def __init__(self, fig, parent=None):
        super().__init__()

        self.frame_ui = FrameUi()
        self.frame_ui.setupUi(self)
        self.update_fig(fig)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.draw()
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        for w in [self.canvas, self.mpl_toolbar]:
            self.frame_ui.verticalLayout_left.addWidget(w)

        # Connecting Signals and Slots
        # self.frame_ui.AxsSelector.currentIndexChanged.connect(lambda:self.frame_ui.ElementsSelector)
        # self.frame_ui.LineWidthSpin = self.findChild(QtWIdgets.QSpinBox, "LineWidthSpin")
        # self.frame_ui.LineWidthSpin.valueChanged.connect(lambda:self.change_line_sizes(self.LineWidthSpin.value))

    def update_fig(self, fig):
        self.fig = fig
        if not self.fig.axes:
            self.fig.add_subplot(1, 1, 1)
        if not self.fig.axes[0].collections:
            self.fig.axes[0].scatter([0, 1, 2], [0, 2, 4], label="test")
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
        current_ax_idx = self.frame_ui.AxsSelector.currentIndex()
        current_ax_ctn = self.axs[current_ax_idx]
        for i, collection in enumerate(current_ax_ctn["collections"]):
            self.frame_ui.ElementsSelector.addItem(collection, ["collection", i])
        for i, line in enumerate(current_ax_ctn["lines"]):
            self.frame_ui.ElementsSelector.addItem(line, ["line", i])

        current_element_idx = self.frame_ui.ElementsSelector.currentIndex()
        current_element_cat = self.frame_ui.ElementsSelector.itemData(current_element_idx)[0]
        current_element_num = self.frame_ui.ElementsSelector.itemData(current_element_idx)[1]

        if current_element_cat == "collection":
            current_collection = self.fig.axes[current_ax_idx].collections[current_element_num]
            collection_params = {"label": current_collection._label,
                                 "sizes": current_collection._sizes[0],
                                }
            self.open_scatter_settings(self, collection_params)
            #self.frame_ui.setup_ScatterSettingsUi(self)

        if current_element_cat == "line":
            current_line = self.fig.axes[current_ax_idx].lines[current_element_num]
            label = current_line._label
            linewidth = current_line._linewidth

    def open_scatter_settings(self, labe, sizes):
        self.scatter_ui = ScatterUi()
        self.scatter_ui.setupUi(self.frame_ui.Settings)


    def change_line_sizes(self, ax_num, line_num, width):
        _linewidth = width
        self.fig.axes[ax_num].lines[line_num]._linewidth = _width
        #self.edit_script()
        #self.execute_script()
