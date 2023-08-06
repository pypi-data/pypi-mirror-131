import os.path

import numpy
from scipy.interpolate import griddata
from sklearn.ensemble import RandomForestRegressor
from pykrige.uk import UniversalKriging

from osgeo import osr
from osgeo import gdal
from osgeo import gdal_array

import rasterio

def minMaxLatLon(lats,lons):
	""" Picks the minimum and maximum values from the two given latitude and longitude arrays"""

	return min(lats),max(lats),min(lons),max(lons)


def minMaxGridResults(results:dict):
	""" Returns the min/max lat/lon/val values from all results in the list"""
	lats = []
	lons = []
	vals = []
	for res in results:
		lats.append(results[res].min_lat)
		lats.append(results[res].max_lat)
		lons.append(results[res].min_lon)
		lons.append(results[res].max_lon)
		vals.append(results[res].min_val)
		vals.append(results[res].max_val)
	return min(lats),max(lats),min(lons),max(lons),min(vals),max(vals)


class Observation:
	""" A class with a latitude and longitude position and an observation value"""

	def __init__(self,lat,lon,val):
		self.lat = lat
		self.lon = lon
		self.val = val


class Observations:
	""" A list of observations"""

	def __init__(self,observations:list = []):
		self.observations = []
		self.lats = []
		self.lons = []
		self.vals = []
		for o in observations:
			if isinstance(o,Observation):
				self.append(o)
			elif isinstance(o,list) and len(o) == 3:
				self.append(Observation(o[0],o[1],o[2]))
			elif isinstance(o,dict) and len(o) == 3:
				self.append(Observation(o['lat'],o['lon'],o['val']))

	def append(self,o):
		self.observations.append(o)
		self.lats.append(o.lat)
		self.lons.append(o.lon)
		self.vals.append(o.val)


class GridResult:
	""" A class that is build around a grid and helps by providing the extent by min/max lat/lon and min/max values """
	def __init__(self,grid,min_lat,max_lat,min_lon,max_lon):

		self.grid = grid
		self.min_val = numpy.min(grid)
		self.max_val = numpy.max(grid)
		self.min_lat = min_lat
		self.max_lat = max_lat
		self.min_lon = min_lon
		self.max_lon = max_lon


class GridCoordinate:
	""" A class to manage coordinates within a grid. Can transform between EPSG4326 and the grids coordinate system """
	def __init__(self,dataset):

		src_ref = osr.SpatialReference()
		src_ref.ImportFromWkt(dataset.GetProjectionRef())

		dst_ref = osr.SpatialReference()
		dst_ref.ImportFromEPSG(4326)

		self.t = osr.CoordinateTransformation(src_ref, dst_ref)
		self.w = dataset.RasterXSize
		self.h = dataset.RasterYSize
		self.g = dataset.GetGeoTransform()

		self.tl = self.toLatLon(self.g[3],self.g[0])
		self.br = self.toLatLon(self.g[3]+self.g[5]*self.h,self.g[0]+self.g[1]*self.w)

		self.pxw = (self.br['lon'] - self.tl['lon']) / self.w
		self.pxh = (self.br['lat'] - self.tl['lat']) / self.h

	def toLatLon(self,y,x):
		p = self.t.TransformPoint(x,y)
		return {'lon':p[1],'lat':p[0]}

	def toXY(self,lat,lon):
		if lon < self.tl['lon'] or lon >= self.br['lon'] or lat > self.tl['lat'] or lat <= self.br['lat']:
			print("Position is outside grid",lon,self.tl['lon'],self.br['lon'],lat,self.tl['lat'],self.br['lat'])
			return None,None

		x = round((lon - self.tl['lon']) / self.pxw)
		y = round((lat - self.tl['lat']) / self.pxh)

		return x,y


def selectTrainingSamples(layers,coord,obs):
	""" Pick values (aka feature vectors) from grid layers at the given lat lon coordinates """

	Xs = []
	ys = []
	for i,lat in enumerate(obs.lats):
		x,y = coord.toXY(lat,obs.lons[i])
		vec = numpy.zeros(len(layers))
		for j,l in enumerate(layers):
			vec[j] = layers[l][y][x]
		if numpy.nan in vec or numpy.inf in vec:
#			print(x,y,lat,lons[i],vec,vals[i])
			continue
		Xs.append(vec)
		ys.append(obs.vals[i])

	return Xs,ys


def loadGridAsGDALDataset(path):
	""" Does what the name says"""

	if not os.path.exists(path):
		print("ERROR: Path ",path,"not found")
		return
	return gdal.Open(path, gdal.GA_ReadOnly)


def GDALDatasetToNumpyImage(dataset):
	""" Does what the name says"""

	# Allocate our array using the first band's datatype
	image_datatype = dataset.GetRasterBand(1).DataType

	image = numpy.zeros((dataset.RasterYSize, dataset.RasterXSize, dataset.RasterCount),
				 dtype=gdal_array.GDALTypeCodeToNumericTypeCode(image_datatype))

	# Loop over all bands in dataset
	for b in range(dataset.RasterCount):
		# Remember, GDAL index is on 1, but Python is on 0 -- so we add 1 for our GDAL calls
		band = dataset.GetRasterBand(b + 1)

		# Read in the band's data into the third dimension of our array
		image[:, :, b] = band.ReadAsArray()

	image[image == -9999] = None
	return image.astype(numpy.float64)


def GDALTerrainAnalysis(dataset,method):
	""" Just a convenience wrapper around gdal.DEMProcessing to compute a derivative from a DEM"""
	return gdal.DEMProcessing('', dataset, method, format='MEM')


def GDALTerrainAnalysisLayers(dataset, layers = ["dem","slope", "aspect", "TRI", "TPI", "Roughness"]):
	"""Uses GDAL to compute up to eight terrain variable layers from the grid file at the given path"""

	# Run terrain analysis
	ret = {}
	for l in layers:
		if l == "dem":
			ret[l] = GDALDatasetToNumpyImage(dataset)
		else:
			tmp = GDALTerrainAnalysis(dataset, l)
			ret[l] = GDALDatasetToNumpyImage(tmp)

	return ret


def interpolateObservationsToGrid(obs,gridx=500,gridy=500,method='nearest',spatial_buffer = 0.1):
	""" Compute a dense grid from observations with interpolation. Uses scipy.interpolyte.griddata """

	min_lat,max_lat,min_lon,max_lon = minMaxLatLon(obs.lats,obs.lons)
	off_lat = spatial_buffer * (max_lat - min_lat)
	off_lon = spatial_buffer * (max_lon - min_lon)

	points = numpy.vstack((obs.lons,obs.lats)).T

	grid_lon, grid_lat = numpy.mgrid[min_lon-off_lon:max_lon+off_lon:complex(gridx,0), min_lat-off_lat:max_lat+off_lat:complex(gridy,0)]
	grid = griddata(points, obs.vals, (grid_lon, grid_lat), method=method)

	return GridResult(grid.T,min_lat-off_lat,max_lat+off_lat,min_lon-off_lon,max_lon+off_lon)


def krigeObservationsToGrid(obs,gridx=500,gridy=500,method='power',spatial_buffer = 0.1):
	""" Compute a dense grid with Kriging. Uses pykrige.UniversalKriging"""

	min_lat,max_lat,min_lon,max_lon = minMaxLatLon(obs.lats,obs.lons)
	off_lat = spatial_buffer * (max_lat - min_lat)
	off_lon = spatial_buffer * (max_lon - min_lon)

	grid_lon = numpy.arange(min_lon-off_lon, max_lon+off_lon, (max_lon-min_lon+2*off_lon)/gridx)
	grid_lat = numpy.arange(min_lat-off_lat, max_lat+off_lat, (max_lat-min_lat+2*off_lat)/gridy)

	UK2 = UniversalKriging(obs.lons,obs.lats,obs.vals,variogram_model=method)
	# drift_terms=["regional_linear"],
	# coordinates_type="geographic"
	# linear, power, gaussian, spherical, exponential, hole-effect

	grid, confidence = UK2.execute("grid", grid_lon, grid_lat)

	return GridResult(grid,min_lat-off_lat,max_lat+off_lat,min_lon-off_lon,max_lon+off_lon)


def predictObservationsToGrid(obs,dataset):
	""" Computes a dense grid with a RandomForest regression. Uses sklearn.ensemble.RandomForestRegressor """

	# Compute derivatives
	layers = GDALTerrainAnalysisLayers(dataset)

	# Get coordinate transformation object
	coord = GridCoordinate(dataset)

	# Extract training samples
	Xs,ys = selectTrainingSamples(layers,coord,obs)

	# Train the random forest regressor
	clf = trainClassifier(Xs,ys)

	# Apply the classifier to the grid and return the result
	grid = applyClassifierToGrid(layers,clf)

	return GridResult(grid,coord.br['lat'],coord.tl['lat'],coord.tl['lon'],coord.br['lon'])


def trainClassifier(Xs,ys):
	""" Trains a RandomForest classifier on the given training data """

	# Train RF regression
	clf = RandomForestRegressor()
	clf.fit(Xs, ys)

	# Output regression quality
	s = clf.score(Xs,ys)
	print("RF regression score:",round(s,2),"(=R^2)")

	return clf


def applyClassifierToGrid(layers,clf):
	""" Takes a grid and a trained classifier to execute the prediction for the entire grid """

	for l in layers:
		h,w,z = layers[l].shape
		break

	# Get all valid data vectors and their positions
	vecs = []
	xys = []

	for y in range(h):
		for x in range(w):
			vec = numpy.zeros(len(layers))
			nope = False
			for i,l in enumerate(layers):
				if layers[l][y][x] == None or numpy.isnan(layers[l][y][x]):
					nope = True
					break
				vec[i] = layers[l][y][x]
			if not nope:
				vecs.append(vec)
				xys.append([x,y])

	# Run the prediction
	tmp = clf.predict(vecs)

	# Store the prediction results in a 2D array = image
	img = numpy.zeros((h,w))
	img[:] = numpy.nan
	for i,v in enumerate(tmp):
		img[h-xys[i][1],xys[i][0]] = v

	return img


def visualizeResults(results:dict,obs:Observations,figsize=10,cmap='magma'):

	import matplotlib.pyplot as plt
	import matplotlib.cm
	import matplotlib.colors

	# Get absolut min/max lat/lon of all grids
	min_lat,max_lat,min_lon,max_lon,min_val,max_val = minMaxGridResults(results)

	# Get color map and colors for observation values
	cmap = matplotlib.cm.get_cmap(cmap)
	norm = matplotlib.colors.Normalize(vmin=min_val, vmax=max_val)
	cols = []
	for val in obs.vals:
		cols.append(matplotlib.colors.to_hex(cmap(norm(val))))

	fig, axs = plt.subplots(1,len(results),figsize=(figsize,figsize))
	for i,title in enumerate(results):

		res = results[title]

		axs[i].set_xlim([min_lon,max_lon])
		axs[i].set_ylim([min_lat,max_lat])

		axs[i].imshow(res.grid,extent=(res.min_lon,res.max_lon,res.min_lat,res.max_lat),vmin=min_val,vmax=max_val,cmap=cmap,origin='lower')

		axs[i].title.set_text(title)
		axs[i].title.set_size(15)

		axs[i].set(adjustable='box', aspect='equal')
		axs[i].tick_params(labelleft=True,labelsize=12)
		axs[i].ticklabel_format(axis='both',style='plain',useOffset=False)

		axs[i].scatter(obs.lons,obs.lats,c=cols,s=100,linewidth=2,edgecolors='w')

	return fig,axs


def writeResults(path:dict,name:str,results:list):
	""" Writes several result grids to separate geotiffs ath the given path an names the files name_title.tif."""

	for i,title in enumerate(results):
		res = results[title]
		file_name = path + "/" + name + "_" + title + ".tif"
		writeGridLatLon(file_name,res.grid,res.min_lat,res.max_lat,res.min_lon,res.max_lon)


def writeGridLatLon(path,grid,min_lat,max_lat,min_lon,max_lon):
	""" Takes a dense grid of values and its real-world lat/lon coordinates and stores them as a GeoTiff on disk."""

	# Determine the size of one pixel in lat & lon direction
	px_size_lon = (max_lon - min_lon) / grid.shape[0]
	px_size_lat = (max_lat - min_lat) / grid.shape[1]

	# Create the affine transformation matrix setting the top left pixel of the translate component to the min lat/lon and the scale component to the lat/lon pixel sizes
	# Actually also shifts the entire grid by half a pixel as it is assumed that the lat/lon coordinates correspond to the center of a pixel
	transform = rasterio.transform.Affine.translation(min_lon, min_lat) * rasterio.transform.Affine.scale(px_size_lon, px_size_lat)

	# - px_size_lon / 2
	#  - px_size_lat / 2

	# Open the GeoTiff writer
	grid_writer = rasterio.open(path,'w',driver='GTiff',width=grid.shape[0],height=grid.shape[1],count=1,dtype=grid.dtype,crs='+proj=latlong',transform=transform)

	# Write to disk and close
	grid_writer.write(grid, 1)
	grid_writer.close()


def writeLayers(path,name,layers,min_lat,max_lat,min_lon,max_lon):
	""" Writes a stack of grid layers to separate geotiffs at the given path and names the files name_layername.tif."""

	for l in layers:
		file_name = path + "/" + name + "_" + l + ".tif"
		writeGridLatLon(file_name,layers[l],min_lat,max_lat,min_lon,max_lon)
