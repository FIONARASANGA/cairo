from flask_restful import Resource
from utils.db_connection import get_db_connection
import json
import pandas as pd
from collections import defaultdict
import datetime
import numpy as np
import calendar

def transaction_summary(start_date, end_date):

  #select from the transactions by start_date and end_date

  result = {
    "transaction_count": 0,
    "inflow_amount":0,
    "outflow_amount":0,
    "net_amount":0,
    "projected_inflows":0,
    "projected_outflows":0

  }

  return result 

