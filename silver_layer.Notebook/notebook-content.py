# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.12"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f044b83a-efe6-422a-9522-57596a6a7471",
# META       "default_lakehouse_name": "lakehouse",
# META       "default_lakehouse_workspace_id": "21e9125c-3146-4682-b634-9a1b9f7026ee",
# META       "known_lakehouses": [
# META         {
# META           "id": "f044b83a-efe6-422a-9522-57596a6a7471"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!

from pyspark.sql import SparkSession, functions as F, Window
from pyspark.sql.types import *
from pyspark.sql.functions import *

df = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_customers LIMIT 1000")
# display(df)

# df.printSchema()
# df.columns
# df.summary().show()
cus=df.select("CustomerKey")



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # <mark>## Adventureworks_customers table for silver</mark>

# CELL ********************

spark.version

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Remove existing table to avoid schema conflicts
spark.sql("DROP TABLE IF EXISTS silver.customers")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import DecimalType

# Create Silver schema
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")

# Drop existing Silver table to avoid schema conflicts
spark.sql("DROP TABLE IF EXISTS silver.customers")

# Read Bronze table
df = spark.table("bronze.adventureworks_customers")

# Silver transformations
silver_df = (
    df
    .withColumn(
        "BirthDate",
        to_date(col("BirthDate"), "M/d/yyyy")
    )
    .withColumn(
        "AnnualIncome",
        regexp_replace(col("AnnualIncome"), "[$,]", "")
        .cast(DecimalType(18, 2))
    )
    .withColumn("Prefix", trim(col("Prefix")))
    .withColumn("FirstName", trim(col("FirstName")))
    .withColumn("LastName", trim(col("LastName")))
    .withColumn("FullName", concat_ws(" ", initcap(col("FirstName")), initcap(col("LastName"))))
    .withColumn("MaritalStatus", trim(col("MaritalStatus")))
    .withColumn("Gender", trim(col("Gender")))
    .withColumn("EmailAddress", trim(col("EmailAddress")))
    .withColumn("EducationLevel", trim(col("EducationLevel")))
    .withColumn("Occupation", trim(col("Occupation")))
    .withColumn("HomeOwner", trim(col("HomeOwner")))
    .dropDuplicates(["CustomerKey"])
)

# Check transformed schema
silver_df.printSchema()

# Write Silver table
(
    silver_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("silver.customers")
)

# Verify
display(spark.table("silver.customers"))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # <mark>Adventureworks_product_categories</mark>

# CELL ********************

df_product_categories = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_product_categories LIMIT 1000")
# display(df_product_categories)
# df_product_categories.printSchema()


if not spark.catalog.tableExists("silver.product_categories"):
    df_product_categories.write \
        .format("delta") \
        .saveAsTable("silver.product_categories")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # <mark># **product categories**</mark>

# CELL ********************

df_product_subcategories = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_product_subcategories LIMIT 1000")
display(df_product_subcategories)
df_product_subcategories.printSchema()

if not spark.catalog.tableExists("silver.product_subcategories"):
    df_product_subcategories.write.format("delta").saveAsTable("silver.product_subcategories")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # <mark># **product silver **</mark>

# CELL ********************

df_product = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_products LIMIT 1000")

df_product.printSchema()

df_product.write.format("delta").mode("overwrite").saveAsTable("silver.products")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_sales_2016 LIMIT 1000")
display(df)

df = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_sales_2017 LIMIT 1000")
display(df)

df = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_territories LIMIT 1000")
display(df)

df = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_calendar LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Sales 2016
print("=" * 80)
print("ADVENTUREWORKS_SALES_2016")
print("=" * 80)

df_sales_2016 = spark.sql("""
    SELECT * 
    FROM lakehouse.bronze.adventureworks_sales_2016
""")

display(df_sales_2016)

df_sales_2016.write.mode("overwrite").saveAsTable(
    "lakehouse.silver.adventureworks_sales_2016"
)


# Sales 2017
print("=" * 80)
print("ADVENTUREWORKS_SALES_2017")
print("=" * 80)

df_sales_2017 = spark.sql("""
    SELECT * 
    FROM lakehouse.bronze.adventureworks_sales_2017
""")

display(df_sales_2017)

df_sales_2017.write.mode("overwrite").saveAsTable(
    "lakehouse.silver.adventureworks_sales_2017"
)


# Territories
print("=" * 80)
print("ADVENTUREWORKS_TERRITORIES")
print("=" * 80)

df_territories = spark.sql("""
    SELECT * 
    FROM lakehouse.bronze.adventureworks_territories
""")

display(df_territories)

df_territories.write.mode("overwrite").saveAsTable(
    "lakehouse.silver.adventureworks_territories"
)


# Calendar
print("=" * 80)
print("ADVENTUREWORKS_CALENDAR")
print("=" * 80)

df_calendar = spark.sql("""
    SELECT * 
    FROM lakehouse.bronze.adventureworks_calendar
""")

display(df_calendar)

df_calendar.write.mode("overwrite").saveAsTable(
    "lakehouse.silver.adventureworks_calendar"
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# # <mark>**AI Generated**</mark>

# CELL ********************


df_products = spark.sql("SELECT * FROM lakehouse.bronze.adventureworks_products LIMIT 1000")
display(df_products)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
