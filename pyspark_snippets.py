import pyspark
  
# importing sparksession from pyspark.sql module
from pyspark.sql import SparkSession
  
# creating sparksession and giving an app name
spark = SparkSession.builder.appName('sparkdf').getOrCreate()

# Read all the csv files and combine in one df
df = spark.read.load('data/*.csv', format='csv')

# Read a simple csv file
df1 = spark.\
      read.\
      format("csv").\
      option("header", "true").\
      load("dbfs:/FileStore/shared_uploads/julio.vince@hotmail.com/products.csv")
      
# Show content. Used in Databricks
# Can creat visualizations on spot
# display(df1)

# Save as a SQL table
df1.write.saveAsTable("Products")

# Can run a SQL script using the magic %sql on a cell
# Single cell:

# %sql

# SELECT

#   ProductName
# , ListPrice

# FROM products

# WHERE Category = 'Touring Bikes';

# defining a schema:
from pyspark.sql.types import *
from pyspark.sql.functions import *

orderSchema = StructType([
     StructField("SalesOrderNumber", StringType()),
     StructField("SalesOrderLineNumber", IntegerType()),
     StructField("OrderDate", DateType()),
     StructField("CustomerName", StringType()),
     StructField("Email", StringType()),
     StructField("Item", StringType()),
     StructField("Quantity", IntegerType()),
     StructField("UnitPrice", FloatType()),
     StructField("Tax", FloatType())
 ])

df = spark.read.load('/data/*.csv', format='csv', schema=orderSchema)
# display(df.limit(100))

# View the schema of a dataframe
df.printSchema()

# Common data analyzis tools are similar to pandas

# Filtering Data
customers = df['CustomerName', 'Email'] # single brackets
print(customers.count())
print(customers.distinct().count())
# display(customers.distinct())

# Aggregate and group
productSales = df.select("Item", "Quantity").groupBy("Item").sum()
# display(productSales)

yearlySales = df.select(year("OrderDate").alias("Year")).groupBy("Year").count().orderBy("Year")
# display(yearlySales)

# Create a temp view to work with SQL
df.createOrReplaceTempView("salesorders")
spark_df = spark.sql("SELECT * FROM salesorders")
# display(spark_df)

# Run sql cell
# %sql
 
# SELECT YEAR(OrderDate) AS OrderYear,
#     SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue
# FROM salesorders
# GROUP BY YEAR(OrderDate)
# ORDER BY OrderYear;

# Can run visualization AND data profile on spot on databrick notebooks

# Visualization with Matplotlib
sqlQuery = "SELECT CAST(YEAR(OrderDate) AS CHAR(4)) AS OrderYear, \
             SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue \
         FROM salesorders \
         GROUP BY CAST(YEAR(OrderDate) AS CHAR(4)) \
         ORDER BY OrderYear"
df_spark = spark.sql(sqlQuery)
df_spark.show()

from matplotlib import pyplot as plt

# matplotlib requires a Pandas dataframe, not a Spark one
df_sales = df_spark.toPandas()

# Create a bar plot of revenue by year
plt.bar(x=df_sales['OrderYear'], height=df_sales['GrossRevenue'])

# Display the plot
plt.show()

### Delta lake

# Load a file into a dataframe
df = spark.read.load('/data/mydata.csv', format='csv', header=True)

# Save the dataframe as a delta table
delta_table_path = "/delta/mydata"
df.write.format("delta").save(delta_table_path)

# Replace existing Delta Lake table with the contents of a dataframe. Overwrite method.
new_df.write.format("delta").mode("overwrite").save(delta_table_path)

# Add new rows to a table
new_rows_df.write.format("delta").mode("append").save(delta_table_path)

# Conditional updates:
from delta.tables import *
from pyspark.sql.functions import *

# Create a deltaTable object
deltaTable = DeltaTable.forPath(spark, delta_table_path)

# Update the table (reduce price of accessories by 10%)
deltaTable.update(
    condition = "Category == 'Accessories'",
    set = { "Price": "Price * 0.9" })

# Time travel:
df = spark.read.format("delta").option("versionAsOf", 0).load(delta_table_path)

df = spark.read.format("delta").option("timestampAsOf", '2022-01-01').load(delta_table_path)

# Catalog tables

# Save a dataframe as a managed table
df.write.format("delta").saveAsTable("MyManagedTable")

## specify a path option to save as an external table
df.write.format("delta").option("path", "/mydata").saveAsTable("MyExternalTable")

# Using SQL
spark.sql("CREATE TABLE MyExternalTable USING DELTA LOCATION '/mydata'")

%sql
CREATE TABLE MyExternalTable # Can also use CREATE TABLE IF NOT EXISTS or CREATE OR REPLACE TABLE
USING DELTA
LOCATION '/mydata'

# Creating table with a defined schema
%sql
CREATE TABLE ManagedSalesOrders
(
    Orderid INT NOT NULL,
    OrderDate TIMESTAMP NOT NULL,
    CustomerName STRING,
    SalesTotal FLOAT NOT NULL
)
USING DELTA

# DeltaTableBuilder API
from delta.tables import *

# can also use createIfNotExists or createOrReplace
DeltaTable.create(spark) \ 
  .tableName("default.ManagedProducts") \
  .addColumn("Productid", "INT") \
  .addColumn("ProductName", "STRING") \
  .addColumn("Category", "STRING") \
  .addColumn("Price", "FLOAT") \
  .execute()

# Streaming data

from pyspark.sql.types import *
from pyspark.sql.functions import *

# Load a streaming dataframe from the Delta Table
stream_df = spark.readStream.format("delta") \
    .option("ignoreChanges", "true") \
    .load("/delta/internetorders")

# Now you can process the streaming data in the dataframe
# for example, show it:
stream_df.show()

# Delta lake Streaming Sink (Destination)

from pyspark.sql.types import *
from pyspark.sql.functions import *

# Create a stream that reads JSON data from a folder
streamFolder = '/streamingdata/'
jsonSchema = StructType([
    StructField("device", StringType(), False),
    StructField("status", StringType(), False)
])
stream_df = spark.readStream.schema(jsonSchema).option("maxFilesPerTrigger", 1).json(inputPath)

# Write the stream to a delta table
table_path = '/delta/devicetable'
checkpoint_path = '/delta/checkpoint'
delta_stream = stream_df.writeStream.format("delta").option("checkpointLocation", checkpoint_path).start(table_path)

# Query the stream data from Data lake
%sql

CREATE TABLE DeviceTable
USING DELTA
LOCATION '/delta/devicetable';

SELECT device, status
FROM DeviceTable;

# Stop the stream
delta_stream.stop()