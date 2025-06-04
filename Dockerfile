#the python version we are using in our container
FROM python:3.12.10

#specify our apps directory
WORKDIR /usr/src/app

#copy the requirements from our app to the WORKDI 
COPY requirements.txt ./

#install packages from requirements
RUN pip install --no-cache-dir -r requirements.txt

#copy all files to the WORKDIR
COPY . ./

#run gunicorn as process manager with uvicorn in it via the config
CMD ["gunicorn", "-c", "gunicorn_conf.py", "app.main:app"]