from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import sys


spark = SparkSession.builder.appName(
    "Counting word occurences from a book."
).getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# If you need to read multiple text files, replace `1342-0` by `*`.
def read_word_count(file):
    results = (
        spark.read.text(file)
        .select(F.split(F.col("value"), " ").alias("line"))
        .select(F.explode(F.col("line")).alias("word"))
        .select(F.lower(F.col("word")).alias("word"))
        .select(F.regexp_extract(F.col("word"), "[a-z']*", 0).alias("word"))
        .where(F.col("word") != "")
        .distinct()
        # .groupby(F.col("word"))
        .count()
    )

    results.orderBy("count", ascending=False).show(10)
    results.coalesce(1).write.csv("./results_single_partition.csv")
    return "success!"

if __name__ == '__main__':
    files = sys.argv[1]
    read_word_count(files)
