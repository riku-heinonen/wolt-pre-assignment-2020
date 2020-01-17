from flask import Flask, jsonify, request, json
import geopy.distance

app = Flask(__name__)

# initialise the database
with open('restaurants.json', 'r') as file:
    restaurant_dict = json.load(file)


#  return the data of all restaurants in the database
@app.route('/restaurants/', methods=['GET'])
def get_restaurants():
    return jsonify(restaurant_dict['restaurants'])


# return all restaurants that match the query
@app.route('/restaurants/search/', methods=['GET'])
def get_restaurant():
    tag = request.args.get('q', type=str)
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    queried_location = (lon, lat)
    matching_restaurants = []

    # From all the restaurants, find the ones which are tagged
    # with the queried tag and are less than 3 kilometers away.
    for restaurant in restaurant_dict['restaurants']:
        if tag in restaurant['tags']:
            current_location = restaurant['location']
            distance = geopy.distance.distance(
                queried_location, current_location).m
            if distance < 3000:
                matching_restaurants.append(restaurant)

    return jsonify(matching_restaurants)


if __name__ == '__main__':
    app.run(debug=True)
