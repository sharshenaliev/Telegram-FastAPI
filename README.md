# Usage

An overview of the project.

## Env configuration

Create `.env` file and fill data:

```shell
POSTGRES_DB=test
POSTGRES_USER=test
POSTGRES_PASSWORD=test
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
TOKEN=<telegram_token>
ADMIN_LOGIN=admin
ADMIN_PASSWORD=admin
```

## Instructions on how to build and run your application using Docker Compose

1. Run Docker Compose command:

    ```
    docker-compose up -d --build
    ```


## Work with app

Admin panel `http://localhost:8000/admin`. 
