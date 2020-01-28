from abistajad import yearmonth, algus, kuupäev, parseString
import pandas as pd
import matplotlib.pyplot as plt
import copy

class messages_per_month:
    def __init__(self, nimed, messages):
        self.kuupäevad = []
        self.kuulõikes = []
        self.kuu = {}

        self.eelminedt = ""
        self.eelmine = ""
        self.streak = 1
        self.suurim = 0
        self.per = {}

        self.per2 = {}
        self.suurimneg = 0

        self.iterationnr = 0

        self.pikkus = len(messages)
        self.names = nimed
        self.abi = algus(messages)
        self.algus1 = algus(messages)
        self.eelmiseitneg = algus(messages)
        self.algus2 = algus(messages)
        for msg in messages:
            ts = msg["timestamp_ms"]
            if yearmonth(ts) not in self.kuupäevad:
                self.kuupäevad.append(yearmonth(ts))
        for name in self.names:
            self.kuu[name] = 0

    def uuenda(self, msg, iterat):
        dt = kuupäev(msg["timestamp_ms"])
        sender, k = parseString(msg["sender_name"])

        # suurima positiivse streak
        if ((self.abi - dt).days == -1):
            self.streak += 1
        if ((self.abi - dt).days < -1):
            self.per[self.streak] = [self.algus1, self.eelminedt]
            self.streak = 1
            self.algus1 = dt
        if (self.suurim < self.streak):
            self.suurim = self.streak

        # suurimn negatiivne streak
        if (self.eelmiseitneg - dt).days == -1 or (self.eelmiseitneg - dt).days == 0:  # kui eelmisene on järgnev kohe
            self.algus2 = dt
        elif (self.algus2 - dt).days < self.suurimneg:
            self.suurimneg = (self.algus2 - dt).days
            self.per2[self.suurimneg] = [self.algus2, dt]
        self.eelmiseitneg = dt

        self.abi = dt
        kp = yearmonth(msg["timestamp_ms"])
        if self.eelmine != kp:
            if self.eelmine != "":
                self.kuulõikes.append(copy.deepcopy(self.kuu))
                for key in self.kuu:
                    self.kuu[key] = 0
            self.eelmine = kp
            self.eelminedt = dt
        c = self.kuu[sender]
        c += 1
        self.kuu[sender] = c
        if iterat + 1 == self.pikkus:
            self.kuulõikes.append(copy.deepcopy(self.kuu))

    def vormista(self):
        x = []
        subheigth = len(self.names) * 3
        df = pd.DataFrame(self.kuulõikes)
        df["date"] = self.kuupäevad
        df = df.iloc[1:]
        df = df.iloc[:len(df["date"]) - 1]

        for i in range(len(self.kuupäevad)):
            x.append(i)

        if len(self.names) % 2 == 0:
            nrow = int(len(self.names) / 2)
        else:
            nrow = int(len(self.names) / 2) + 1

        ncol = 2
        count = 0
        if len(self.names) > 2:
            fig, axes = plt.subplots(nrow, ncol, figsize=(24, subheigth), sharey=True)
            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
            for r in range(nrow):
                for c in range(ncol):
                    new = df[["date", self.names[count]]].copy()
                    new.plot(ax=axes[r, c], legend=False, title="Messages per month: " + self.names[count],
                             xticks=range(0, len(df["date"])))
                    axes[r][c].set_xticklabels(self.kuupäevad, fontdict=None, minor=False, rotation=90)
                    axes[r][c].title.set_size(20)
                    count += 1
                    if count == len(self.names):
                        break
                if count == len(self.names):
                    break
        plt.savefig("results\\plots\\" + "Messages per month separetely.png")
        plt.close()
        df.plot(figsize=(20, 10), xticks=range(0, len(df["date"]))).legend(title='Names', bbox_to_anchor=(1, 1))
        plt.xticks(x, self.kuupäevad, rotation=70)
        plt.title("Messages per month", fontsize=25)
        plt.legend(prop={'size': 20})
        plt.savefig("results\\plots\\" + "Messages per month.png")
        plt.close()

        algusss = self.per[self.suurim][0]
        lõpppp = self.per[self.suurim][1]
        posstreak = [algusss, lõpppp, self.suurim]

        algusss2 = self.per2[self.suurimneg][0]
        lõpppp2 = self.per2[self.suurimneg][1]
        negstreak = [algusss2, lõpppp2, self.suurimneg]

        return posstreak, negstreak