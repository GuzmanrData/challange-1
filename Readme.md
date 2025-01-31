# 📌 Levantar el proyecto en local

## 🚀 Clonar el repositorio
```bash
git clone https://github.com/GuzmanrData/challange-1.git
```

## 📂 Entrar en la carpeta del proyecto
```bash
cd challange-1
```

## 🐳 Levantar los contenedores con Docker (asegúrate de tener Docker corriendo en local)
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
Llamar al endpoint de verificación de conexión:
```
http://localhost:8000/healthcheck
```

Deberíamos obtener la siguiente respuesta:
```json
{
    "message": "Database connection successful"
}
```

✅ ¡Listo! Ahora puedes comenzar a trabajar con el proyecto. 🚀

