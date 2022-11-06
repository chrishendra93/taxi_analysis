DROP TABLE IF EXISTS cleaned_taxi_trips;

SELECT *
INTO cleaned_taxi_trips
FROM taxi_trips_raw
WHERE
        fare >= :'min_fare'
    AND fare <= :'max_fare'
    AND payment_type NOT IN ('Dispute', 'No Charge', 'Prepaid')
    AND trip_seconds >= :'min_trip_secs'
    AND trip_seconds <= :'max_trip_secs'
    AND trip_miles IS NOT NULL
    AND trip_miles != 0
    AND 3600 * trip_miles / trip_seconds <= :'max_mph'
