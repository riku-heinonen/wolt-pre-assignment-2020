## Introduction
This is my submission for the pre-assignment of Wolt 2020 backend internship
application. The assignment was to create a RESTful API that serves restaurant
data in JSON format. I decided to use Python along with the
[Flask](https://pypi.org/project/Flask/) micro framework for the task as Python
is the language I am most familiar with.

## Blurhash
I also familiarised myself with blurhash as per the bonus task. According to
blurha.sh and the [blurhash](https://pypi.org/project/blurhash/) module the
blurhashes in the given dataset are of invalid length and cannot be decoded. For
this reason I decided to add an option to recalculate the blurhashes when
loading the data. This option can be enabled or disabled by setting the
RECALCULATE_HASHES flag at the top of server.py to True or False, respectively.
If the blurhashes are recalculated, booting the server as well as running the
unit tests takes around 10 seconds longer.

Calculating the blurhashes uses the python modules
[blurhash](https://pypi.org/project/blurhash/) for calculating the hash,
[Pillow](https://pypi.org/project/Pillow/) and
[numpy](https://pypi.org/project/numpy/) for handling images and
[requests](https://pypi.org/project/requests/) to fetch the images from the URLs
in the dataset. 

## Setup
The application is written in Python 3.7.5 and most likely requires atleast
version 3.6. Python can be [downloaded from
here](https://www.python.org/downloads/) if you do not have it installed yet.


The repository includes a *requirements.txt* file which lists all of the Python
dependencies.  Before installing them it is advised to create and activate a
virtual environment (Python 3.6 and higher)
```
python3 -m venv test-env
source test-env/bin/activate
```
The dependencies can then be installed with pip
```
pip install -r requirements.txt
```

After this we are ready to start the API on a WSGI server with [gunicorn](https://pypi.org/project/gunicorn/) by running
```
gunicorn server:app
```
## Usage
After the setup the API can be accessed at localhost port 8000.

http://localhost:8000/restaurants/

The API has two URL routes
1. /restaurants/
    * For accessing all data of all restaurants in the database 


2. /restaurants/search/?q=\<tag\>&lat=\<lat\>&lon=\<lon\>
    * For accessing all data of the restaurants which match the parameters in the query string. In the URL \<lat\> and \<lon\> represent the latitude and longitude of a restaurant and \<tag\> a tag included in the restaurant's data. The API returns all restaurants that mention the queried tag in their name, description or tags and are less than 3 kilometers away from the queried location.

## Tests
The API can be unit tested with [pytest](https://docs.pytest.org/en/latest/) (included in requirements.txt) by simply running: 
```
pytest
```
The tests can be found and inspected in the *test_server.py* file.