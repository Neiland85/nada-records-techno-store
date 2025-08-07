# Docker Development Environment

## Security Setup

⚠️ **IMPORTANT**: This project uses environment variables for sensitive configuration.

### First Time Setup

1. Copy the environment example file:
   ```bash
   cp .env.docker.example .env.docker
   ```

2. Edit `.env.docker` with secure passwords:
   ```bash
   # Use strong, unique passwords for each service
   POSTGRES_PASSWORD=your_secure_postgres_password_here
   REDIS_PASSWORD=your_secure_redis_password_here
   MINIO_ROOT_PASSWORD=your_secure_minio_password_here
   REDIS_COMMANDER_PASSWORD=your_secure_redis_commander_password_here
   ```

3. Start the development environment:
   ```bash
   docker-compose --env-file .env.docker up -d
   ```

## Services

| Service | Port | Description | Admin URL |
|---------|------|-------------|-----------|
| PostgreSQL | 5432 | Main database | - |
| Redis | 6379 | Cache & queue | - |
| MinIO | 9000/9001 | S3-compatible storage | http://localhost:9001 |
| Adminer | 8080 | Database admin | http://localhost:8080 |
| Redis Commander | 8081 | Redis admin | http://localhost:8081 |
| MailHog | 8025 | Email testing | http://localhost:8025 |

## Security Best Practices

- ✅ Never commit `.env.docker` to version control
- ✅ Use strong, unique passwords for each service
- ✅ Regularly rotate development passwords
- ✅ In production, use proper secret management
- ✅ Review Docker Compose logs for security issues

## Development Commands

```bash
# Start all services
docker-compose --env-file .env.docker up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Reset all data (⚠️ destructive)
docker-compose down -v
```

## Troubleshooting

### Environment file not found
```bash
cp .env.docker.example .env.docker
# Edit the file with your values
```

### Permission denied errors
```bash
# Fix file permissions
chmod 600 .env.docker
```
