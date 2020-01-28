from abistajad import parseString, save_df
import pandas as pd
class hüüdnimed:
    def __init__(self, nimed, omanik):
        self.aliased = {}
        self.omanik = omanik
        self.names = nimed
        for n in self.names:
            self.aliased[n] = []

    def uuenda(self, msg):
        # "set his own nickname to"
        # "set her own nickname to"
        # "set the nickname for"
        # "set your nickname to"  you võib ka olla
        try:
            sisu, emojis = parseString(msg["content"])
            if "set the nickname for" in sisu:
                ar = []
                e1 = sisu.split("set the nickname for")
                ar.append(e1[0].strip())
                e2 = e1[1].split("to")
                ar.append(e2[0].strip())
                ar.append(e2[1].strip())
                temp = self.aliased[ar[1]]
                temp.append(ar[2])
                self.aliased[ar[1]] = temp
                # print(sisu)
            if "set your nickname to" in sisu:
                ar = []
                e1 = sisu.split("set your nickname to")
                ar.append(e1[0].strip())
                ar.append(self.omanik)
                ar.append(e1[1].strip())
                temp = self.aliased[self.omanik]
                temp.append(ar[2])
                self.aliased[self.omanik] = temp
                # print(sisu)
            if "set his own nickname to" in sisu:
                ar = []
                e1 = sisu.split("set his own nickname to")
                ar.append(e1[0].strip())
                ar.append(e1[0].strip())
                ar.append(e1[1].strip())
                muudetav = ""
                for n in self.names:
                    v = n.split(" ")
                    v = v[:len(v) - 1]
                    v = " ".join(v)
                    if ar[1] == v:
                        muudetav = n
                        break
                temp = self.aliased[muudetav]
                temp.append(ar[2])
                self.aliased[muudetav] = temp
                # print(sisu)
            if "set her own nickname to" in sisu:
                ar = []
                e1 = sisu.split("set her own nickname to")
                ar.append(e1[0].strip())
                ar.append(e1[0].strip())
                ar.append(e1[1].strip())
                muudetav = ""
                for n in self.names:
                    v = n.split(" ")
                    v = v[:len(v) - 1]
                    v = " ".join(v)
                    if ar[1] == v:
                        muudetav = n
                        break
                temp = self.aliased[muudetav]
                temp.append(ar[2])
                self.aliased[muudetav] = temp
                # print(sisu)

        except:
            pass

    def vormista(self):
        aliasteDF = (pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.aliased.items()])))
        aliasteDF = aliasteDF.fillna("")
        if len(aliasteDF) != 0:
            save_df(aliasteDF, "Nicknames.png")