from flask import Flask, jsonify, request, json, Response
import geopy.distance
from PIL import Image, ImageOps
import numpy as np
import blurhash
import requests
import io

app = Flask(__name__)


def calculate_hash(image_url):
    ''' Calculate the blurhash for an url containing an image '''
    image_response = requests.get(image_url, stream=True)
    image_content = image_response.content
    image = Image.open(io.BytesIO(image_content))
    # downscaling the image yields much better performance 
    # with little to no quality loss as the image is blurred anyway
    size = (20, 20)
    downscaled = ImageOps.fit(image, size, Image.NEAREST)
    pixels = np.array(downscaled.convert("RGB"))
    hash = blurhash.encode(pixels)
    return hash


# initialise the dataset
with open('restaurants.json', 'r') as file:
    restaurant_dict = json.load(file)
    for restaurant in restaurant_dict['restaurants']:
        # recalculate the invalid blurhashes in the dataset
        new_hash = calculate_hash(restaurant['image'])
        restaurant['blurhash'] = new_hash


@app.route('/restaurants/', methods=['GET'])
def get_restaurants():
    ''' Return the data of all restaurants in the database '''
    return jsonify(restaurant_dict['restaurants'])


@app.route('/restaurants/search/', methods=['GET'])
def get_restaurant():
    ''' Return the data of all restaurants that include the queried tag in their
        tags and are less than 3 kilometers away from the queried location.
    '''
    try:
        tag = request.args['q']
        lat = float(request.args['lat'])
        lon = float(request.args['lon'])

    # some or all of the query parameters were invalid
    except KeyError:
        return Response(json.dumps({'error': 'Bad query parameters.'}),
                        status=400,
                        mimetype="application/json")
    else:
        queried_location = (lon, lat)
        matching_restaurants = []
        for restaurant in restaurant_dict['restaurants']:
            if tag in restaurant['tags']:
                current_location = restaurant['location']
                distance = geopy.distance.distance(queried_location,
                                                   current_location).m
                if distance < 3000:
                    matching_restaurants.append(restaurant)

        # returns HTTP 200 OK, along with the queried data
        return jsonify(matching_restaurants)


if __name__ == '__main__':
    app.run()
