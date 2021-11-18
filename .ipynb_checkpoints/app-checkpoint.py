from flask import Flask, render_template, request
import os
import glob
from datetime import datetime, timedelta, timezone
import graphics
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)

###THIS WAS THE OLD WAY I TRIED###
#class Config:
#    SCHEDULER_API_ENABLED = True

#scheduler = APScheduler()
#app.config.from_object(Config())
#scheduler.init_app(app)
#scheduler.start()





@app.route('/')
def index():
    return render_template("index.html")


@app.route('/argentina', methods = ['GET', 'POST'])
def argentina():
    if request.method == 'POST':
        
        forecast_date = str(request.form.get("forecast_dates"))
        
        files = glob.glob("static/pics/Argentina/*")
        
        #I have to only match the first date which was the forecasted date - not the date of the forecast
        matching = [s for s in files if forecast_date in s[0:32]]
        
        matching.sort(reverse = True)
    
    
        return render_template('argentina.html', links=matching)

            
            
    
    else:
    
        files=glob.glob("static/pics/Argentina/*")

        files = [file.replace('static/pics/Argentina/', '') for file in files]
    
        forecast_dates = list(set([x[0:8] for x in files]))
        forecast_dates = [int(x) for x in forecast_dates]
        forecast_dates.sort(reverse = True)
        
        return render_template("argentina.html", forecast_dates = forecast_dates)

    
    
    

@app.route('/usa', methods = ['GET', 'POST'])
def usa():
    if request.method == 'POST':
        
        forecast_date = str(request.form.get("forecast_datez"))
        
        files = glob.glob("static/pics/usa/*")
        
        #I have to only match the first date which was the forecasted date - not the date of the forecast
        matching = [s for s in files if forecast_date in s[0:30]]
        
        matching.sort(reverse = True)
    
    
        return render_template('usa.html', links=matching)

            
            
    
    else:
    
        filez=glob.glob("static/pics/usa/*")

        filez = [file.replace('static/pics/usa/', '') for file in filez]
    
        forecast_datez = list(set([x[0:8] for x in filez]))
        forecast_datez = [int(y) for y in forecast_datez]
        forecast_datez.sort(reverse = True)
        
        return render_template("usa.html", forecast_datez = forecast_datez)

    
    
    
@app.route('/newest', methods = ['GET', 'POST'])
def newest():
    if request.method == 'POST':
        
        return render_template('index.html')

    else:
    
        files=glob.glob("static/pics/Argentina/*")
        filez=glob.glob("static/pics/usa/*")

        #files = [file.replace('.png', '') for file in files]
        #filez = [file.replace('.png', '') for file in filez]
    
        forecast_arg = list(set([x[-12:-4] for x in files]))
        forecast_arg = [int(x) for x in forecast_arg]
        forecast_arg.sort(reverse = True)
        newest_arg = str(forecast_arg[0])
        matching_arg = [s for s in files if newest_arg in s[-12:-4]]
        matching_arg.sort(reverse = True)
        
        
        
        
        forecast_usa = list(set([y[-12:-4] for y in filez]))
        forecast_usa = [int(y) for y in forecast_usa]
        forecast_usa.sort(reverse = True)
        newest_usa = str(forecast_usa[0])
        matching_usa = [t for t in filez if newest_usa in t[-12:-4]]
        matching_usa.sort(reverse = True)
        
        
        
        
        return render_template("newest.html", matching_arg = matching_arg, matching_usa = matching_usa)    
    
    
    
    
    
    

### BEFORE I WAS TRYING TO SCHEDULE TASKS, I CAME UP WITH THIS --- PROBABLY SHOULD JUST DELETE IT
#def check_open_dates():
 #   ### I've got to find the latest date of forecast
  #  files = glob.glob("static/pics/*")
   # matching = [s[-12:-4] for s in files]
    #matching.sort(reverse=True)
#    last_forecast = datetime(int(matching[0][0:4]),int(matching[0][4:6]),int(matching[0][6:8]))
    
    ### Figure out today's date
 #   todays_date = datetime.utcnow()
    
    
 #   midnight = datetime(todays_date.year, todays_date.month, todays_date.day)
    
    ### Then figure out how to work through those forecast dates - adding them to the available data
    
  #  difference = (midnight - last_forecast).days
    
 #   if difference > 0:
  #      for i in range(0,difference):
   #         forecast_date = last_forecast + timedelta(days=i+1)
    #        string_date_of_forecast = forecast_date.strftime("%Y%m%d")
     #       graphics.main(string_date_of_forecast)
    
    
    

#@scheduler.task('cron', id='do_job', hour='1')
def job1():
    today = datetime.utcnow()
    today = datetime(today.year, today.month, today.day)
    string_date_of_forecast = today.strftime("%Y%m%d")
    graphics.main(forecastdate = string_date_of_forecast, location = None)  
    

    
#@scheduler.task('cron', id='do_job2', hour='2')
def job2():
    today = datetime.utcnow()
    today = datetime(today.year, today.month, today.day)
    string_date_of_forecast = today.strftime("%Y%m%d")
    graphics.main(forecastdate = string_date_of_forecast, location = 'Argentina')    
    
    

    
sched = BackgroundScheduler(daemon=True)


sched.add_job(job1,'cron',hour='1', minute='11')
sched.add_job(job2,'cron',hour='1', minute='13')


sched.start()



if __name__ == '__main__':
    app.run(debug = True)