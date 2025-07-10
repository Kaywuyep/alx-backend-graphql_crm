#!/bin/bash

# Customer Cleanup Script
# Deletes customers with no orders since a year ago using Django manage.py shell

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log file path
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Navigate to Django project directory (adjust path as needed)
cd /path/to/your/django/project

# Execute Django shell command to delete inactive customers
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since one year ago
inactive_customers = Customer.objects.filter(
    orders__isnull=True
).union(
    Customer.objects.exclude(
        orders__order_date__gte=one_year_ago
    )
).distinct()

# Count and delete inactive customers
deleted_count = inactive_customers.count()
inactive_customers.delete()

print(deleted_count)
")

# Log the result with timestamp
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"

# Optional: Print to console for debugging
echo "Customer cleanup completed. Deleted $DELETED_COUNT inactive customers."