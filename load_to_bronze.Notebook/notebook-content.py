# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
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
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
## create a schema 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # **Ingest all the files into the bronze tables**

# CELL ********************

import re

schema = "bronze"
source_path = "Files"

# Create the bronze schema if it does not exist
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")

# Get all folders under Files
folders = [
    item for item in mssparkutils.fs.ls(source_path)
    if item.isDir
]

for folder in folders:

    # Find CSV files inside the current folder
    csv_files = [
        item for item in mssparkutils.fs.ls(folder.path)
        if not item.isDir and item.name.lower().endswith(".csv")
    ]

    for file in csv_files:

        # Create the table name from the CSV filename
        table_name = re.sub(
            r"[^a-zA-Z0-9_]",
            "_",
            file.name.rsplit(".", 1)[0]
        ).lower()

        full_table_name = f"{schema}.{table_name}"

        # Only create the table when it does not already exist
        if not spark.catalog.tableExists(full_table_name):

            df = (
                spark.read
                .option("header", "true")
                .option("inferSchema", "true")
                .csv(file.path)
            )

            (
                df.write
                .format("delta")
                .mode("errorifexists")
                .saveAsTable(full_table_name)
            )

            print(f"Created: {full_table_name}")

        else:
            print(f"Skipped because table exists: {full_table_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
