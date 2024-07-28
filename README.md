# retail-store-management
online retail store management 


# to create docker image
docker build -t retail-store .

# to run docker container with local creds
docker-compose up -d DATABASE_URL=postgresql://root:root@host:5432/retail_db

# to run via virtual env

create virtual env 
pip install -r requirements.txt

activate venv

to run server:
uvicorn app:app --reload

to run test case: 
run this command ./local_test.sh (make sure venv activated)

# db model 
<img width="353" alt="Screenshot 2024-07-28 at 10 24 44 PM" src="https://github.com/user-attachments/assets/c0e7ab63-4891-431d-b305-eefb0ae84148">

# refer this doc for request response 
https://docs.google.com/document/d/1CsShthNPHhCaGQQ511NqqeZ4oyXpuK52-dhtqWRmPu0/edit

# refer this postman collection for apis
https://go.postman.co/workspace/My-Workspace~e47e31a8-192a-4906-8804-9f21a733b534/collection/19580116-e5f7870e-2de5-4741-99fd-d711f5293774?action=share&creator=19580116
