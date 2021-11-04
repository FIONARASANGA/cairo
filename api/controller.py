"""Controller"""

import json
import logging
from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from utils.db_connection import get_db_connection
import api.transaction_api as trans_api

logger = logging.getLogger('Cairo')
logger.setLevel(logging.DEBUG)

dashboard_app = Blueprint('Cairo_API', __name__)


@dashboard_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        logger.info('health status OK')
        return 'ok'


# Transaction Summary - Endpoint
@dashboard_app.route('/boa_dashboard/transaction_summary', methods=['POST'])
@cross_origin()
def trans_summary():
    if request.method == 'POST':
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        json_str = json.dumps(json_data)
        jdata = json.loads(json_str)
        start_date = jdata['start_date']
        end_date = jdata['end_date']

        trans_summary = trans_api.transaction_summary(start_date, end_date)

        return trans_summary



