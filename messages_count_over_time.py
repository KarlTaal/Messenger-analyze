from abistajad import yearmonth
import pandas as pd
import matplotlib.pyplot as plt

class message_count_over_time:
    def __init__(self):
        self.kuud = {}
        self.kuupäevad = []

    def uuenda(self, msg):
        kuu = yearmonth(msg["timestamp_ms"])
        if kuu in self.kuud:
            temp = self.kuud[kuu]
            temp += 1
            self.kuud[kuu] = temp
        else:
            self.kuud[kuu] = 1
            self.kuupäevad.append(kuu)

    def vormista(self):
        x = []
        for i in range(len(self.kuupäevad)):
            x.append(i)
        df = pd.DataFrame.from_dict(self.kuud, 'index').stack().reset_index(level=0)
        df.columns = ['', 's']
        df.plot(figsize=(15, 10), kind='line', y=df.columns[1], x=df.columns[0], color='blue', legend=False,
                title="Messages count over time")
        plt.xticks(x, self.kuupäevad, rotation=70)
        plt.savefig("results\\plots\\" + "Messages count over time.png")
        plt.close()