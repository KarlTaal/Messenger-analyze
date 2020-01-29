import emoji
import datetime
import numpy as np
import six
import matplotlib.pyplot as plt

# Teeb täpitähed nähtavaks.
def parseString(str):
    t = str.encode('latin1').decode('utf8')
    e = ""
    i = 0
    while i < (len(t)):
        if t[i] in emoji.UNICODE_EMOJI:
            e += t[i] + " "
            t = t[:i] + ' ' + t[i + 1:]
            i -= 1
        i += 1
    symbols = [
        ",", ".", ";", ":", "*", "'", "\"",
        "-", "_", "<", ">", "!", "@", "#",
        "£", "¤", "$", "%", "&", "/", "{", "}",
        "(", ")", "[", "]", "=", "?", "+", "´", "´´", "ˇ", "|"
    ]
    for sy in symbols:
        t = t.replace(sy, " ")
    return t.strip(), e.strip()


# Dictionary väärtuste summa.
def dictSum(myDict):
    sum = 0
    for i in myDict:
        sum = sum + myDict[i]
    return sum


def on_contenti(msg):
    try:
        c = msg["content"]

        return True
    except:
        return False


def plotLisa(largest):
    if largest < 10:
        return 2
    if largest < 100:
        return 20
    if largest < 10000:
        return largest * 0.1
    if largest < 15000:
        return largest * 0.2
    if largest < 35000:
        return largest * 0.2
    if largest < 70000:
        return largest * 0.15
    if largest < 100000:
        return largest * 0.08
    return round(largest * 0.14)


def kuupäev(ts):
    return datetime.datetime.fromtimestamp(ts / 1000.0).date()


def yearmonth(ts):
    kp = kuupäev(ts)
    return (str(kp.year) + str(kp.strftime('%h')))


def algus(messages):
    ts = messages[0]["timestamp_ms"]
    return kuupäev(ts)


def lõpp(messages):
    ts = messages[len(messages) - 1]["timestamp_ms"]
    return kuupäev(ts)


def save_df(data, filename, row_height=0.625, font_size=14,
            header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
            bbox=[0, 0, 1, 1], header_columns=0,
            ax=None, **kwargs):
    longest = 0
    for row in data.itertuples():
        for colname in data.columns:
            n = (data.at[row.Index, colname])
            if len(n) > longest:
                longest = len(n)
            if len(colname) > longest:
                longest = len(colname)

    tegur = 0.1715
    if longest < 5:
        tegur = 0.24
    if longest < 10:
        tegur = 0.2
    if longest < 31:
        tegur = 0.18

    col_width = longest * tegur
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    ax.get_figure().savefig("results\\plots\\" + filename)
    plt.close()


def kellaaeg(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1000.0).time()
