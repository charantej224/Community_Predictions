from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
from models.geo_boundary_model import BoundaryMapper
from utilities.app_logger import AppLogger

logger = AppLogger.getInstance()
root = "/home/charan/DATA/311_Data/Boundary_Mapping"
neigh = os.path.join(root, "Kansas_City_Neighborhood_Boundaries.geojson")
block = os.path.join(root, "1672_Block_Group_Shape.json")
boundary_mapper = BoundaryMapper(block, neigh)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/getGeoLocations', methods=['POST'])
@cross_origin()
def search_query():
    logger.debug("Making search_query call.")
    latitude, longitude = request.json['latitude'], request.json['longitude']
    boundaries = boundary_mapper.get_boundaries(latitude, longitude)
    return jsonify(boundaries), 200


if __name__ == '__main__':
    app.run(port=5002)
