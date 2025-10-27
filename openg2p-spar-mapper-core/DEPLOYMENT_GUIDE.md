# Deployment Guide

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Docker (optional)
- pip or poetry

---

## Installation

### From PyPI

```bash
pip install openg2p-spar-mapper-core
```

### From Source

```bash
git clone https://github.com/OpenG2P/openg2p-spar-mapper-api.git
cd openg2p-spar-mapper-core
pip install -e .
```

---

## Configuration

### Environment Variables

Create `.env` file:

```bash
# Database
SPAR_BENE_PORTAL_API_DB_DBNAME=openg2p_spar_db
SPAR_BENE_PORTAL_API_DB_USERNAME=postgres
SPAR_BENE_PORTAL_API_DB_PASSWORD=secure_password
SPAR_BENE_PORTAL_API_DB_HOSTNAME=localhost
SPAR_BENE_PORTAL_API_DB_PORT=5432

# API
SPAR_BENE_PORTAL_API_HOST=0.0.0.0
SPAR_BENE_PORTAL_API_PORT=8004

# Logging
LOG_LEVEL=INFO

# Environment
ENV=production
DEBUG=false
```

---

## Database Setup

### Initialize Database

```bash
# Create database
createdb openg2p_spar_db

# Run migrations
python main.py migrate
```

### Insert Sample Data

```bash
# Using SQL script
psql -h localhost -U postgres -d openg2p_spar_db -f insert_dfsp_data.sql
```

---

## Running the Application

### Development Server

```bash
uvicorn openg2p_spar_bene_portal_api.app:app --reload --host 0.0.0.0 --port 8004
```

### Production Server

```bash
gunicorn openg2p_spar_bene_portal_api.app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8004
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "openg2p_spar_bene_portal_api.app:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8004"]
```

### Build and Run

```bash
docker build -t spar-mapper-api .
docker run -p 8004:8004 \
  -e SPAR_BENE_PORTAL_API_DB_HOSTNAME=postgres \
  -e SPAR_BENE_PORTAL_API_DB_PASSWORD=password \
  spar-mapper-api
```

### Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: openg2p_spar_db
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "8004:8004"
    environment:
      SPAR_BENE_PORTAL_API_DB_HOSTNAME: postgres
      SPAR_BENE_PORTAL_API_DB_PASSWORD: password
    depends_on:
      - postgres

volumes:
  postgres_data:
```

---

## Health Checks

### Endpoint

```bash
curl http://localhost:8004/health
```

### Response

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "database": "connected"
}
```

---

## Monitoring

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics

```bash
curl http://localhost:8004/metrics
```

---

## Backup and Recovery

### Database Backup

```bash
# Full backup
pg_dump -h localhost -U postgres openg2p_spar_db > backup.sql

# Compressed backup
pg_dump -h localhost -U postgres openg2p_spar_db | gzip > backup.sql.gz
```

### Database Restore

```bash
# From SQL file
psql -h localhost -U postgres openg2p_spar_db < backup.sql

# From compressed file
gunzip -c backup.sql.gz | psql -h localhost -U postgres openg2p_spar_db
```

---

## Scaling

### Horizontal Scaling

Deploy multiple instances behind a load balancer:

```nginx
upstream spar_mapper {
    server localhost:8004;
    server localhost:8005;
    server localhost:8006;
}

server {
    listen 80;
    location / {
        proxy_pass http://spar_mapper;
    }
}
```

### Database Connection Pooling

Use PgBouncer:

```ini
# pgbouncer.ini
[databases]
openg2p_spar_db = host=localhost port=5432 dbname=openg2p_spar_db

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

---

## Security

### Database Security

```bash
# Create restricted user
createuser spar_user -P
psql -c "GRANT CONNECT ON DATABASE openg2p_spar_db TO spar_user"
psql -c "GRANT USAGE ON SCHEMA public TO spar_user"
psql -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO spar_user"
```

### API Security

- Use HTTPS in production
- Implement authentication (OAuth2, API keys)
- Add rate limiting
- Validate all inputs
- Use CORS appropriately

### Environment Security

```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use secrets management (AWS Secrets Manager, Vault, etc.)
```

---

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
psql -h localhost -U postgres -c "SELECT 1"

# Verify credentials in .env
# Check firewall rules
```

### Migration Errors

```bash
# Check existing tables
psql -h localhost -U postgres -d openg2p_spar_db -c "\dt"

# Drop and recreate if needed
python main.py migrate --reset
```

### High Memory Usage

- Reduce worker count
- Enable caching
- Optimize database queries
- Monitor with `top` or `htop`

---

## Performance Tuning

### Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_id_value ON id_fa_mapping(id_value);
CREATE INDEX idx_fa_value ON id_fa_mapping(fa_value);
CREATE INDEX idx_active ON id_fa_mapping(active);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM id_fa_mapping WHERE id_value = 'ID123';
```

### Application Optimization

- Enable caching
- Use connection pooling
- Optimize queries
- Batch operations
- Use async operations

---

## Maintenance

### Regular Tasks

- Monitor disk space
- Review logs
- Update dependencies
- Run backups
- Test disaster recovery

### Dependency Updates

```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade openg2p-spar-mapper-core

# Update all
pip install --upgrade -r requirements.txt
```

---

## Rollback Procedures

### Application Rollback

```bash
# Revert to previous version
pip install openg2p-spar-mapper-core==1.0.0

# Restart application
systemctl restart spar-mapper-api
```

### Database Rollback

```bash
# Restore from backup
psql -h localhost -U postgres openg2p_spar_db < backup.sql
```

---

## Compliance and Auditing

### Audit Logging

```python
# Log all database changes
@event.listens_for(IdFaMapping, "after_insert")
def receive_after_insert(mapper, connection, target):
    _logger.info(f"Created mapping: {target.id_value} -> {target.fa_value}")
```

### Data Retention

```python
# Archive old records
DELETE FROM id_fa_mapping 
WHERE updated_at < NOW() - INTERVAL '1 year'
AND active = false;
```

---

## Deployment Checklist

- [ ] Database configured and initialized
- [ ] Environment variables set
- [ ] Application running successfully
- [ ] Health check passing
- [ ] Backups configured
- [ ] Monitoring enabled
- [ ] Security measures implemented
- [ ] Team trained on operations
- [ ] Disaster recovery tested

---

**Last Updated**: October 2024
**Version**: 1.0.0

