# 📊 Django CRM Backend with Celery, Redis & GraphQL

This project is a backend CRM system using Django with Celery for background task processing, Redis as the broker, and GraphQL for data queries.

## 🚀 Features

- Weekly CRM report generation via Celery Beat
- Integration with external GraphQL API using `gql`
- Background processing using Celery
- Redis as Celery broker

---

## 🧰 Tech Stack

- **Django**
- **Celery**
- **Redis**
- **gql** for GraphQL API access
- **requests / requests-toolbelt**

---

## ⚙️ Setup Instructions (Windows)

```bash
# in linux environment
sudo apt update
sudo apt install redis-server
sudo service redis-server start

# migrate first
celery -A crm worker -l info --pool=solo
celery -A crm beat -l info
```