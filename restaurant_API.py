from flask import Flask, jsonify, request, json
import geopy.distance

app = Flask(__name__)

# initialise the database
with open('restaurants.json', 'r') as file:
    restaurant_dict = json.load(file)


@app.route('/restaurants/', methods=['GET'])
def get_restaurants():
    """ return the data of all restaurants in the database """
    return jsonify(restaurant_dict['restaurants'])


@app.route('/restaurants/search/', methods=['GET'])
def get_restaurant():
    """ Return the data of all restaurants that include the queried tag in their        tags and are less than 3 kilometers away from the queried location.
    """
    tag = request.args.get('q', type=str)
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    queried_location = (lon, lat)

    matching_restaurants = []
    for restaurant in restaurant_dict['restaurants']:
        if tag in restaurant['tags']:
            current_location = restaurant['location']
            distance = geopy.distance.distance(queried_location,
                                               current_location).m
            if distance < 3000:
                matching_restaurants.append(restaurant)

    return jsonify(matching_restaurants)


if __name__ == '__main__':
    app.run(debug=True)
