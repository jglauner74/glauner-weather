FROM heroku/miniconda

# Grab requirements.txt.
ADD ./requirements.txt 

# Install dependencies
RUN pip install -qr /requirements.txt

# Add our code
ADD /glauner-weather
WORKDIR /glauner-weather

RUN conda install -c conda-forge cartopy

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
