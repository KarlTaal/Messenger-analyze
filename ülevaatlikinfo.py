from abistajad import algus, lõpp

class ülevaatlikinfo:

    def __init__(self, nimed, sõnumid):
        self.names = nimed
        self.messages = sõnumid


    def anna_tekst(self, posstreak, negstreak):
        t = "Vestluses osalejad:\n"
        for n in self.names:
            t += n + "\n"

        t += "\n"

        t += "Vestluse algus: " + str(algus(self.messages)) + "\n"
        t += "Vestluse lõpp:  " + (str(lõpp(self.messages))) + "\n"

        t += "\n"

        t += "Pikim streak, kus räägiti iga päev: " + str(posstreak[2]) + "  Vahemikus: " + str(posstreak[0]) + " kuni " + str(posstreak[1]) + "\n"
        t += "Pikim streak, kus ei räägitud iga päev: " + str(abs(negstreak[2])) + "  Vahemikus: " + str(negstreak[0]) + " kuni " + str(negstreak[1]) + "\n"

        return t