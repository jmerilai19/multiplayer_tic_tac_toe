# Database server running in Docker container

## Instructions

### Navigate to server folder:
```
cd database
```

### Build image:
```
docker build . --tag database
```

### Run container:
```
docker run -p 3000:5000 database
```
