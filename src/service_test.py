"""
Test prediction web-service
If you have error: 503 Response, disable proxies in your requests
https://stackoverflow.com/questions/40430799/503-reponse-when-trying-to-use-python-request-on-local-website
"""
import logging
import time
import numpy as np
import requests
import tqdm
from dotenv import dotenv_values
import pandas as pd
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log/service_test.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(message)s')

endpoints = 'http://192.168.1.7:5000/predict'

config = dotenv_values(".env")
HEADERS = {"Authorization": f"Bearer {config['APP_TOKEN']}"}


def do_request(data: dict, endpoint) -> tuple:
    t0 = time.time()
    resp = requests.post(
        endpoint,
        json=data,
        headers=HEADERS
    )
    resp = resp.json()
    t = time.time() - t0
    return t, resp['price']


def test_100(endpoint, name):
    df = pd.read_csv('data/proc/test_sample.csv')
    prices = df['price']
    df = df.drop(['price'], axis=1)
    records = df.to_dict('records')
    delays, pred_prices = [], []
    for row in tqdm.tqdm(records):
        t, price = do_request(row, endpoint)
        delays.append(t)
        # print(f'Price: {price}, delay: {t}')
        pred_prices.append(price)
    avg_delay = sum(delays) / len(delays)
    error = np.array(pred_prices) - prices.to_numpy()
    avg_error = np.mean(error)
    logger.info(f'{name}: Avg delay: {avg_delay*1000} ms, avg error: {avg_error} RUB')


if __name__ == '__main__':
    test_100(endpoints, "nata")