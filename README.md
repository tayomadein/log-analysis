# FSND Project: Logs Analysis
#### by Omotayo Madein

## Description

This is a project for [Udacity Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). The Logs Analysis project focuses on testing and improving my skills in Database Management using PostgreSQL + Python. It answers the following questions: 

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Project contents

This project consists for the following files:

* log.py - Main Script to manage queries and generate content of output.txt
* output.txt - Contains the output of running the queries in log.py

## How to run

* Step 0:

Clone this repo to your desktop
```
git clone https://github.com/tayomadein/log-analysis.git
```
___or___
Download this repo as a zipped file from [Github](https://github.com/tayomadein/log-analysis/archive/master.zip)

* Step 1: 

Setup your virtual environment by following these [instructions](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)

* Step 2:

Download the data used from this [link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and copy it to your shared virtual environment folder `/vagrant/log-analysis` 

* Step 3:

From your virtual environment terminal, switch to `/vagrant/log-analysis`  and run this command to load data
```
psql -d news -f newsdata.sql
```

* Step 4:

Connect to your database using 
```
psql -d news
```

* Step 5:

While connected to your database, run log analysis using

```
python log.py
```
The output will appear 

**Notes:**
* 
