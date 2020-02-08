# This Python file uses the following encoding: utf-8
import pickle

class ScriptExecutor():

    def __init__(self, script):
        self.interpreter = "default"
        self.script = script

    def execute_script(self, script):
        exec(script)
        with open("./figure.pkl", "wb") as f:
            pickle.dump(fig, f)

        self.script = script
        return fig

    def export_script(self):
        return self.script





