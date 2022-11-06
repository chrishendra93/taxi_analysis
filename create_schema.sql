DROP TABLE IF EXISTS taxi_trips_raw;

CREATE UNLOGGED TABLE taxi_trips_raw (
  trip_id text,
  taxi_id text,
  trip_start_timestamp timestamp,
  trip_end_timestamp timestamp,
  trip_seconds numeric,
  trip_miles numeric,
  pickup_census_tract text,
  dropoff_census_tract text,
  pickup_community_area int,
  dropoff_community_area int,
  fare numeric,
  tips numeric,
  tolls numeric,
  extras numeric,
  trip_total numeric,
  payment_type text,
  company text,
  pickup_centroid_latitude numeric,
  pickup_centroid_longitude numeric,
  pickup_centroid_location text,
  dropoff_centroid_latitude numeric,
  dropoff_centroid_longitude numeric,
  dropoff_centroid_location text
);
