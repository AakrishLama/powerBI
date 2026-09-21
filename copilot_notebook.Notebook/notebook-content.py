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

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Read and display sample data from AdventureWorks tables
sample_tables = [
    "adventureworks_products",
    "adventureworks_customers",
    "adventureworks_calendar",
]

for table_name in sample_tables:
    print(f"Sample rows from {table_name}")
    sample_df = spark.sql(f"SELECT * FROM lakehouse.bronze.{table_name} LIMIT 10")
    display(sample_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
