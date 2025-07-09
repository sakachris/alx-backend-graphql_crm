# CRM Weekly Report Task

## Setup Instructions

1. **Install Dependencies**:
    ```bash
    pip install celery django-celery-beat redis gql
    ```

2. **Start Redis**:
    ```bash
    sudo systemctl start redis
    ```

3. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

4. **Start Celery Workers**:
    - Celery:
      ```bash
      celery -A crm worker -l info
      ```
    - Beat:
      ```bash
      celery -A crm beat -l info
      ```

5. **View Report Logs**:
    - Check `/tmp/crm_report_log.txt` for weekly reports.
