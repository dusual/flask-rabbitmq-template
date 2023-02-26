## flask-rabbitmq-template
A sample app using flask, rabbitmq and celery


### Setup to install the app

```
$ touch csv_file.csv # this step is already done in the repo
$ docker-compose up --build --remove-orphans
```
This creates the csv file where the data is added from celery worker 
and the docker-compose file creates the containers for the app, rabbitmq and celery worker.

### Testing the app

```
$python test_api.py # run and calls the api 1000 times
$python check_csv.py # checks the count of number of lines of the csv file created by celery worker
```


