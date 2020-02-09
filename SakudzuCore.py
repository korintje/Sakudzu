# This Python file uses the following encoding: utf-8

from PyQt5 import QtCore
import matplotlib.pyplot as plt
import pandas as pd


class Model():

    def __init__(self):
        self.consts = []
        self.dataframes = []
        self.figures = []

    def add_const(self):
        const = {}
        self.consts.append(const)

    def add_dataframe(self):
        dataframe = DataFrameModel()
        self.dataframes.append(dataframe)

    def add_figure(self):
        fig = plt.figure()
        self.figures.append(fig)


class DataFrameModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = pd.DataFrame()

    def headerData(self, rowcol, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole: return self.df.columns[rowcol] if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self.df.index[rowcol]
        else:
            return None

    def columnCount(self, parent=None):
        return self.df.columns.size

    def rowCount(self, parent=None):
        return len(self.df)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole or role == QtCore.Qt.ToolTipRole:
            row = index.row()
            col = index.column()
            cell = self.df.iloc[row, col]

            # NaN case
            if pd.isnull(cell):
                return ""

            # Float formatting
            if isinstance(cell, (float, np.floating)):
                if not role == QtCore.Qt.ToolTipRole:
                    return "{:.4f}".format(cell)

            return str(cell)

        elif role == QtCore.Qt.ToolTipRole:
            row = index.row()
            col = index.column()
            cell = self.df.iloc[row, col]

            # NaN case
            if pd.isnull(cell):
                return "NaN"

            return str(cell)

    def flags(self, index):
        # Set the table to be editable
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # Set data in the DataFrame. Required if table is editable
    def setData(self, index, value, role=None):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            try:
                self.df.iat[row, col] = value
            except Exception as e:
                print(e)
                return False
            self.dataChanged.emit(index, index)

            return True
"""
class HeaderModel(QtCore.QAbstractTableModel):

    def __init__(self, df, orientation, parent=None):
        super().__init__(parent)
        self.df = df
        self.orientation = orientation

    def columnCount(self, parent=None):
        if self.orientation == Qt.Horizontal:
            return self.df.columns.shape[0]
        else:  # Vertical
            return self.df.index.nlevels

    def rowCount(self, parent=None):
        if self.orientation == Qt.Horizontal:
            return self.df.columns.nlevels
        elif self.orientation == Qt.Vertical:
            return self.df.index.shape[0]

    def data(self, index, role=None):
        row = index.row()
        col = index.column()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.ToolTipRole:

            if self.orientation == Qt.Horizontal:

                if type(self.df.columns) == pd.MultiIndex:
                    return str(self.df.columns.values[col][row])
                else:
                    return str(self.df.columns.values[col])

            elif self.orientation == Qt.Vertical:

                if type(self.df.index) == pd.MultiIndex:
                    return str(self.df.index.values[row][col])
                else:
                    return str(self.df.index.values[row])

    # The headers of this table will show the level names of the MultiIndex
    def headerData(self, section, orientation, role=None):
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole]:

            if self.orientation == Qt.Horizontal and orientation == Qt.Vertical:
                if type(self.df.columns) == pd.MultiIndex:
                    return str(self.df.columns.names[section])
                else:
                    return str(self.df.columns.name)
            elif self.orientation == Qt.Vertical and orientation == Qt.Horizontal:
                if type(self.df.index) == pd.MultiIndex:
                    return str(self.df.index.names[section])
                else:
                    return str(self.df.index.name)
            else:
                return None  # These cells should be hidden anyways

"""
