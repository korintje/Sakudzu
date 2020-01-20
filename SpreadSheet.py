from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pandas as pd

class SpreadSheet(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = "test_df"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 960
        self.test_data = [
                    ['2019-07-01 15:00:00','9997','740'],
                    ['2019-07-02 15:00:00','9997','749'],
                    ['2019-07-03 15:00:00','9997','757'],
                    ['2019-07-04 15:00:00','9997','769'],
                    ['2019-07-05 15:00:00','9997','762'],
                    ['2019-07-08 15:00:00','9997','760']
                ]
        self.test_df = pd.DataFrame(self.test_data)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table = DataTableView(self.test_df, parent=self)
        self.show()


class DataTableModel(QtCore.QAbstractTableModel):
    """
    Model for DataTableView to connect for DataFrame data
    """

    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.df = df

    def headerData(self, section, orientation, role=None):
        # Headers for DataTableView are hidden. Header data is shown in HeaderView
        pass

    def columnCount(self, parent=None):
        if type(self.df) == pd.Series:
            return 1
        else:
            return self.df.columns.shape[0]

    def rowCount(self, parent=None):
        return len(self.df)

    # Returns the data from the DataFrame
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


class DataTableView(QTableView):

    def __init__(self, df, parent):
        super().__init__(parent)
        self.parent = parent

        # Create and set model
        model = DataTableModel(df)
        self.setModel(model)

        # Hide the headers. The DataFrame headers (index & columns) will be displayed in the DataFrameHeaderViews
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        # Link selection to headers
        self.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        # Settings
        # self.setWordWrap(True)
        # self.resizeRowsToContents()
        self.setAlternatingRowColors(True)
        self.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

    def on_selectionChanged(self):
        """
        Runs when cells are selected in the main table. This logic highlights the correct cells in the vertical and
        horizontal headers when a data cell is selected
        """
        columnHeader = self.parent.columnHeader
        indexHeader = self.parent.indexHeader

        # The two blocks below check what columns or rows are selected in the data table and highlights the
        # corresponding ones in the two headers. The if statements check for focus on headers, because if the user
        # clicks a header that will auto-select all cells in that row or column which will trigger this function
        # and cause and infinite loop

        if not columnHeader.hasFocus():
            selection = self.selectionModel().selection()
            columnHeader.selectionModel().select(selection,
                                                 QItemSelectionModel.Columns | QItemSelectionModel.ClearAndSelect)

        if not indexHeader.hasFocus():
            selection = self.selectionModel().selection()
            indexHeader.selectionModel().select(selection,
                                                QItemSelectionModel.Rows | QItemSelectionModel.ClearAndSelect)

    def print(self):
        print(self.model().df)

    def copy(self):
        """
        Copy the selected cells to clipboard in an Excel-pasteable format
        """

        # Get the bounds using the top left and bottom right selected cells
        indexes = self.selectionModel().selection().indexes()

        rows = [ix.row() for ix in indexes]
        cols = [ix.column() for ix in indexes]

        df = self.model().df.iloc[min(rows):max(rows) + 1, min(cols):max(cols) + 1]

        # If I try to use Pyperclip without starting new thread large values give access denied error
        def thread_function(df):
            df.to_clipboard(index=False, header=False)

        threading.Thread(target=thread_function, args=(df,)).start()

        clipboard.setText(text)

    def paste(self):
        # Set up clipboard object
        app = QtWidgets.QApplication.instance()
        if not app:
            app = QtWidgets.QApplication(sys.argv)
        clipboard = app.clipboard()

        # TODO
        print(clipboard.text())

    def sizeHint(self):
        # Set width and height based on number of columns in model
        # Width
        width = 2 * self.frameWidth()  # Account for border & padding
        # width += self.verticalScrollBar().width()  # Dark theme has scrollbars always shown
        for i in range(self.model().columnCount()):
            width += self.columnWidth(i)

        # Height
        height = 2 * self.frameWidth()  # Account for border & padding
        # height += self.horizontalScrollBar().height()  # Dark theme has scrollbars always shown
        for i in range(self.model().rowCount()):
            height += self.rowHeight(i)

        return QSize(width, height)
