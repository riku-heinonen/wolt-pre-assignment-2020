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


if __name__ == '__main__':
    app.run(debug=True)
