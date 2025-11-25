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

Test API using:
1. http://localhost:8888/schema/swagger
2. curl
3. etc.