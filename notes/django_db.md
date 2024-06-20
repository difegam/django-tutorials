https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/



```bash
docker compose exec postgres psql --username=postgres --dbname=djangodb
```
```sql
CREATE USER blog WITH PASSWORD 'xxxxxx';
CREATE DATABASE blog OWNER blog ENCODING 'UTF8';
```
