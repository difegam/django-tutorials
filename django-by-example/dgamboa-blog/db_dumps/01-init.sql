-- Create user with password from environment variable
CREATE USER blog WITH PASSWORD 'Bl0gDj@ngo2024$';
CREATE DATABASE blog OWNER blog ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE blog TO blog;