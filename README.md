# taxi_analysis

taxi_analysis is a collection of notebooks and scripts to run analysis on the Chicago taxi dataset. A presentation slides and long form report are available inside the report folder.

### Installation

To install run

```sh
$ git clone https://github.com/chrishendra93/taxi_analysis.git
$ python setup.py install
```

There are four notebooks that requires chicago taxi datasets for the year 2017 to 2021. To download these datasets run

```sh
$ mkdir 2021 & wget https://data.cityofchicago.org/api/views/9kgb-ykyt/rows.csv?accessType=DOWNLOAD -O 2021/chicago_taxi.csv
$ mkdir 2020 & wget https://data.cityofchicago.org/api/views/r2u4-wwk3/rows.csv?accessType=DOWNLOAD -O 2020/chicago_taxi.csv
$ mkdir 2019 & wget https://data.cityofchicago.org/api/views/h4cq-z3dy/rows.csv?accessType=DOWNLOAD -O 2019/chicago_taxi.csv
$ mkdir 2018 & wget https://data.cityofchicago.org/api/views/vbsw-zws8/rows.csv?accessType=DOWNLOAD -O 2018/chicago_taxi.csv
$ mkdir 2017 & wget https://data.cityofchicago.org/api/views/jeij-fq8w/rows.csv?accessType=DOWNLOAD -O 2017/chicago_taxi.csv
```

To clean these datasets and run inference:
```sh
$ clean data --input_dir 2021 2020 2019 2018 2017 --out_dir 2021 2020 2019 2018 2017
$ run_inference --input_fpath ./2021/chicago_taxi_cleaned.csv --out_fpath ./2021/chicago_taxi_pred.txt
```

There are three notebooks that contain data analysis, visualization, and model training on the taxi datasets. data_cleaning.ipynb details the reasoning behind the variables and choice of thresholds used to filter out anomalous rides from all the datasets. data_visualization.ipynb presents visualization of interesting ride patterns on all the datasets and fare_prediction.ipynb details model training and performance for predicting taxi fare on all 5 datasets. If you are running this repository on a machine with limited memory, run the sql-version of the analysis instead

```sh
$ sh initialize_database.sh
$ psql chicago-taxi-data -f clean_data.sql -v min_fare=3.25 -v max_fare=100 -v min_trip_secs=60 -v max_trip_secs=60 -v max_mph=70
```

The SQL version of the data nalysis is in Data Visualization-SQL.ipynb notebook
### Contributors

This package is developed and maintaned by [Christopher Hendra](https://github.com/chrishendra93). If you want to contribute, please leave an issue. Thank you.

### License
MIT
