import matplotlib.pyplot as plt
import numpy as np
import rocket, planets

def plotter(x, y, kind='scatter', title=None, x_label=None, y_label=None):
	f, ax = plt.subplots(1, 1)
	if kind == 'scatter':
		ax.scatter(x, y)
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()