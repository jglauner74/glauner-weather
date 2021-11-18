from datetime import datetime, timedelta, timezone
import pytz
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point
from siphon.catalog import TDSCatalog
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import netCDF4 as Dataset
from metpy.plots import USCOUNTIES




### This is to build the past pictures library which I'm storing in /static/pics
### I may adjust it after I've build a history, to then somewhat automate the process


def timename(daytah):
    ### This function identifies the name of the "time" variable in the netcdf file
    ### That variable switches seemingly daily from: time2, time1, to time27... etc
    ### Then I can rename the file's time fuction using this info
    thenumber = 0
    for i in range(len(list(daytah.variables))):
        if list(daytah.variables)[i].startswith('time'):
            thenumber = i
    return(list(daytah.variables)[thenumber])


def yesterday(var = 1):
    # In the short term, I'm going to totally revamp this -- I think it might need to be user input
    # Which day to search for
    
    yesterday = datetime.utcnow() - timedelta(days=var)
    return yesterday.strftime("%Y%m%d")

def yesterday_url():
    
    ### This just puts together the URL for the date you've picked
    ### I can delete the "x=1" part, if I get the dates differently like from user input
    
    baseurl = ('https://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/Global_0p5deg'
          '/GFS_Global_0p5deg_' + string_date_of_forecast + '_0000.grib2/'
          'catalog.html?dataset=grib/NCEP/GFS/Global_0p5deg'
          '/GFS_Global_0p5deg_' + string_date_of_forecast + '_0000.grib2')
    
    
    return baseurl


def get_data():
    
    #This designs the query object and query's the data from the thredds server
    
    yesterdaygfs = TDSCatalog(yesterday_url())
    yday = yesterdaygfs.datasets[0]
    ncss = yday.subset()
    query = ncss.query()
    query.lonlat_box(north=n, south=s, east=e, west=w).time_range(date_of_forecast, date_of_forecast+timedelta(days=16))
    query.accept('netcdf4')
    query.variables('Precipitation_rate_surface')
    data = ncss.get_data(query)
    return data




def main(forecastdate = None, location = None):

    #set these variables to be used in the other def's as well...
    global date_of_forecast
    global string_date_of_forecast
    global n, e, w, s
    global nam
    
    if forecastdate == None:
        date_of_forecast = datetime(int(input("Year: ")), int(input("Month Number: ")), int(input("Day: "))).astimezone(pytz.utc)
    
        string_date_of_forecast = date_of_forecast.strftime("%Y%m%d")
    
    else:
        
        date_of_forecast = datetime(int(forecastdate[0:4]), int(forecastdate[4:6]), int(forecastdate[6:8])).astimezone(pytz.utc)
                                    
        string_date_of_forecast = forecastdate
    
                                    
                                    
                                    
    if location == None:
        #stick with the north american values
        n, s, e, w = 50, 35, -80, -104
        nam = f'static/pics/usa/%s_from_forecast_date:%s.png'
        
    elif location == 'Argentina':
        #use the south american values
        n, s, e, w = -25, -40, -50, -65  
        nam = f'static/pics/Argentina/%s_from_forecast_date:%s.png'
                                    
    else:
        print("That's not an acceptable location - pick either '' or 'Argentina'")
    
                                    
    
    data = get_data()

    thyme = timename(data)

    ds = xr.open_dataset(xr.backends.NetCDF4DataStore(data))

    ds = ds.rename({thyme: 'time'})

    ds = ds.resample(time='1D').mean()


    for i in range(0,16):
        rain = ds['Precipitation_rate_surface'][i,:,:]*60*60*24/25.4
    
        rain,lons=add_cyclic_point(rain,coord=ds['lon'])  #test
    
    
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

 

    # draw coastlines, state and country boundaries, edge of map.

        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linewidth=1.2)
        ax.add_feature(cfeature.STATES)
        ax.add_feature(USCOUNTIES, linewidth=0.3)

 

    # draw filled contours.

        clevs = [0, 0.05, 0.10, 0.20, 0.35, 0.5, 0.65, 0.8, 1.0, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8]

 

    #clevs = np.linspace(0,rain.max()*1.2,21)   Keeping just in case

 

 

    # In future MetPy

    # norm, cmap = ctables.registry.get_with_boundaries('precipitation', clevs)

        cmap_data = [(1.0, 1.0, 1.0), (0.3137255012989044, 0.8156862854957581, 0.8156862854957581),
            (0.0, 1.0, 1.0), (0.0, 0.8784313797950745, 0.501960813999176),(0.0, 0.7529411911964417, 0.0),
            (0.501960813999176, 0.8784313797950745, 0.0),(1.0, 1.0, 0.0),(1.0, 0.6274510025978088, 0.0),
            (1.0, 0.0, 0.0),(1.0, 0.125490203499794, 0.501960813999176),(0.9411764740943909, 0.250980406999588, 1.0),
            (0.501960813999176, 0.125490203499794, 1.0),(0.250980406999588, 0.250980406999588, 1.0),
            (0.125490203499794, 0.125490203499794, 0.501960813999176),
            (0.125490203499794, 0.125490203499794, 0.125490203499794),
            (0.501960813999176, 0.501960813999176, 0.501960813999176),
            (0.8784313797950745, 0.8784313797950745, 0.8784313797950745),
            (0.9333333373069763, 0.8313725590705872, 0.7372549176216125),
            (0.8549019694328308, 0.6509804129600525, 0.47058823704719543),
            (0.6274510025978088, 0.42352941632270813, 0.23529411852359772),
            (0.4000000059604645, 0.20000000298023224, 0.0)]

        cmap = mcolors.ListedColormap(cmap_data, 'precipitation')

        norm = mcolors.BoundaryNorm(clevs, cmap.N)

 

        cs = ax.contourf(lons,ds['lat'],rain, clevs, cmap=cmap, norm=norm, transform=ccrs.PlateCarree())

 

# add colorbar.

        cbar = plt.colorbar(cs, orientation='horizontal')

        cbar.set_label('inches')

 

        ax.set_title(f'Rainfall totals in inches for %s from forecast date: %s' % ((date_of_forecast + timedelta(days = i)).strftime("%Y%m%d"), string_date_of_forecast))

        plt.savefig(nam % ((date_of_forecast + timedelta(days = i)).strftime("%Y%m%d"), string_date_of_forecast), bbox_inches='tight')
    
        #plt.show()


if __name__ == "__main__":
    main()
    


    
    
### Should I create a sqlite database of all of the forecast dates & dates forcasted?...
### then I could have a drop down in the html to select each?!?
### no, the vision is that I select all of the forecasts for a specific date forecasted.


