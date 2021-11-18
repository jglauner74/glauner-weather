# AAA-Projects
###final project for cs50


The goal was to build a website to view weather forecasts, specifically precipitation.

There are a few main weather models used in the agriculture industry.  Governments produce them.  Core models are: GFS (Global Forecasting System -- USA),
EURO, and Canadian models.  The USA's 2 week (16 day) model, the GFS, is free... thus, was my focus.

I've had meterologists in the past and most don't want to provide simply what the models say (because their expertise often can show where the model is wrong).

What I've always wanted, I built.  I wanted a website that organized model runs by date of forecast.  In this way, I and my friends can look at the
current forecast for a specific day and see how that forecast has changed/drifted since the model started forecasting that day.

To complete this project, I had to learn how to query and to use netCDF4 and xarray files as well as cartopy, a mapping tool used by meteorologists.

Finally, I had to learn how to use a scheduler to keep updating the data.
