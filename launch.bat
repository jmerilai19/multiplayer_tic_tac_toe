:: Build docker images
docker build ./server --tag server 
docker build ./database --tag database

:: Run docker containers 
docker run -dp 3000:5000 database
docker run -dp 5000:5000 server

:: Start two clients
start cmd /c python test_client_server.py
start cmd /c python test_client_server.py
