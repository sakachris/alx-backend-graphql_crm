#!/bin/bash

# Navigate to project root
cwd=$(dirname "$(realpath "$0")")
project_root=$(realpath "$cwd/../..")
cd "$project_root"

# Activate virtual environment
if [ -f ".crm/bin/activate" ]; then
  source .crm/bin/activate
else
  echo "Virtual environment not found." >> /tmp/customer_cleanup_log.txt
  exit 1
fi

# Run cleanup logic
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
  echo \"[$(date '+%Y-%m-%d %H:%M:%S')] Deleted \$deleted inactive customers\" >> /tmp/customer_cleanup_log.txt
else
  echo \"[$(date '+%Y-%m-%d %H:%M:%S')] No deletions occurred.\" >> /tmp/customer_cleanup_log.txt
fi