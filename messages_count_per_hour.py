import pandas as pd
from abistajad import kellaaeg
import datetime
import matplotlib.pyplot as plt

class message_count_per_hour:
    def __init__(self):
        self.hours = {}
        for i in range(24):
            self.hours[i] = 0

    def uuenda(self, msg):
        stamp = msg["timestamp_ms"]
        clock = kellaaeg(stamp)

        for i in range(24):
            if i != 23:
                if datetime.time(i) <= clock < datetime.time(i + 1):
                    temp = self.hours[i]
                    temp += 1
                    self.hours[i] = temp
                    break
            else:
                temp = self.hours[23]
                temp += 1
                self.hours[23] = temp
                break

    def vormista(self):
        df = pd.DataFrame.from_dict(self.hours, 'index').stack().reset_index(level=0)
        df.columns = ['', 's']
        df.plot(figsize=(15, 10), kind='bar', y=df.columns[1], x=df.columns[0], color='blue', legend=False, width=0.7,
                title="Messages count per hour")
        plt.savefig("results\\plots\\" + "Messages count per hour.png")
        plt.close()