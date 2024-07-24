# retail-store-management
online retail store management 


# to create docker image
docker build -t retail-store .

# to run docker container with local creds
docker-compose up -d DATABASE_URL=postgresql://root:root@host:5432/retail_db

# to run via virtual env
uvicorn main:app --host 0.0.0.0 --port 8000
