# Usamos la imagen oficial de Apache Spark con Python
FROM apache/spark-py:latest

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Copiamos los archivos del backend
COPY . .

# Instalamos las dependencias
USER root


# Descargar el driver JDBC dentro del contenedor
RUN mkdir -p /opt/spark/jars && \
    wget -O /opt/spark/jars/postgresql-42.5.0.jar https://jdbc.postgresql.org/download/postgresql-42.5.0.jar

RUN pip install pyspark[sql,avro]
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip instrall avro


# Exponemos el puerto 8000 para FastAPI
EXPOSE 8000

# Ejecutamos la API con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]