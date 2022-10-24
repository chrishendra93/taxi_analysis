import os
import numpy as np
import pandas as pd
import geopandas as gpd
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from copy import deepcopy


def argparser():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        add_help=False
    )
    parser.add_argument("--input_dir", default=None, type=str, nargs="*", required=True)
    parser.add_argument("--out_dir", default=None, type=str, nargs="*", required=True)
    parser.add_argument("--minimum_fare", default=3.25, type=float)
    parser.add_argument("--maximum_fare", default=100, type=float)
    parser.add_argument("--minimum_trip_secs", default=60, type=float)
    parser.add_argument("--maximum_trip_secs", default=7200, type=float)
    parser.add_argument("--maximum_mph", default=70, type=float)

    return parser


def clean_data(input_dir, output_dir, args):

    df = pd.read_csv(os.path.join(input_dir, "./chicago_taxi.csv"))

    # Filtering for minimum fare
    df = df[(df["Fare"] >= args.minimum_fare) & (df["Fare"] <= args.maximum_fare)]

    print("Filtering for minimum and maximum fare: {} entries remaining".format(len(df)))
    
    # Filtering for payment type

    df = df[~df["Payment Type"].isin(["Dispute", "No Charge", "Prepaid"])]    
    print("Filtering for payment type: {} entries remaining".format(len(df)))

    # Filtering for minimum trip duration and maximum trip duration
    df = df[(df["Trip Seconds"] <= args.maximum_trip_secs) \
                & (df["Trip Seconds"] >= args.minimum_trip_secs)]
    
    print("Filtering for trip duration: {} entries remaining".format(len(df)))

    # Filtering for null or zero trip information
    df = df[~(df["Trip Miles"].isna()) & ~(df["Trip Miles"] == 0)]
    
    trip_miles = df["Trip Miles"] * 3600 / df["Trip Seconds"]
    df = df[trip_miles < args.maximum_mph]

    print("Filtering for invalid trip miles: {} entries remaining".format(len(df)))

    # Imputing location information
    ca = gpd.read_file("./chicago_map.geojson")
    ca['area_num_1'] = ca['area_num_1'].astype('int')

    pickup_df = df[["Pickup Centroid Longitude", "Pickup Centroid Latitude",
                    "Pickup Community Area"]]
    dropoff_df = df[["Dropoff Centroid Longitude", "Dropoff Centroid Latitude",
                     "Dropoff Community Area"]]

    pickup_df = gpd.GeoDataFrame(pickup_df, 
                                geometry=gpd.points_from_xy(pickup_df["Pickup Centroid Longitude"],
                                                            pickup_df["Pickup Centroid Latitude"]),
                                crs=4326)

    dropoff_df = gpd.GeoDataFrame(dropoff_df, 
                                geometry=\
                                    gpd.points_from_xy(dropoff_df["Dropoff Centroid Longitude"],
                                                        dropoff_df["Dropoff Centroid Latitude"]),
                                crs=4326)

    pickup_df = gpd.sjoin(ca[["area_num_1", "geometry"]], pickup_df, how='right')
    dropoff_df = gpd.sjoin(ca[["area_num_1", "geometry"]], dropoff_df, how='right')
    
    df["Pickup Community Area"] = pickup_df["Pickup Community Area"].values
    df["Dropoff Community Area"] = dropoff_df["Dropoff Community Area"].values

    df.to_csv(os.path.join(output_dir, "chicago_taxi_cleaned.csv"), index=False)

    
def main():
    args = argparser().parse_args()
    input_dirs = args.input_dir
    output_dirs = args.out_dir

    if len(input_dirs) != len(output_dirs):
        raise ValueError("Number of input directories must match number of output directories")
    
    for input_dir, output_dir in zip(input_dirs, output_dirs):
        clean_data(input_dir, output_dir, args)


if __name__ == '__main__':
    main()
