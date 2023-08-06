import matplotlib.pyplot as plt
import matplotlib.cm
import matplotlib.colors
import pyquickmaps.pqm as pqm

def visualizeGrid(grid,min_lat,max_lat,min_lon,max_lon,title = False, xlabel = False, ylabel = False, cmap = 'magma',figsize=10):
	""" Uses matplotlib to show one grid."""

	fig, axs = plt.subplots(1,1,figsize=(figsize,figsize))

	visualizeGridInFigure(axs,grid,min_lat,max_lat,min_lon,max_lon,title,xlabel,ylabel,cmap)
	return fig,axs


def visualizeGrids(grids,min_lat,max_lat,min_lon,max_lon,titles = False, xlabel = False, ylabel = False, cmap = 'magma',figsize=10):
	""" Uses matplotlib to show several grids with synchronized extents."""

	if len(grids) == 1:
		return visualizeGrid(grids[0],min_lat,max_lat,min_lon,max_lon,titles,xlabel,ylabel,cmap,figsize)

	fig, axs = plt.subplots(1,len(grids),figsize=(figsize,figsize))
	for i,grid in enumerate(grids):
		title = False
		if titles != False:
			title = titles[i]
		visualizeGridInFigure(axs[i],grid,min_lat,max_lat,min_lon,max_lon,title,xlabel,ylabel,cmap)
		# TODO Sync color maps between figures

	return fig,axs


def visualizeGridInFigure(axs,grid,min_lat,max_lat,min_lon,max_lon,title = False, xlabel = False, ylabel = False, cmap = 'magma'):
	""" Visualizes a single grid in an existing matplotlib subplot """

	cmap = plt.get_cmap(cmap)

	axs.imshow(grid.T,extent=(min_lon,max_lon,min_lat,max_lat),cmap=cmap,origin='lower')

	if title != False:
		axs.title.set_text(title)
		axs.title.set_size(15)
	if xlabel != False:
		axs.set_xlabel(xlabel,fontsize=15)
	if ylabel != False:
		axs.set_ylabel(ylabel,fontsize=15)

	axs.set(adjustable='box', aspect='equal')
	axs.tick_params(labelleft=True,labelsize=12)
	axs.ticklabel_format(axis='both',style='plain',useOffset=False)


def visualizePoints(axs, lats, lons, vals, min_val = False, max_val = False, cmap = 'magma'):
	""" Visualizes point observations in an existing matplotlib subplot """

	cmap = matplotlib.cm.get_cmap(cmap)

	if min_val == False:
		min_val = min(vals)
	if max_val == False:
		max_val = max(vals)

	norm = matplotlib.colors.Normalize(vmin=min_val, vmax=max_val)

	cols = []
	for val in vals:
		cols.append(matplotlib.colors.to_hex(cmap(norm(val))))
	axs.scatter(lons, lats, c = cols,s=100,linewidth=2,edgecolors='w')


def comparePredictionGrids(lats,lons,vals,grid_method='nearest',kriging_method='spherical',title = False, xlabel = False, ylabel = False,cmap='magma',figsize=10):
	""" Calculates and visualizes two grids next to each other for comparison """

	# Compute grids
	grid_inter,min_lat,max_lat,min_lon,max_lon,min_val,max_val = pqm.interpolateobservationsToGrid(lats,lons,vals,500,500,grid_method)
	grid_krigi,conf_krigi,min_lat,max_lat,min_lon,max_lon,min_val,max_val = pqm.krigeObservationsToGrid(lats,lons,vals,500,500,kriging_method)

	grids = [grid_inter,grid_krigi]
	titles = False
	if title != False:
		titles = [title+"\n" + grid_method+" interpolation",title+"\n"+kriging_method+" kriging"]
	fig,axs = visualizeGrids(grids,min_lat,max_lat,min_lon,max_lon,titles, xlabel, ylabel, cmap,figsize)

	for i,ax in enumerate(axs):
		visualizePoints(ax, lats, lons, vals,cmap=cmap)
