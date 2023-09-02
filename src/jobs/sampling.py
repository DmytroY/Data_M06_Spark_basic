from src.shared.udfs import get_geohash4_udf

def _load_one_csv(config, df, file):
    """ Save data to csv file """
    df.coalesce(1).write.option("header",True).mode("overwrite").csv(
        f"{config.get('output_data_path')}/{file}"
    )

def run_job(spark, config):
    # sampling data for hotels with coordinates in Italy (Latitude/Longitude range (45, 8)-(46, 10)) + US, Washington
    df_h = spark.read.option("header", True).csv(f"{config.get('source_data_path')}/hotels")  
    df_h_sample1 = df_h \
        .filter(df_h.Latitude > 45.0) \
        .filter(df_h.Latitude < 46.0) \
        .filter(df_h.Longitude > 8.0) \
        .filter(df_h.Longitude < 10.0)
    
    df_h_sample2 = df_h \
        .filter(df_h.Country == "US") \
        .filter(df_h.City == "Washington")
    
    df_h_sample = df_h_sample1.union(df_h_sample2).distinct()
    _load_one_csv(config, df_h_sample, "hotel_sample")
    print(df_h_sample.show(5))

    # sampling data for weather with coordinates in range (45, 8)-(46, 10) for year 2017, month 8
    df_w = spark.read.option("header", True).parquet(f"{config.get('source_data_path')}/weather")
    df_w_sample = df_w \
        .filter(df_w.lat > 45.0) \
        .filter(df_w.lat < 46.0) \
        .filter(df_w.lng > 8.0) \
        .filter(df_w.lng < 10.0) \
        .filter(df_w.year == 2017) \
        .filter(df_w.month == 8)
    _load_one_csv(config, df_w_sample, "weather_sample")
    df_w_sample.show(5)
    