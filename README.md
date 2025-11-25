Clone repo:
```sh
git clone https://github.com/holodnyisiemens/python-web-app.git
```

```sh
cd python-web-app
```

Rename file (without editing):
```sh
mv .env.example .env
```

Start app and PostgreSQL instance:
```sh
docker compose up -d
```

Wait for start:
```sh
docker ps
```

Test API using:
1. http://localhost:8888/schema/swagger
2. curl
3. etc.

Deleting all Docker objects from docker-compose.yaml including containers, volumes and images:
```sh
docker compose down -v --rmi all
```
