from msg_word_emoji_pertext_counts import msg_word_emoji_pertext
from messages_per_month import messages_per_month
from ülevaatlikinfo import ülevaatlikinfo
from hüüdnimed import hüüdnimed
from messages_count_per_hour import message_count_per_hour
from messages_count_over_time import message_count_over_time

def arvuta_progress(pr, bar):
    bar["value"] = int(pr * 100)
    bar.update()


def analyze(sõnumid, names, bar, tööinfo, omanik):
    progresscontrol = []
    for i in range(2, 102, 2):
        progresscontrol.append(i / 100)


    tekster = ülevaatlikinfo(names, sõnumid)
    w1 = msg_word_emoji_pertext(names)
    w2 = messages_per_month(names, sõnumid)
    w3 = hüüdnimed(names, omanik)
    w4 = message_count_per_hour()
    w5 = message_count_over_time()


    i = 0
    while i < len(sõnumid):
        ########################################Progress calculation.
        pr_ctr = round(i / (len(sõnumid) - 1), 2)
        if pr_ctr in progresscontrol:
            arvuta_progress(i / len(sõnumid), bar)
            progresscontrol.remove(pr_ctr)
        #######################################Workers
        w1.uuenda(sõnumid[i])
        w2.uuenda(sõnumid[i], i)
        w3.uuenda(sõnumid[i])
        w4.uuenda(sõnumid[i])
        w5.uuenda(sõnumid[i])

        i += 1

    tööinfo.config(text="Joonistan graafikuid, kohe on valmis...")
    tööinfo.update()

    w1.vormista()
    posstreak, negstreak = w2.vormista()
    tekst = tekster.anna_tekst(posstreak, negstreak)
    w3.vormista()
    w4.vormista()
    w5.vormista()

    return tekst