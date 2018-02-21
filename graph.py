#! /usr/bin/python
import pickle
import numpy as np
import matplotlib.pyplot as plt

def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        if height == 0:
            continue
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

with open("gitdm.dump", 'rb') as f:
    (versions, FE) = pickle.load(f)

ind = np.arange(len(versions))
bottom_c = [0] * len(versions)
bottom_s = bottom_c
bottom_cc = bottom_c
bottom_sc = bottom_c

lc = []
ll = []
colors = [
    'black',
    'dodgerblue',
    'gold',
    'slategray',
    'mediumseagreen',
    'mediumpurple',
    'mediumvioletred',
    'orangered',
    'sienna',
    'mediumturquoise',
    'darkorange',
    'lightgray',
    'seagreen',
    'b',
    'tan'
]

ci = 0
figt = plt.figure(figsize=(16,4))
axt1 = figt.add_subplot(1, 1, 1)
plt.xticks(ind, versions, rotation=70)
axt2 = axt1.twinx()
axt1.yaxis.grid(True)
axt1.spines['top'].set_visible(False)
axt2.spines['top'].set_visible(False)

for u in sorted(FE):
    commits = [FE[u][v][0] if v in FE[u] else 0 for v in versions]
    sob = [FE[u][v][1] if v in FE[u] else 0 for v in versions]

    commits_c = np.cumsum(commits)
    sob_c = np.cumsum(sob)

    width = 0.4

    fig = plt.figure(figsize=(16,4))
    plt.figure(fig.number)
    ax1 = fig.add_subplot(1, 1, 1)
    plt.xticks(ind, versions, rotation=70)
    offset = -width/2
    if sob_c[-1] > 0:
        offset = -width
    c = ax1.bar(ind + offset, commits, width, align='edge', color='orange')
    if sob_c[-1] > 0:
        s = ax1.bar(ind, sob, width, align='edge', color='dodgerblue')

    ax2 = ax1.twinx()
    lim = ax1.get_ylim()
    ratio = int(max(sob_c[-1], commits_c[-1])/(lim[1] * 10)) + 1
    lim = (lim[0], lim[1]*1.05)
    ax1.set_ylim(lim)
    lim = (lim[0], lim[1] * 10 * ratio)
    ax2.set_ylim(lim)
    cc = ax2.plot(commits_c, color='darkorange')
    if sob_c[-1] > 0:
        sc = ax2.plot(sob_c, color='blue')

    ax1.yaxis.grid(True)
    if sob_c[-1] > 0:
        ax1.legend([c, s], ['Commits', 'SoBs'], loc=2)
    else:
        ax1.legend([c], ['Commits'], loc=2)
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    off = 0
    if sob_c[-1] > 0 and abs(commits_c[-1] - sob_c[-1]) < 25:
        off = 10
    if commits_c[-1] < sob_c[-1]:
        off = -off

    plt.text(len(versions) - 0.5, commits_c[-1] + off, commits_c[-1])
    if sob_c[-1] > 0:
        plt.text(len(versions) - 0.5, sob_c[-1] - off, sob_c[-1])
    autolabel(c, ax1)
    if sob_c[-1] > 0:
        autolabel(s, ax1)

    #plt.title(u)

    fig.tight_layout()
    plt.savefig("%s.png"%(u), dpi=100)
    plt.close(fig)

    plt.figure(figt.number)
    ct = axt1.bar(ind - width, commits, width, align='edge', bottom=bottom_c, color=colors[ci])
    axt1.bar(ind, sob, width, align='edge', bottom=bottom_s, color=colors[ci])

    lc.append(ct[0])
    ll.append(u)
    ci = ci + 1
    bottom_c = map(lambda x,y:x+y, bottom_c, commits)
    bottom_s = map(lambda x,y:x+y, bottom_s, sob)
    bottom_cc = map(lambda x,y:x+y, bottom_cc, commits_c)
    bottom_sc = map(lambda x,y:x+y, bottom_sc, sob_c)

lim = axt1.get_ylim()
ratio = int(max(bottom_cc[-1], bottom_sc[-1])/(lim[1] * 10)) + 1
lim = (lim[0], lim[1]*1.05)
axt1.set_ylim(lim)
lim = (lim[0], lim[1]*10*ratio)
axt2.set_ylim(lim)
axt2.plot(bottom_cc, color='darkorange')
axt2.plot(bottom_sc, color='blue')
axt1.legend(lc, ll, loc=2, ncol=2)
off = 0
if bottom_sc[-1] > 0 and abs(bottom_cc[-1] - bottom_sc[-1]) < 25:
    off = 10
if bottom_cc[-1] < bottom_sc[-1]:
    off = -off
plt.text(len(versions) - 0.5, bottom_cc[-1] + off, bottom_cc[-1])
if sob_c[-1] > 0:
    plt.text(len(versions) - 0.5, bottom_sc[-1] - off, bottom_sc[-1])

figt.tight_layout()
plt.savefig("bootlin.png", dpi=100)
plt.close(figt)
