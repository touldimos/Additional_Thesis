Guide to install rasterio -->	https://medium.com/@chrieke/howto-install-python-for-geospatial-applications-1dbc82433c05

- Modality: 	Inputs -->	12 months Precipitation.
		Outputs-->	Number of Peaks, Flats and Rain Modality

- PointClim:	Input -->	X and Y
		Output-->	Number of Peaks, Flats and Rain Modality

- Koppen_class:	Input -->	12 months Precipitation and 12 months Temperature and point's Elevation
		Output-->	Koppen's classification (http://www.guildcompanion.com/scrolls/2014/aug/climatefinder.html)

- run_Koppen:	Input -->	12 months Precipitation and 12 months Temperature and point's Elevation
		Output-->	Koppen's classification

- Run_Clim:	Input-->	12 months Precipitation and 12 months Temperature and point's Elevation
		Outputs-->	Number of Peaks, Flats, Rain Modality and Koppen's classification. (FIGURES)

- Climate_all:			Definition of the function that takes 12 months Precipitation and 12 months Temperature and point's Elevation
				and gives Number of Peaks, Flats, Rain Modality, Koppen's classification and Terrain. (FIGURES)

- Climate:			Run of Climate all


- ECAD_Read:	Input-->	Input daily data of meteorological parameters, filter the flag and missing data
		Outputs-->	Monthly meteorological data, map of the stations