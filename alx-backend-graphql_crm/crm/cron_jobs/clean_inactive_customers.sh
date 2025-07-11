#!/bin/bash

# Customer Cleanup Script
# Deletes customers with no orders since a year ago using Django manage.py shell

# Resolve script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log file path
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Navigate to Django project root (contains manage.py)
cd "$PROJECT_ROOT"

# Check if we're in the correct directory
if [ ! -f "manage.py" ]; then
  echo "[$TIMESTAMP] Error: manage.py not found in $PROJECT_ROOT" >> "$LOG_FILE"
  exit 1
else
  # Execute Django shell command to delete inactive customers
  DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since a year ago
inactive_customers = Customer.objects.filter(
    orders__isnull=True
).union(
    Customer.objects.exclude(
        orders__order_date__gte=one_year_ago
    )
).distinct()

# Count and delete
count = inactive_customers.count()
inactive_customers.delete()

print(count)
")

  # Log the result
  echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"
  echo "Customer cleanup completed. Deleted $DELETED_COUNT inactive customers."
fi
