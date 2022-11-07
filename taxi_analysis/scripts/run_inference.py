import os
import torch
import numpy as np
import pandas as pd
import joblib
import pkg_resources
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from copy import deepcopy
from datetime import datetime, timedelta
from sklearn.preprocessing import LabelEncoder
from .model import FarePredictor


DEFAULT_EMBEDDING_WEIGHTS = pkg_resources.resource_filename("taxi_analysis.model", 'nn_model.pth')
DEFAULT_MODEL = pkg_resources.resource_filename('taxi_analysis.model', 'xgb_clf.joblib')
DEFAULT_SCALER = pkg_resources.resource_filename('taxi_analysis.model', 'scaler.joblib')
NUMERICAL_FEATURES = ['Trip Miles', 'Trip Seconds', 'Trip Start Time', 'Trip End Time']
CAT_FEATURES = ['Pickup Community Area', 'Dropoff Community Area', 'Payment Type', 'month', 'weekday']
DEFAULT_NN_PARAMS = {'numeric_features': NUMERICAL_FEATURES,
                     'embedding_in_channels' : [79, 79, 5, 12, 7],
                     'embedding_out_channels' : [2, 2, 2, 2, 2],
                     'hidden_layers' : [32, 64, 32]}

def argparser():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        add_help=False
    )
    parser.add_argument("--input_fpath", default=None, type=str, nargs="*", required=True)
    parser.add_argument("--out_fpath", default=None, type=str, nargs="*", required=True)
    return parser


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def encode_cat_variables(df):

    
    # Converting to datetime format
    
    dtformat = "%m/%d/%Y %I:%M:%S %p"

    df["Trip Start Timestamp"] = pd.to_datetime(df["Trip Start Timestamp"], format=dtformat)
    df["Trip End Timestamp"] = pd.to_datetime(df["Trip End Timestamp"], format=dtformat)
    
    df["Trip Start Time"] = df["Trip Start Timestamp"].dt.time.astype('str')
    df["Trip End Time"] = df["Trip End Timestamp"].dt.time.astype('str')

    df['month'] = df['Trip Start Timestamp'].dt.month
    df['weekday'] = df['Trip Start Timestamp'].dt.day_name()
    
    # Encoding date time information
    
    # There are 96 15-minutes interval from 00:00 to 23:45
    time_encoder = LabelEncoder().fit([dt.strftime('%H:%M:%S') for dt in 
           datetime_range(datetime(2016, 9, 1, 0), datetime(2016, 9, 1, 23, 59), 
           timedelta(minutes=15))])
    
    df["Trip Start Time"] = time_encoder.transform(df["Trip Start Time"]) / 95
    df["Trip End Time"] = time_encoder.transform(df["Trip End Time"]) / 95
    
    # Encoding month and day of the week
    df['month'] = LabelEncoder().fit(np.arange(1, 13)).transform(df['month'])
    df['weekday'] = LabelEncoder().fit(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
                                        'Saturday', 'Sunday']).transform(df['weekday'])
                                        
    df["Pickup Community Area"] = df["Pickup Community Area"].fillna(78).astype('int')
    df["Dropoff Community Area"] = df["Dropoff Community Area"].fillna(78).astype('int')

    df["Payment Type"] = df["Payment Type"].fillna('Unknown')
    df["Payment Type"] = LabelEncoder().fit(['Cash', 'Unknown', 'Credit Card', 'Prcard', 'Mobile'])\
        .transform(df["Payment Type"])
    
    return df


def extract_embedding(df, num_columns, cat_columns, model):
    model.eval()
    with torch.no_grad():
        embedding_layers = model.embedding_layers
        cat_features = torch.LongTensor(df[cat_columns].values)
        cat_features = torch.cat([embedding_layer(cat_feature.squeeze(1)) for 
                                  embedding_layer, cat_feature in
                              zip(embedding_layers, cat_features.split(1, dim=1))], dim=1).numpy()
        return np.concatenate([df[num_columns], cat_features], axis=1)


def run_inference(input_fpath, out_fpath, args):

    # Loading embedding models
    nn_model = FarePredictor(**DEFAULT_NN_PARAMS)
    nn_model.load_state_dict({k.split("module.")[1]: v for k, v in torch.load(DEFAULT_EMBEDDING_WEIGHTS)['model'].items()})

    # Loading XGBoost Regressor
    
    xgbr = joblib.load(DEFAULT_MODEL)
    scaler = joblib.load(DEFAULT_SCALER)

    # Normalizing data and extracting features
    df = pd.read_csv(input_fpath)
    df.loc[~df["Payment Type"].isin(['Cash', 'Unknown', 'Credit Card', 'Prcard', 'Mobile']), "Payment Type"] = "Unknown"
    df = encode_cat_variables(df)
    df.loc[:, NUMERICAL_FEATURES] = scaler.transform(df[NUMERICAL_FEATURES]).astype('float32')
    X = extract_embedding(df, NUMERICAL_FEATURES, CAT_FEATURES, nn_model)

    # Running prediction
    pred = xgbr.predict(X)
    np.savetxt(out_fpath, pred)
    
def main():
    args = argparser().parse_args()

    if len(args.input_fpath) != len(args.out_fpath):
        raise ValueError("Number of input directories must match number of output directories")
    
    for input_fpath, out_fpath in zip(args.input_fpath, args.out_fpath):
        run_inference(input_fpath, out_fpath, args)


if __name__ == '__main__':
    main()
