#!/bin/bash

# Customer Cleanup Script
# Deletes customers with no orders since a year ago using Django manage.py shell

# Get script directory (using ${BASH_SOURCE[0]})
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cwd=$(pwd)  # Capture current working directory before changing

# Move to Django project root (assumed 2 levels above crm/)
cd "$SCRIPT_DIR/../.."

# Get timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Check for manage.py
if [ ! -f "manage.py" ]; then
  echo "[$TIMESTAMP] ERROR: manage.py not found in $(pwd)" >> "$LOG_FILE"
  exit 1
else
  # Run Django shell command to delete inactive customers
  DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.filter(
    orders__isnull=True
).union(
    Customer.objects.exclude(
        orders__order_date__gte=one_year_ago
    )
).distinct()

count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

  echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers (called from $cwd)" >> "$LOG_FILE"
  echo "Customer cleanup completed. Deleted $DELETED_COUNT inactive customers."
fi
