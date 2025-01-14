# Databricks notebook source
# DBTITLE 1,Import Packages
from pyspark.sql import SparkSession
from pyspark.sql.functions import inline,col

# COMMAND ----------

# MAGIC %md
# MAGIC ### Files Available:
# MAGIC - schedules.json - dbfs:/FileStore/shared_uploads/brijeshpatel4547@gmail.com/Indian_Rail/schedules.json 
# MAGIC - stations.json - dbfs:/FileStore/shared_uploads/brijeshpatel4547@gmail.com/Indian_Rail/stations.json
# MAGIC - trains.json - dbfs:/FileStore/shared_uploads/brijeshpatel4547@gmail.com/Indian_Rail/trains.json

# COMMAND ----------

# MAGIC %md
# MAGIC # Perform Below Tasks on the Data
# MAGIC - > Reading JSON Data Files into dataframe and apply transformations as per the requirement to make to Structered Data.
# MAGIC - > List their columns to understand the structure of each dataframe.

# COMMAND ----------

# MAGIC %md 
# MAGIC > **schedules.json - Normal JSON File Has info about the schedule of trains**

# COMMAND ----------

# DBTITLE 1,Read Schedules Data
# Import schedules.json file
schedules_df = spark.read.option("multiline","true").json("dbfs:/FileStore/shared_uploads/brijeshpatel4547@gmail.com/Indian_Rail/schedules.json")
schedules_df.columns

# COMMAND ----------

# MAGIC %md
# MAGIC > **stations.json - GeoJSON file including information of Stations in India**

# COMMAND ----------

# DBTITLE 1,Read and Trasnform Statiosn data
#Importing stations.json file
stations_df = spark.read.option("multiline","true").json("dbfs:/FileStore/shared_uploads/brijeshpatel4547@gmail.com/Indian_Rail/stations.json")
print("**********************************************************************************************************")
print("Schema Before Transformation:")
stations_df.printSchema()
print()
print("**********************************************************************************************************")


# As we have array of structs we can simplify this using inline transformation.
stations_df = stations_df.select(
    inline(col("features"))
).drop("type")
print("Schema After Inline Trasnformation:")
stations_df.printSchema()
print()
print("**********************************************************************************************************")

# Now from the schema of the stations we can now identify the features required and export them to our final dataframe.


stations_df = stations_df.select(
    col("properties.code").alias("Stn_Code"),
    col("properties.name").alias("Stn_Name"),
    col("geometry.coordinates").alias("Stn_Coordinates"),
    col("properties.address").alias("Address"),
    col("properties.state").alias("Stn_State"),
    col("properties.zone").alias("Stn_Zone")
)

print("Final Schema:")
stations_df.printSchema()
print()
print("**********************************************************************************************************")
print()


print("Sample Data: ")
stations_df.show(n=5,truncate=False)



# COMMAND ----------

# MAGIC %md
# MAGIC > trains.json - GeoJSON file including information about train routes.

# COMMAND ----------

#Importing trains.json file
trains_df = spark.read.option("multiline","true").json("dbfs:/FileStore/shared_uploads/brijeshpatel4547@gmail.com/Indian_Rail/trains.json")
print("**********************************************************************************************************")
print("Schema Before Transformation:")
trains_df.printSchema()
print()
print("**********************************************************************************************************")


# As we have array of structs we can simplify this using inline transformation.
trains_df = trains_df.select(
    inline(col("features"))
).drop("type")
print("Schema After Inline Transformation:")
trains_df.printSchema()
print()
print("**********************************************************************************************************")

# Now from the schema of the trains we can now identify the features required and export them to our final dataframe and cast them into required data types.
#Note: Uncasted columns are already in th required formats
trains_df = trains_df.select(
    col("properties.number").alias("Train_Number").cast("long"), 
    col("properties.return_train").alias("Return_Train_Number").cast("long"),
    col("properties.name").alias("Train_Name"),
    col("properties.from_station_code").alias("From_Stn_Code"),
    col("properties.from_station_name").alias("From_Stn_Name"),
    col("properties.to_station_code").alias("To_Stn_Code"),
    col("properties.to_station_name").alias("To_Stn_Name"),
    col("properties.arrival").alias("Arrival"),
    col("properties.departure").alias("Departure"),
    col("properties.distance").alias("Distance"),
    col("properties.duration_h").alias("Duration_Hrs"),
    col("properties.duration_m").alias("Duration_Mins"),
    col("properties.classes").alias("Classes"),
    col("properties.first_class").alias("First_Class").cast("boolean"),
    col("properties.chair_car").alias("Chair_car").cast("boolean"),
    col("properties.first_ac").alias("First_Ac").cast("boolean"),
    col("properties.second_ac").alias("Second_AC").cast("boolean"),
    col("properties.third_ac").alias("Third_AC").cast("boolean"),
    col("properties.sleeper").alias("Sleeper").cast("boolean"),
    col("properties.type").alias("Type"),
    col("properties.zone").alias("Zone"),
    col("geometry.coordinates").alias("Coordinates")  
)

print("Final Schema:")
trains_df.printSchema()
print()
print("**********************************************************************************************************")
print()


print("Sample Data: ")
trains_df.show(n=5,truncate=False)

# COMMAND ----------


