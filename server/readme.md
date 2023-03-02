# Game logic server running in Docker container

## Instructions

### Navigate to server folder:
```
cd server
```

### Build image:
```
docker build . --tag server
```

### Run container:
```
docker run -p 5000:5000 server 
```
