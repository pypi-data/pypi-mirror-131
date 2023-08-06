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


def selectTrainingSamples(layers,coord,lats,lons,vals):
	""" Pick values (aka feature vectors) from grid layers at the given lat lon coordinates """

	Xs = []
	ys = []
	for i,lat in enumerate(lats):
		x,y = coord.toXY(lat,lons[i])
		vec = numpy.zeros(len(layers))
		for j,l in enumerate(layers):
			vec[j] = layers[l][x][y]
		Xs.append(vec)
		ys.append(vals[i])

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


def interpolateobservationsToGrid(lats,lons,vals,gridx,gridy,method='nearest',spatial_buffer = 0.1):
	""" Compute a dense grid from observations with interpolation. Uses scipy.interpolyte.griddata """

	min_lat,max_lat,min_lon,max_lon = minMaxLatLon(lats,lons)
	off_lat = spatial_buffer * (max_lat - min_lat)
	off_lon = spatial_buffer * (max_lon - min_lon)

	points = numpy.vstack((lons,lats)).T

	grid_lon, grid_lat = numpy.mgrid[min_lon-off_lon:max_lon+off_lon:complex(gridx,0), min_lat-off_lat:max_lat+off_lat:complex(gridy,0)]
	grid = griddata(points, vals, (grid_lon, grid_lat), method=method)

	min_val = numpy.min(grid)
	max_val = numpy.max(grid)

	return grid,min_lat-off_lat,max_lat+off_lat,min_lon-off_lon,max_lon+off_lon,min_val,max_val


def krigeObservationsToGrid(lats,lons,vals,gridx,gridy,method='power',spatial_buffer = 0.1):
	""" Compute a dense grid with Kriging. Uses pykrige.UniversalKriging"""

	min_lat,max_lat,min_lon,max_lon = minMaxLatLon(lats,lons)
	off_lat = spatial_buffer * (max_lat - min_lat)
	off_lon = spatial_buffer * (max_lon - min_lon)

	grid_lon = numpy.arange(min_lon-off_lon, max_lon+off_lon, (max_lon-min_lon+2*off_lon)/gridx)
	grid_lat = numpy.arange(min_lat-off_lat, max_lat+off_lat, (max_lat-min_lat+2*off_lat)/gridy)

	UK2 = UniversalKriging(lons,lats,vals,variogram_model=method)
	# drift_terms=["regional_linear"],
	# coordinates_type="geographic"
	# linear, power, gaussian, spherical, exponential, hole-effect

	grid, confidence = UK2.execute("grid", grid_lon, grid_lat)

	min_val = numpy.min(grid)
	max_val = numpy.max(grid)

	return grid.T,confidence,min_lat-off_lat,max_lat+off_lat,min_lon-off_lon,max_lon+off_lon,min_val,max_val


def predictObservationsToGrid(dataset,lats,lons,vals):
	""" Computes a dense grid with a RandomForest regression. Uses scipy.ensemble.RandomForestRegressor """

	# Compute derivatives
	layers = GDALTerrainAnalysisLayers(dataset)

	# Get coordinate transformation object
	coord = GridCoordinate(dataset)

	# Extract training samples
	Xs,ys = selectTrainingSamples(layers,coord,lats,lons,vals)

	# Train the random forest regressor
	clf = trainClassifier(Xs,ys)

	# Apply the classifier to the grid and return the result
	return applyClassifierToGrid(layers,clf)


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
		w,h,z = layers[l].shape
		break

	# Get all valid data vectors and their positions
	vecs = []
	xys = []

	for x in range(w):
		for y in range(h):
			vec = numpy.zeros(len(layers))
			nope = False
			for i,l in enumerate(layers):
				if layers[l][x][y] == None or numpy.isnan(layers[l][x][y]):
					nope = True
					break
				vec[i] = layers[l][x][y]
			if not nope:
				vecs.append(vec)
				xys.append([x,y])

	# Run the prediction
	tmp = clf.predict(vecs)

	# Store the prediction results in a 2D array = image
	img = numpy.zeros((w,h))
	img[:] = numpy.nan
	for i,v in enumerate(tmp):
		img[xys[i][0],xys[i][1]] = v

	return img



def writeGridLatLon(path,grid,grid_latitudes,grid_longitudes):
	""" Takes a dense grid of values and its real-world lat/lon coordinates and stores them as a GeoTiff on disk.

	While the grid axes are simply indexed by array indices (0,1,...), the grid_latitude and grid_longitude arrays
	(numpy or python ranges) contain the lat / lon values for each of these array indices. Actually this is a bit
	of overkill as the function uses only the min/max lat/lon to calculate the pixel resolution of the grid. But
	thats what it is. The resulting GeoTiff is written to the given path (first argument). No sanity checks
	implemented, yet.
	"""

	# Determine the size of one pixel in lat & lon direction
	px_size_lon = (grid_longitudes[-1] - grid_longitudes[0]) / grid.shape[0]
	px_size_lat = (grid_latitudes[-1] - grid_latitudes[0]) / grid.shape[1]

	# Create the affine transformation matrix setting the top left pixel of the translate component to the min lat/lon and the scale component to the lat/lon pixel sizes
	# Actually also shifts the entire grid also by half a pixel as it is assumed that the lat/lon coordinates correspond to the center of a pixel
	transform = rasterio.transform.Affine.translation(grid_longitudes[0] - px_size_lon / 2, grid_latitudes[0] - px_size_lat / 2) * rasterio.transform.Affine.scale(px_size_lon, px_size_lat)

	# Open the GeoTiff writer
	grid_writer = rasterio.open(path,'w',driver='GTiff',width=grid.shape[0],height=grid.shape[1],count=1,dtype=grid.dtype,crs='+proj=latlong',transform=transform)

	# Write to disk and close
	grid_writer.write(grid, 1)
	grid_writer.close()


def writeLayers(path,name,layers,lats,lons):
	""" Writes a stack of grid layers to separate geotiffs at the given path and names the file name_layername.tif."""

	for l in layers:
		file_name = path + "/" + name + "_" + l + ".tif"
		writeGridLatLon(file_name,layers[l],lats,lons)
