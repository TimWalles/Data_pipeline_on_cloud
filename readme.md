# Welcome to the GANS github repository
This github is part of coding project on data pipelines as part of the data science bootcamp at WBS. The goal of the project was to develop a create a mysql database on AWS and a data pipeline (so-called lambda function) also on AWS that pushes data to the mysql database.

## To-Do-List
- deploy docker with AWS CDK
- add more cities to the database


## project background
GANS


## Project steps:
- In the first step of the project I created a free AWS MySQL RD instance and created a relational database inside it, followed by populating the static databases that contained cities and airports information. 
- in the next step I developed two pipelines, one for getting weather info and another for flights information via API requests and associated normalization functions. 
- to deploy the pipelines as a lambda function on AWS I used a docker image and the AWS CLI software.

## setting up the local repository
### setting up your environment variables
please start with making a copy of the `.env-dist` file and rename it to `.env`. Inside the created `.env` file please add your required information. Please note that getting a API key for the AeroBox API isn't for free. 

### install dependencies
It's recommended to create a new `virtualenv` or `conda` environment and install the required packages inside that environment.

To install the required packages please run:
```bash
pip install -r requirements.txt
```

## setting up MySql architecture on AWS
In a first step connect to your MySQL instance on the AWS RD service and then run the queries inside the `setup_gans_database.sql`. 

```Please change the database name on the first line to the name you used for your database.```

## creating and pushing cities and airports data to the MySQL DB tables on AWS
by running both notebooks `city_data.ipynb` and `flight_data.ipynb` will populate the tables:
- cities
- cities_locations
- populations
- airports
- airports_location
- cities_airports

## build and test the docker image
```Copy and paste the .env file created into the image folder```

See also the AWS developer guide: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html

### Docker build, run and test
From inside the image folder you can use this command in your terminal to build the docker container:
```bash
docker build --platform linux/amd64 -t docker-image:test .
```
followed by to run the docker:
```bash
docker run -p 9000:8080 docker-image:test
```
To test it then you run in a new terminal:
```bash
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

### Docker compose
you can also choose to use docker-compose by running the following command inside your terminal:
```bash
docker-compose up --build
```
To test it then you run in a new terminal:
```bash
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```
After testing you can run the following command to remove the docker image again:
```bash
docker-compose down
```

## Deploying the docker image to Lambda
`In a real world situation you add your API keys inside the secret manager but this isn't a for free service. Therefor in this example we pass our secrets as environment variables`
### Using the developers guide
A detailed description on how to deploy your docker image on lambda can be found on the AWS developer guide: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html . Please follow the whole guide up creating the lambda function.
When we want to create the lambda function we need to pass in an additional parameter `--environment`, see example below. Please note the `<INSERT ITEM>` these needs to be replaced with the content in your .env file. 
```bash

aws lambda create-function \
    ...
    --environment Variables="{OPEN_WEATHER_API=<INSERT ITEM>,OPEN_WEATHER_KEY=<INSERT ITEM>,AERO_DATA_KEY=<INSERT ITEM>,RD_HOST=<INSERT ITEM>,RD_SCHEMA=<INSERT ITEM>,RD_USER=<INSERT ITEM>,RD_KEY=<INSERT ITEM>,RD_PORT=<INSERT ITEM>}"
```
### Deploying using the shellscript
Alternatively the image can also be deployed using filling in all required information into the deploy-image-dist.sh and run the shellscript from your terminal.

## Update your image
An error that a lambda function with that name already exists is returned When you rerun the deploy-image-dist.sh after you made changes to your script and want to update your lambda function. please use the following command instead:
```bash
aws lambda update-function-code \
    --function-name  my-function \ # replace my-function with your lambda function name
    --image-uri # URI of a container image in the Amazon ECR registry
```