from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from models.geo_boundary_model import BoundaryMapper
from models.bert_predictive_models import PredictiveModel
from utilities.app_logger import AppLogger
import os

logger = AppLogger.getInstance()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

root = "/home/charan/DATA/311_Data/311_Server_Files"
neigh = os.path.join(root, "Kansas_City_Neighborhood_Boundaries.geojson")
block = os.path.join(root, "1672_Block_Group_Shape.json")
boundary_mapper = BoundaryMapper(block, neigh)
pred_model = PredictiveModel(root)


@app.route('/getPrediction', methods=['POST'])
@cross_origin()
def get_predictions():
    logger.debug("Making search_query call.")
    description = request.json['description']
    result = pred_model.inference_predictive_models(description)
    return jsonify(result), 200


@app.route('/getGeoLocations', methods=['POST'])
@cross_origin()
def get_geo_locations():
    logger.debug("Making search_query call.")
    latitude, longitude = request.json['latitude'], request.json['longitude']
    boundaries = boundary_mapper.get_boundaries(latitude, longitude)
    return jsonify(boundaries), 200


if __name__ == '__main__':
    app.run(port=5002)
