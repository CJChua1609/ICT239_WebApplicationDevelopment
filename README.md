# BMI

This is an example flask app for SUSS ICT 239 - web programming.

# Student Details
- Student Name: 
- Student ID: 

To identify your submission, you may rename the `README.md` to `<NAME>_<ID>_README.md`

# Getting started

```
cd app
./start.sh
```


## FAQ

1. The backend chart is producing error when I load the page. 

A. First, check if you have a mongoDB connection. Next, does your database contains the necessary data? If not, you will need to upload dataset2.csv from `assets/js/` before the backend chart will work. 

2. Our default OS is `Ubuntu on Vocareum` only and we do not support Window. This is true for marking too. 

For powershell users, 
```
$env:FLASK_APP="app.py"
$env:PYTHONPATH="." 
$env:FLASK_DEBUG=1
flask run --host=0.0.0.0
```

For command prompt users, 
```
set FLASK_APP=app.py; set PYTHONPATH=.; set FLASK_DEBUG=1;
flask run --host=0.0.0.0
```
