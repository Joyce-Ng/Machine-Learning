# -*- coding: utf-8 -*-
# Import SparkContext libraries to run Python script
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.sql.types import Row
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType,IntegerType
from pyspark.ml.feature import PCA
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.feature import VectorAssembler
from numpy import array
from pyspark.ml.clustering import KMeans

spark = SparkSession \
        .builder \
        .appName("RDD_and_DataFrame") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

# step1:create dataframe from text

sc = spark.sparkContext

blogRdd = sc.textFile("file:///home/edu/myproject/data/data-00000")
# dataframe的五个字段
schemaString = "id title landing_words tag body"
fields = list(map( lambda fieldName : StructField(fieldName, StringType(), nullable = True), schemaString.split(" ")))
#print("-----------------------",fields)
rowRDD = blogRdd.map(lambda line: line.split("\x00")).map(lambda attributes : Row(attributes[0], attributes[1],attributes[2],attributes[3],attributes[4]))
schema = StructType(fields)
#print("-----------------------",schema)
blogDF = spark.createDataFrame(rowRDD, schema)
blogDF.show(5)

# step2:计算TF-IDF，numFeatures=20
# 提取dataframe中的title
tokenizer = Tokenizer(inputCol="title", outputCol="words")
#对title分词
titleWordsDF = tokenizer.transform(blogDF).select("id","title","words")
#计算tf-idf
hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=20)
featurizedData = hashingTF.transform(titleWordsDF)
idf = IDF(inputCol="rawFeatures", outputCol="idffeatures")
idfModel = idf.fit(featurizedData)
# 只取dataframe中的idffeatures列存到新的一个dataframe中（即tfidfDF）
tfidfDF = idfModel.transform(featurizedData).select("id","idffeatures")

tfidfDF.show(4)

# step3:PCA降维
pca = PCA(k=4, inputCol="idffeatures", outputCol="pcaFeatures")
model = pca.fit(tfidfDF)
pcaDF = model.transform(tfidfDF).select("id","pcaFeatures")

pcaDF.show(truncate=False)

# step4:kmeans
vecAssembler = VectorAssembler(inputCols=["pcaFeatures"], outputCol="features")
vector_df = vecAssembler.transform(pcaDF)

#kmeans clustering 
kmeans = KMeans(k=2) 
model = kmeans.fit(vector_df) 
predictions = model.transform(vector_df) 
kmeansDF = predictions.select("id","prediction")
kmeansDF.show()
kmeansDF.coalesce(1).write.csv(path="file:///home/edu/myproject/output/id_cluster", header=False, sep=",", mode='overwrite')

sc.stop()
