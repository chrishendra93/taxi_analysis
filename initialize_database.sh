
#!/bin/bash

createdb chicago-taxi-data

psql chicago-taxi-data -f create_schema.sql

cat chicago_map.csv | psql chicago-taxi-data -c "COPY chicago_map FROM stdin CSV HEADER;"

echo "`date`: beginning raw taxi data load"
cat 2021/chicago_taxi.csv | psql chicago-taxi-data -c "set datestyle to MDY; COPY taxi_trips_raw FROM stdin CSV HEADER;"
cat 2020/chicago_taxi.csv | psql chicago-taxi-data -c "set datestyle to MDY; COPY taxi_trips_raw FROM stdin CSV HEADER;"
cat 2019/chicago_taxi.csv | psql chicago-taxi-data -c "set datestyle to MDY; COPY taxi_trips_raw FROM stdin CSV HEADER;"
cat 2018/chicago_taxi.csv | psql chicago-taxi-data -c "set datestyle to MDY; COPY taxi_trips_raw FROM stdin CSV HEADER;"
cat 2017/chicago_taxi.csv | psql chicago-taxi-data -c "set datestyle to MDY; COPY taxi_trips_raw FROM stdin CSV HEADER;"

# shp2pgsql -d -I shapefiles/community_areas/community_areas.shp | psql -d chicago-taxi-data
# shp2pgsql -d -I shapefiles/census_tracts/census_tracts.shp | psql -d chicago-taxi-data

# weather_schema="station_id, station_name, date, average_wind_speed, precipitation, snowfall, snow_depth, max_temperature, min_temperature"
# cat data/chicago_weather_data.csv | psql chicago-taxi-data -c "COPY weather_observations (${weather_schema}) FROM stdin WITH CSV HEADER;"
# psql chicago-taxi-data -c "UPDATE weather_observations SET average_wind_speed = NULL WHERE average_wind_speed = -9999;"
