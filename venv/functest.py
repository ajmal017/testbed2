from vix_etf_stats_compares import *

wins = [30, 45, 60, 75, 90, 105, 120]
lils = [15]
t = 'vixy'
ctl = 0.8
lengencies = []
ctlylist = [ctl] * 200
ctlymin = 10
ctlymax = -1
for w in wins:
    for l in lils:
        adjclist = rangefuncMin(t, w, lmax=l)
        hist, bins = cumcovert(adjclist)
        if ctlymin > min(bins):
            ctlymin = min(bins)
        if ctlymax < max(bins):
            ctlymax = max(bins)
        lg = ''
        lengencies.append(lg)
        label = 'Win = ' + str(w) + ', VIX < ' + str(l)
        lengencies[-1], = plt.plot(bins, hist, label=label)
ctlxlist = list(np.linspace(ctlymin, ctlymax, 200))
plt.plot(ctlxlist, ctlylist, c='black', lw=2)
plt.title('RangeMinValues: ' + t.upper())
plt.legend()
plt.tight_layout()
plt.grid()
plt.show()