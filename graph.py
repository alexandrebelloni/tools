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
	commits_c = np.cumsum(commits)
	sob_c = np.cumsum(sob)

	ind = np.arange(len(versions))
	width = 0.4

	fig, ax1 = plt.subplots()
	plt.xticks(ind, versions, rotation=70)
	offset = -width/2
	if sob_c[-1] > 0:
		offset = -width
	c = ax1.bar(ind + offset, commits, width, align='edge', color='orange')
	if sob_c[-1] > 0:
		s = ax1.bar(ind, sob, width, align='edge', color='dodgerblue')

	ax2 = ax1.twinx()
	lim = ax1.get_ylim()
	lim = (lim[0], lim[1]*1.05)
	ax1.set_ylim(lim)
	lim = (lim[0], lim[1]*10)
	ax2.set_ylim(lim)
	cc = ax2.plot(commits_c, color='darkorange')
	if sob_c[-1] > 0:
		sc = ax2.plot(sob_c, color='blue')

	ax1.yaxis.grid(True)
	ax1.legend((c[0], s[0]), ('Commits', 'SoBs'), loc=2)
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

	fig.set_size_inches(16,4)
	fig.tight_layout()
	plt.savefig("%s.png"%(u), dpi=100)
	plt.close(fig)
