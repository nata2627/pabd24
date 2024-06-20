"""Train model and save checkpoint"""

import argparse
import logging
import pandas as pd
from sklearn.metrics import mean_absolute_error
from joblib import dump
import xgboost as xgb

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='log/train_model_xgb.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')

TRAIN_DATA = 'data/proc/train.csv'
VAL_DATA = 'data/proc/val.csv'
MODEL_SAVE_PATH = 'models/xgb_model.joblib'


def main(args):
    df_train = pd.read_csv(TRAIN_DATA)
    x_train = df_train.drop(columns='price')
    y_train = df_train['price']
    model = xgb.XGBRegressor(n_estimators=100,max_depth=3)
    model.fit(x_train, y_train)
    dump(model, args.model)
    logger.info(f'Saved to {args.model}')
    r2 = model.score(x_train, y_train)
    mae = mean_absolute_error(y_train, model.predict(x_train))
    logger.info(f'R2 = {r2:.3f}   MAE = {mae}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', 
                        help='Model save path',
                        default=MODEL_SAVE_PATH)
    args = parser.parse_args()
    main(args)