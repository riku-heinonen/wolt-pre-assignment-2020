import pytest
from server import app, restaurants
from flask import json
import random
import geopy
from pprint import pprint


@pytest.fixture
def tags():
    '''
        Returns all the possible tags in the dataset
    '''
    tags = []
    for restaurant in restaurants:
        tags.extend(restaurant['tags'])
    return list(set(tags))


@pytest.fixture
def coordinates():
    '''
        Returns the corner coordinates of the bounding
        rectangle of the restaurants in the dataset
    '''
    latitudes = []
    longitudes = []
    for restaurant in restaurants:
        longitudes.append(restaurant['location']['lon'])
        latitudes.append(restaurant['location']['lat'])
    return {
        'min_lat': min(latitudes),
        'max_lat': max(latitudes),
        'min_lon': min(longitudes),
        'max_lon': max(longitudes)
    }


def test_get_restaurants():
    '''
        Test that querying for all restaurants
        returns the correct amount of restaurants
    '''
    response = app.test_client().get('/restaurants/')
    response_list = json.loads(response.data)
    assert response.status_code == 200
    assert len(response_list) == 50


def test_random_queries(tags, coordinates):
    '''
        Make 1000 queries with random parameters chosen from all of the possible tags
        and random locations inside the bounding rectangle of the restaurants in the dataset.
        If the query matches any restaurants, check that the location is less than 3000 metres away
        from the queried location and the tags are included in the restaurant's name, description or tags.
    '''
    for i in range(1000):
        lon = random.uniform(coordinates['min_lon'],
                             coordinates['max_lon'])
        lat = random.uniform(coordinates['min_lat'],
                             coordinates['max_lat'])
        queried_location = (lat, lon)
        tag = random.choice(tags)
        url = f'/restaurants/search/?q={tag}&lat={lat}&lon={lon}'
        response = app.test_client().get(url)

        # the endpoint always returns HTTP 200 if the parameters
        # are valid, whether the queried set is empty or not
        assert response.status_code == 200
        if response.data:
            response_list = json.loads(response.data)
            for restaurant in response_list:
                tag_fields = [restaurant['name'],
                              restaurant['description'],
                              restaurant['tags']]
                assert any(tag in field for field in tag_fields)

                current_location = (restaurant['location']['lat'],
                                    restaurant['location']['lon'])
                distance = geopy.distance.distance(queried_location,
                                                   current_location)
                assert distance.m < 3000


def test_invalid_query():
    '''
        Test that giving invalid query parameters returns HTTP 400 bad request
    '''
    response = app.test_client().get(
        '/restaurants/search/?q=sushi&lat=latitude&lon=longitude')
    response_data = json.loads(response.data)
    assert response.status_code == 400
    assert response_data['error'] == 'Invalid query parameters.'
