from flask import Flask, jsonify, request, json, Response
from PIL import Image, ImageOps
import geopy.distance
import numpy as np
import blurhash
import requests
import io

# Config

# If true, recalculates the blurhashes of the dataset
# which takes a few seconds when the server starts.
RECALCULATE_HASHES = False

app = Flask(__name__)


def calculate_hash(image_url):
    """ Calculate the blurhash of an image """
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
with open("restaurants.json", "r") as file:
    restaurants = json.load(file)["restaurants"]
    for restaurant in restaurants:
        # make the location attribute a dictionary
        # to avoid confusion later on
        location = {
            "lat": restaurant["location"][1],
            "lon": restaurant["location"][0]
        }
        restaurant["location"] = location
        if RECALCULATE_HASHES:
            # recalculate the invalid blurhashes in the dataset
            new_hash = calculate_hash(restaurant["image"])
            restaurant["blurhash"] = new_hash


@app.route("/restaurants/", methods=["GET"])
def get_restaurants():
    """ 
        Return HTTP 200 along with the data
        of all restaurants in the dataset. 
    """
    return jsonify(restaurants)


@app.route("/restaurants/search/", methods=["GET"])
def get_restaurant():
    """ 
        Fetch all restaurants that include the queried tag in their
        name, description or tags and are less than 3 kilometers away
        from the queried location. Return HTTP 200 along with the queried
        data or HTTP 400 if the query parameters were invalid. 
    """
    try:
        tag = request.args["q"]
        lat = float(request.args["lat"])
        lon = float(request.args["lon"])

    # missing or invalid parameters
    except (KeyError, ValueError):
        return Response(
            json.dumps({"error": "Invalid query parameters."}),
            status=400,
            mimetype="application/json",
        )
    else:
        queried_location = (lat, lon)
        matching_restaurants = []
        for restaurant in restaurants:
            tag_fields = [
                restaurant["description"],
                restaurant["name"],
                restaurant["tags"],
            ]
            if any(tag in field for field in tag_fields):
                current_location = (
                    restaurant["location"]["lat"],
                    restaurant["location"]["lon"],
                )
                distance = geopy.distance.distance(queried_location,
                                                   current_location)
                if distance.m < 3000:
                    matching_restaurants.append(restaurant)

        return jsonify(matching_restaurants)


if __name__ == "__main__":
    app.run()
