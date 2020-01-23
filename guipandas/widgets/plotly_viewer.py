import os, sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import plotly

instance_list = []

# If QtWebEngineWidgets is imported while a QApplication instance already exists it will fail, so we have to
try:
    from PyQt5 import QtWebEngineWidgets
except ImportError as e:
    if e.msg == "QtWebEngineWidgets must be imported before a QCoreApplication instance is created":
        print("Killing QApplication to reimport QtWebEngineWidgets")
        from PyQt5 import sip

        app = QApplication.instance()
        app.quit()
        sip.delete(app)
        del app
        from PyQt5 import QtWebEngineWidgets

        # Without remaking the QApplication you will get an unrecoverable crash on the next attempted usage of it
        app = QApplication([])
    else:
        raise e


class PlotlyViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, fig):
        # Create a QApplication instance or use the existing one if it exists
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

        super().__init__()

        # This ensures there is always a reference to this widget and it doesn't get garbage collected
        global instance_list
        instance_list.append(self)

        # self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp.html"))
        self.file_path = os.path.join(os.getcwd(), 'temp.html')
        self.setWindowTitle("Plotly Viewer")

        plotly.offline.plot(fig, filename=self.file_path, auto_open=False)
        self.load(QUrl.fromLocalFile(self.file_path))

        self.resize(640, 480)
        self.show()

    def closeEvent(self, event):
        os.remove(self.file_path)


def view(fig, block=False):
    pv = PlotlyViewer(fig)

    if block:
        pv.app.exec_()


if __name__ == "__main__":
    import numpy as np
    import plotly.graph_objs as go
    import plotly.offline
    from pandasgui.utility import fix_ipython

    fix_ipython()

    fig = go.Figure()
    fig.add_scatter(x=np.random.rand(100), y=np.random.rand(100), mode='markers',
                    marker={'size': 30, 'color': np.random.rand(100), 'opacity': 0.6,
                            'colorscale': 'Viridis'});

    view(fig)
