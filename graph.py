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

with open("gitdm.dump", 'r') as f:
	(versions, FE) = pickle.load(f)

for u in sorted(FE):
	commits = [FE[u][v][0] if v in FE[u] else 0 for v in versions]
	sob = [FE[u][v][1] if v in FE[u] else 0 for v in versions]

	ind = np.arange(len(versions))
	width = 0.2

	fig, ax1 = plt.subplots()
	c = ax1.bar(ind - width/2, commits, width, color='darkorange')
	s = ax1.bar(ind + width/2, sob, width, color='dodgerblue')

	ax2 = ax1.twinx()
	lim = ax1.get_ylim()
	lim = (lim[0], lim[1]*1.05)
	ax1.set_ylim(lim)
	lim = (lim[0], lim[1]*10)
	ax2.set_ylim(lim)
	cc = ax2.plot(np.cumsum(commits), color='darkorange')
	sc = ax2.plot(np.cumsum(sob), color='dodgerblue')

	ax1.yaxis.grid(True)
	ax1.set_xticks(ind)
	ax1.set_xticklabels(versions)
	ax1.legend((c[0], s[0]), ('commits', 'sobs'), loc=2)
	ax1.spines['top'].set_visible(False)
	ax2.spines['top'].set_visible(False)

	autolabel(c, ax1)
	autolabel(s, ax1)
	#autolabel(cc, ax2)
	#autolabel(sc, ax2)

	#plt.title(u)

	fig.set_size_inches(16,4)
	fig.tight_layout()
	plt.savefig("%s.png"%(u), dpi=100)
	#plt.show()
	plt.close(fig)
