import matplotlib
import matplotlib.pyplot as plt

import figplotter

from figplotter.utils import Parameter as P
from figplotter.plot import figure, bar_series, line_series

fig = figure()
ax = fig.add_subplot(111)

line_series(ax,
            { 'Read':  [1, 2,   4,    5],
              'Write': [2, 3, 3.5, 3.75] })

fig.show()

fig2 = figure()
ax2 = fig2.add_subplot(111)

bar_series(ax2,
           { 'Read' : [1, 2,   4,    5],
             'Write': [2, 3, 3.5, 3.75] },
           plot_params = {
               'color' : P({ 'Read' : 'b',
                             'Write': 'g'})
           })

fig2.show()

plt.show()
