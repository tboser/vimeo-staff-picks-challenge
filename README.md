# Vimeo Staff Picks Challenge
Thomas Boser  
  
Project in development.  


### TO USE:  
docker-compose up --build -d  
go to http://0.0.0.0:5000  
enter clip ID  
#### TO CLOSE DOCKER CONTAINERS:
docker-compose down -v
  

#### Command line interface:
To access without dependencies:  
docker exec -ti <container id (check docker ps)> /bin/bash  

usage: main.py [-h] [-f] [-p PATH] <clip id>

Find similar clips from clip id.

positional arguments:
  <clip id>

optional arguments:
  -h, --help            show this help message and exit  
  -f, --fillIndex       Fill ES index with staff pick data.  
  -p PATH, --dataPath PATH  
                         Set base path to staff picks directory.
