## Introduction
This is my pre-assignment for the Wolt 2020 backend internship application. I decided to use Python for the task as that's the language I am most familiar with. The API was created using *Flask* and it also uses the *geopy* module to calculate distances between coordinate pairs.

## Usage
The repository includes a *requirements.txt* file which lists all the Python dependencies.  Before installing them it is advised to create and activate a virtual environment (Python 3.6 and higher)
```
python3 -m venv test-env
source test-env/bin/activate
```
The dependencies can then be installed with pip
```
pip install -r "requirements.txt"
```

After this we are ready to start the API server by running
```
python3 restaurant_API.py
```
The API can now be accessed at localhost port 5000

http://localhost:5000/restaurants/

The API has two URL routes
1. /restaurants/
    * For accessing all data of all restaurants in the database 


2. /restaurants/search/q=\<tag\>&lat=\<lat\>&lon=\<lon\>
    * For accessing all data of the restaurants which match the parameters in the query string. In the URL \<lat\> and \<lon\> represent the latitude and longitude of a restaurant and \<tag\> a tag included in the restaurant's data. The API returns all restaurants that match the tag and are less than 3 kilometers away from the queried location.