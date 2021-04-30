from pyspark.sql.functions import udf, struct
from pyspark.sql.types import IntegerType
from pyspark.sql import *

spark = SparkSession.builder.getOrCreate()
df = spark.createDataFrame([(None, None), (1, None), (None, 2)], ("a", "b"))
count_empty_columns = udf(lambda row: len([x for x in row if x == None]), IntegerType())

new_df = df.withColumn("null_count", count_empty_columns(struct([df[x] for x in df.columns])))

new_df.show()