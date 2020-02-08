# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets

import matplotlib.pyplot as plt

class SakudzuCore():
    def __init__(self):
        self.code = ""
        self.const_code = ConstCode()
        self.dataframe_code = DFCode()
        self.matplotlib_code = MPLCode()

class ConstCode():
    def __init__(self):
        self.code = ""
        self.const_dict = {}
    #def temp_save(self):

class DFCode():
    def __init__(self):
        self.code = ""
        self.dataframe_dict = {}
    #def temp_save(self):


class MPLModel():
    def __init__(self):
        self.fig = mpl.figure()


"""
class MPLCode():
    def __init__(self):
        self.code = ""
        self.prefix = ["fig = plt.figure()"]
        self.sentences = []
        self.axs_dict = {}
        self.plots_dict = {}
        self.scatter_list = []

    def add_scatter_plot(self, scatter_name, ax_name, x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, edgecolors=None, plotnonfinite=False, data=None):
        self.plots_dict[scatter_name] = ScatterPlot(ax_name, x, y, s, c, marker, cmap, norm, vmin, vmax, alpha, linewidths, verts, edgecolors, plotnonfinite, data)

    def create_code(self, axs_dict, plots_dict, layout=[1,1]):
        self.sentences = []
        self.sentences += self.prefix
        for ax in axs_dict.keys():
            self.sentences.append("{ax_name} = fig.add_subplot({row}, {column}, {num}).".format(ax_name=ax, row=layout[0], column=layout[1], num=axs_dict[num]))
        for plot in plots_dict.keys():
            if plot.kind == "scatter":
                sentence = "{plot_name} = {ax_name}.scatter({x}, {y}, {options})".format(plot_name=plot, ax_name=plot.ax_name, x=plot.x, y=plot.y)
                for k, v in plot.options_dict.items():
                    if v != None:
                        sentence += "{key_name} = {key_value}".format(key_name=k, key_value=v)
                self.sentences.append(sentence)
        self.code = "\n".join(self.sentences)
"""


"""
class ScatterPlot():
    def __init__(self, kind, ax_name, x, y, s, c, marker, cmap, norm, vmin, vmax, alpha, linewidths, edgecolors, plotnonfinite, data):
        self.kind = "scatter"
        self.ax_name = ax_name
        self.x = x
        self.y = y
        self.s = s
        self.c = c
        self.marker = marker
        self.cmap = cmap
        self.norm = norm
        self.vmin = vmin
        self.vmax = vmax
        self.alpha = alpha
        self.linewidths = linewidths
        self.edgecolors = edgecolors
        self.plotnonfinite = plotnonfinite
        self.data = data
        self.options_dict = {"x": x, "c": c, "marker": marker, "cmap": cmap, "norm": norm, "vmin": vmin, "vmax": vmax, "alpha": alpha, "linewidths": linewidths, "edgecolors": edgecolors, "plotnonfinite": plotnonfinite, "data": data}
"""
