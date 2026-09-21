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
# META     }
# META   }
# META }

# CELL ********************

df = spark.read.option("multiline", "true").json("Files/script.json")
# df now is a Spark DataFrame containing JSON data from "Files/script.json".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

mssparkutils.fs.ls("Files")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

files = mssparkutils.fs.ls("Files")
for f in files:
    print(f.name, f.size)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.read.text("Files/script.json").show(50, truncate=False)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = (
    spark.read
         .option("multiline", "true")
         .json("Files/script.json")
)

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.read.option("multiline","true").json("Files/script.json").show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
