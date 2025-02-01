FROM bitnami/spark:latest

# Configurar JAVA_HOME en Spark
ENV JAVA_HOME=/opt/bitnami/java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

WORKDIR /opt/spark/work-dir

CMD ["/opt/bitnami/spark/bin/spark-class", "org.apache.spark.deploy.master.Master", "--host", "spark_cluster", "--port", "7077"]
