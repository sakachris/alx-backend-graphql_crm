#!/bin/bash

# Define paths
LOG_FILE="/tmp/customer_cleanup_log.txt"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_ACTIVATE="$PROJECT_DIR/.crm/bin/activate"

# Activate virtual environment
source "$VENV_ACTIVATE"

# Navigate to project root
cd "$PROJECT_DIR"

# Run Django shell command
DELETED=$(python manage.py shell -c "
from datetime import datetime, timedelta
from crm.models import Customer
from django.utils import timezone

cutoff = timezone.now() - timedelta(days=365)
to_delete = Customer.objects.exclude(order__order_date__gte=cutoff).distinct()
deleted_count = to_delete.count()
to_delete.delete()
print(deleted_count)
")

# Log result
echo "[$TIMESTAMP] Deleted $DELETED inactive customers" >> "$LOG_FILE"
