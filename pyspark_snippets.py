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



