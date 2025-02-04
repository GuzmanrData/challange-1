# 📌 Levantar el proyecto en local

## 🚀 Clonar el repositorio
```bash
git clone https://github.com/GuzmanrData/challange-1.git
```

## 📂 Entrar en la carpeta del proyecto
```bash
cd challange-1
```

## 🐳 Levantar los contenedores con Docker (asegúrate de tener Docker ejecutándose en local)
```bash
docker-compose up -d
```

---

## 🛠️ Crear la base de datos
Ejecuta el siguiente comando para inicializar la base de datos con las tablas necesarias:
```bash
docker exec -it postgres_db psql -U user -d coding_challenge -f /docker-entrypoint-initdb.d/init.sql
```

---

## 🔍 Probar conexión a la base de datos
Para verificar que la base de datos está funcionando correctamente, puedes llamar al siguiente endpoint:
```
http://localhost:8000/healthcheck
```
Si todo está correctamente configurado, deberías recibir la siguiente respuesta:
```json
{
    "message": "Database connection successful"
}
```
✅ ¡Listo! Ahora puedes comenzar a trabajar con el proyecto. 🚀

---

## 📥 Cargar datos en la base de datos

### 1️⃣ Cargar datos históricos desde archivos CSV
Para cargar datos en formato CSV en la base de datos PostgreSQL, llama al siguiente endpoint:
```
http://localhost:8000/batch-load-historical-data
```

En el cuerpo de la solicitud (`body`), proporciona la información de los archivos CSV a cargar:
```json
[
   {
        "input_path": "landing/departments_2024-12-31.csv",
        "schema_path": "schemas/department_schema.json",
        "table_name": "departments",
        "process_date": "2024-12-31"
    },
    {
        "input_path": "landing/jobs_2024-12-31.csv",
        "schema_path": "schemas/jobs_schema.json",
        "table_name": "jobs",
        "process_date": "2024-12-31"
    },
    {
        "input_path": "landing/hired_employees_2024-12-31.csv",
        "schema_path": "schemas/employees_schema.json",
        "table_name": "hired_employees",
        "process_date": "2024-12-31"
    }
]
```

### 2️⃣ Insertar nuevos registros en la base de datos
Para insertar nuevos registros en lote, llama al siguiente endpoint:
```
http://localhost:8000/insert-batch/
```

El cuerpo de la solicitud debe tener la siguiente estructura:
```json
{
    "departments": [
        { "department": "IT" },
        { "department": "HR 3" },
        { "department": "HR 2" },
        { "department": "HR 4" }
    ],
    "jobs": [
        { "job": "Software Engineer 2" }
    ],
    "hired_employees": [
        {
            "name": "John Doe",
            "datetime": "2024-01-01T09:00:00",
            "department_id": 1,
            "job_id": 1
        },
        {
            "name": "Carlos Guzmán",
            "datetime": "2024-01-01T09:00:00",
            "department_id": 1,
            "job_id": 1
        }
    ]
}
```

### 3️⃣ Generar un backup de la base de datos
Para generar una copia de seguridad de las tablas en formato Parquet, llama al siguiente endpoint:
```
http://localhost:8000/backup/
```
El sistema creará una versión de las tablas en formato Parquet, particionándolas por la marca de tiempo de la ejecución.

### 4️⃣ Restaurar un backup
Para restaurar los datos de una tabla desde un backup, usa el siguiente endpoint:
```
http://localhost:8000/restore
```

En el cuerpo de la solicitud, proporciona la información de la tabla que deseas restaurar:
```json
{
    "table_name": "departments",
    "backup_timestamp": "20250202_214259"
}
```

### 5️⃣ Generar reportes
El sistema cuenta con dos endpoints para generar reportes sobre los datos almacenados:

📊 **Reporte de empleados contratados por trimestre y departamento**
```
http://localhost:8000/hired-employees-report
```

📈 **Reporte de departamentos con contrataciones por encima del promedio**
```
http://localhost:8000/departments-above-mean
```

✅ ¡Ahora el sistema está listo para gestionar y analizar los datos de empleados de forma eficiente! 🚀

