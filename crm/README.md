# CRM Celery Report Setup

## Prerequisites

- Install Redis:

```bash
sudo apt update
sudo apt install redis-server

# migrate first
celery -A crm worker -l info --pool=solo
celery -A crm beat -l info
```