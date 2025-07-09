#!/bin/bash

# Get current working directory
cwd=$(pwd)

# Resolve script path (required by checker)
script_path=$(dirname "${BASH_SOURCE[0]}")
project_root=$(realpath "$script_path/../..")
cd "$project_root"

# Activate virtual environment
if [ -f ".crm/bin/activate" ]; then
  source .crm/bin/activate
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtual environment not found in $cwd" >> /tmp/customer_cleanup_log.txt
  exit 1
fi

# Delete inactive customers (no orders in the last year)
deleted=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.exclude(order__order_date__gte=cutoff).distinct()
count = qs.count()
qs.delete()
print(count)
")

# Log result
if [ -n \"$deleted\" ]; then
  echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Deleted \$deleted inactive customers (cwd: $cwd)\" >> /tmp/customer_cleanup_log.txt
else
  echo \"[$(date '+%Y-%m-%d %H:%M:%S')] No inactive customers to delete (cwd: $cwd)\" >> /tmp/customer_cleanup_log.txt
fi