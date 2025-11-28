import pandas as pd
import time
import os

class SessionLogger:
    def __init__(self, filename="data/sessions.csv"):
        self.filename = filename

        if not os.path.exists("data"):
            os.mkdir("data")

        if not os.path.isfile(self.filename):
            df = pd.DataFrame(columns=["timestamp", "student", "subject", "trigger", "input", "output"])
            df.to_csv(self.filename, index=False)

    def log(self, student, subject, trigger, input_msg, output_msg):
        df = pd.read_csv(self.filename)
        df.loc[len(df)] = [time.time(), student, subject, trigger, input_msg, output_msg]
        df.to_csv(self.filename, index=False)
