# PySpark Snippets

 # # Import data types and functions
 # import pyspark.sql.types as T
 # import pyspark.sql.functions as F
 # from pyspark.sql import Window
 
 # Read parquet folder
 # df_con = spark.read.load(PATH, format='parquet')
 
 # Display
 # display(df_con.limit(5))
 
 # Show
 # df_con.limit(5).show()
 # df.show(20, truncate=False) # Do not limit the size of the columns
 
 # Select distinct values
 # df_con.select(F.lower(df_con['Contract_status'])).distinct().show()
 
 # Filter data
 # df_con = df_con.filter(F.year(df_con['Contract_created']) > 2019)
 # df_con = df_con.filter(F.lower(df_con['Contract_status']) == 'processed')
 
 # Convert to pandas
 # df_con_pd = df_con.toPandas()
 
 # Convert UTC timestamp to a different Timezone
 # df_crc = df_crc.withColumn('Contract_created_CEST', F.from_utc_timestamp(F.col('Contract_created'), "Europe/Amsterdam")) 
 
 # drop/remove a column from pyspark dataframe
 # df = df.drop('ColumnName')
 # df = df.drop(df.ColumnName)
 # df = df.drop(F.col('ColumnName'))
 # # Drop multiple columns
 # df = df.drop('col1', 'col2')
 # df = df.drop(*['col1', 'col2'])
 
 # Save DataFrame to location
 # df.write.mode("overwrite").parquet(PATH)
 
 # Convert column
 # for column in ['Amount_1', 'Amount_2']:
 #     df_spark = df_spark.withColumn(column, df_spark[column].cast(T.DoubleType()))
 
 # Convert date column with specific format
 # df_spark_full = df_spark_full.withColumn('DateModif', F.to_date(df_spark_full['DateModif'], format = 'yyyy-MM-dd'))
 
 # Replace NaN with None/NULL:
 # for s in df_pyspark.schema:
 #    if s.dataType == T.StringType():
 #         df_pyspark = df_pyspark.withColumn(s.name, F.when(df_pyspark[s.name] == 'NaN', None).otherwise(df_pyspark[s.name]))
 
 # Group By:
 # df_check = df_check.groupBy(row['primaryKeys']).count()
 
 # AnalysisException error:
 # import pyspark.sql.utils
 # try:
 #         df_check = spark.read.load(path, format='parquet')
 #     except pyspark.sql.utils.AnalysisException:
 
 # String split
 # split_col_1 = F.split(df_spark_full['DateModif'], '/SolarPanelPrices/')
 # split_col_2 = F.split(split_col_1.getItem(1), '%20-%20')
 # df_spark_full = df_spark_full.withColumn('DateModif2', split_col_2.getItem(0))
 # df_spark_full.select('DateModif2').show(5, truncate=False)
 
 # Replace characters
 # df_spark_full = df_spark_full.withColumn(col, F.regexp_replace(col, '€', ''))
 # df_spark_full = df_spark_full.withColumn(col, F.regexp_replace(col, '.', ''))
 # df_spark_full = df_spark_full.withColumn(col, F.regexp_replace(col, ',', '.'))
 
 # Sort values
 # df_price = df_price.orderBy(['Count', 'DateModif'])
 
 # Drop duplicated values
 # df_prod_dedup = df_prod.dropDuplicates()
 
 # Filter dataframe based on column
 # df_check.where(F.col('count') > 1)
 
 # Add current timestamp (datetime now) on pyspark dataframe
 # df_prod = df_prod.withColumn('DateModified', F.current_timestamp())
 
 # Get a list of values based on a column
 # excluded_ids = [row[0] for row in df_3y_f_m_broken.select("Contract_id").collect()]
 
 # Row number | Partition By | Cumcount on pandas
 # window_spec = Window.partitionBy('Contract_emailaddresses').orderBy('Contract_created')
 # df = df.withColumn('contract_number', F.row_number().over(window_spec))
 
 # Calculate the difference between two datetime columns in days
 # df_3y_f_m = df_3y_f_m.withColumn("Contract_Duration_End", F.datediff(col("Contract_created_new"), col("Contract_created")))
 
 # Multiple when clausules and otherwhise:
 # df_3y_f_m = df_3y_f_m.withColumn(
 #     "Flag_Broken_Contracts", 
 #     when(
 #         (col("Contract_Duration_End") > 1) &\
 #         (col("Contract_Duration_End") < 30), 
 #         1).otherwise(0)
 # )
 
 # Fillna
 # df_final = df_final.fillna(0, subset=['converted']) # Subset is the column names
 
 # Save to csv in one single file (it will still create a folder with a random file name)
 # df_gb.coalesce(1).write.mode('overwrite').csv('abfss://test@bcdatahubdevdls.dfs.core.windows.net/sandbox/JulioVince/Bellen_Data_MB_Traffic_gb', header='true')
 
 # Save to one CSV file using pandas
 # df_pandas = df_final.toPandas()
 # df_pandas.to_csv('abfss://test@bcdatahubdevdls.dfs.core.windows.net/sandbox/JulioVince/bellen_mb.csv', index=False)