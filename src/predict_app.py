"""House price prediction service"""
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from joblib import load
from dotenv import dotenv_values
from flask_httpauth import HTTPTokenAuth
from src.utils import *

MODEL_SAVE_PATH = 'models/xgb_model.joblib'

app = Flask(__name__)
CORS(app)

config = dotenv_values(".env")
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    config['APP_TOKEN']: "user1",
}

model = load(MODEL_SAVE_PATH)


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

def predict(in_data: dict) -> int:
    """ Predict house price from input data parameters.
    :param in_data: house parameters.
    :raise Error: If something goes wrong.
    :return: House price, RUB.
    :rtype: int
    """
    df = pd.DataFrame([in_data], columns=['url_id', 'floor', 'floors_count', 'rooms_count', 'total_meters'])
    price = model.predict(df)
    return int(price)



@app.route("/")
def home():
    return '<h1>Housing price service.</h1> Use /predict endpoint'


@app.route("/predict", methods=['POST'])
def predict_web_serve():
    """Dummy service"""
    in_data = request.get_json()
    price = predict(in_data)
    return {'price': price}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
