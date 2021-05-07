
import pyspark
from pyspark import SQLContext
from pyspark.sql.types import *


sc = pyspark.SparkContext()
sql = SQLContext(sc)
a=['A', 'B']
b=['-12', '16']
outSchema = StructType([StructField("Result",  StringType(), True), StructField("Result_Value",  StringType(), True)])    
sql.createDataFrame(zip(a, b), schema=outSchema).show()


sql.createDataFrame(zip(a, b), schema=(StructType([StructField("Result1", StringType(),True),StructField("Result1_Value",StringType(),True)]))).show()
