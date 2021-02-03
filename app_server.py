from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from models.geo_boundary_model import BoundaryMapper
from models.bert_predictive_models import PredictiveModel
from utilities.app_logger import AppLogger
import os
from flask_ngrok import run_with_ngrok

logger = AppLogger.getInstance()
app = Flask(__name__)
run_with_ngrok(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

root = "/home/charan/DATA/311_Data/311_Server_Files"
neigh = os.path.join(root, "Kansas_City_Neighborhood_Boundaries.geojson")
block = os.path.join(root, "1672_Block_Group_Shape.json")
police = os.path.join(root, "Police Divisions.geojson")
council = os.path.join(root, "Council Districts.geojson")

boundary_mapper = BoundaryMapper(block, neigh, police, council)
pred_model = PredictiveModel(root)


@app.route('/getPrediction', methods=['GET', 'POST'])
@cross_origin()
def get_predictions():
    if request.method == 'POST':
        logger.debug("Making search_query call.")
        description = request.json['description']
    elif request.method == 'GET':
        logger.debug("Making GET call.")
        description = request.args.get('description')
    result = pred_model.inference_predictive_models(description)
    return jsonify(result), 200


@app.route('/getGeoLocations', methods=['GET', 'POST'])
@cross_origin()
def get_geo_locations():
    if request.method == 'POST':
        logger.debug("Making search_query POST call.")
        latitude, longitude = request.json['latitude'], request.json['longitude']
    elif request.method == 'GET':
        logger.debug("Making search_query GET call.")
        latitude, longitude = float(request.args.get('latitude')), float(request.args.get('longitude'))
    boundaries = boundary_mapper.get_boundaries(latitude, longitude)
    return jsonify(boundaries), 200


if __name__ == '__main__':
    app.run(port=5002)
