"""  https://github.com/lenarsaitov/cianparser
"""
import datetime

import cianparser
import pandas as pd
from dotenv import dotenv_values
import boto3

YOUR_ID = '18'

config = dotenv_values(".env")
client = boto3.client(
    's3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=config['KEY'],
    aws_secret_access_key=config['SECRET']
)

moscow_parser = cianparser.CianParser(location="Москва")

n_rooms = [1, 2, 3]


def main():
    """Function docstring"""
    for rooms in n_rooms:
        CSV_PATH = f'data/raw/{rooms}_file.csv'
        data = moscow_parser.get_flats(
            deal_type="sale",
            rooms=(rooms,),
            with_saving_csv=True,
            additional_settings={
                "start_page": 1,
                "end_page": 2,
                "object_type": "secondary"
            })
        df = pd.DataFrame(data)
        df.to_csv(CSV_PATH,
                  encoding='utf-8',
                  index=False)


if __name__ == '__main__':
    main()
