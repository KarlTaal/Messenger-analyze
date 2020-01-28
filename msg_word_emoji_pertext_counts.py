from abistajad import parseString, on_contenti, plotLisa, dictSum
import pandas as pd
import matplotlib.pyplot as plt

class msg_word_emoji_pertext:
    def __init__(self, nimed):
        self.names_messagecount = {}
        self.names_wordcount = {}
        self.names_emojicount = {}
        self.names_contentmsgcount = {}  # sõnumite arv, kus oli tekstilist sisu
        self.names = nimed
        for n in self.names:
            self.names_messagecount[n] = 0
            self.names_wordcount[n] = 0
            self.names_emojicount[n] = 0
            self.names_contentmsgcount[n] = 0


    def uuenda(self, msg):
        sender, k = parseString(msg["sender_name"])
        c = self.names_messagecount[sender]
        c += 1
        self.names_messagecount[sender] = c

        if on_contenti(msg):
            con, emojis = parseString(msg["content"])

            c2 = self.names_wordcount[sender]
            c2 += len(con.split())
            self.names_wordcount[sender] = c2

            c3 = self.names_emojicount[sender]
            c3 += len(emojis.split())
            self.names_emojicount[sender] = c3

            if len(con.split()) != 0:
                c4 = self.names_contentmsgcount[sender]
                c4 += 1
                self.names_contentmsgcount[sender] = c4

    def vormista(self):
        plotHeigth = len(self.names)
        titles = ["Message count", "Word count", "Emoji count"]
        dicts = [self.names_messagecount, self.names_wordcount, self.names_emojicount]
        for title, dic in zip(titles, dicts):
            df = pd.DataFrame(list(dic.items()), columns=['', 'xd'])
            y = list(dic.values())
            y.sort()
            ax = df.sort_values('xd', ascending=True).plot(kind='barh',
                                                           title=title + ", sum is " + str(dictSum(dic)),
                                                           x='',
                                                           y='xd', legend=False, figsize=(13, plotHeigth), color="y")
            for i, v in enumerate(y):
                ax.text(v + 10, i, str(v), color='red', fontweight='bold')
            ax.set_xlim(0, y[len(y) - 1] + plotLisa(y[len(y) - 1]))
            plt.savefig("results\\plots\\" + title + ".png")
            plt.close()

        ###########################    Words per text message
        names_wordratiopermsg = {}
        for key in self.names_contentmsgcount:
            names_wordratiopermsg[key] = round(self.names_wordcount[key] / self.names_contentmsgcount[key], 2)
        df = pd.DataFrame(list(names_wordratiopermsg.items()), columns=['', 'ratio'])
        y = list(names_wordratiopermsg.values())
        y.sort()
        ax = df.sort_values('ratio', ascending=True).plot(kind='barh', title="Words per text message", x='', y='ratio',
                                                          legend=False, figsize=(13, plotHeigth), color="y")
        for i, v in enumerate(y):
            ax.text(v, i, str(v), color='red', fontweight='bold')
        ax.set_xlim(0, y[len(y) - 1] + plotLisa(y[len(y) - 1]))
        plt.savefig("results\\plots\\" + "Words per text message.png")
        plt.close()

