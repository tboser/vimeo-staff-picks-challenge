# Vimeo Staff Picks Challenge

#### Requirements:
docker, docker-compose: https://www.docker.com/get-started  
1.5GB memory for docker images


### Installation and Use:

```bash
git clone https://github.com/tboser/vimeo-staff-picks-challenge
cd vimeo-staff-picks-challenge
docker-compose up --build -d
```    
The docker containers can be shut down with the command:  
```bash
docker-compose down -v
```

#### Web interface:
After completing the installation the web app will be running at:  
<http://0.0.0.0:5000>  

  

#### Command line interface:
To access CLI from docker container:  
```bash
docker exec -ti flask-app /bin/bash
```
You can also access the CLI from your own workspace if you install dependencies (requirements.txt), and have python 3.6 installed.

IMPORTANT: when using the CLI from the docker container always pass argument ```-o elasticsearch ``` in order to specify the ES host name (which is not localhost from the docker container).

##### CLI Usage:
```
usage: main.py [-h] [-f] [-p PATH] [-s] [-n MODEL_NAME] [-l] [-o HOST]
               [<clip id>]

Find clips similar to clip_id.

positional arguments:
  <clip id>

optional arguments:
  -h, --help            show this help message and exit
  -f, --fillIndex       Fill ES index with staff pick data.
  -p PATH, --dataPath PATH
                        Set base path to staff picks directory.
  -s, --saveModel       Create snapshot of clips index.
  -n MODEL_NAME, --modelName MODEL_NAME
                        Specify snapshot name when saving/loading.
  -l, --loadModel       Restore a snapshot of clips index.
  -o HOST, --hostName HOST
                        Set elasticsearch host name.
```

If you haven't populated the ES index (when you first run the program), you need to use the ```-l``` flag in order to specify the need to populate the index. The ```-f``` flag also works, but takes longer because it builds the index from the csv data.   

##### Example:  
```python main.py -l 250482473```  