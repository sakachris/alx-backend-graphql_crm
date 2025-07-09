# crm/cron.py
import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_line = f"{timestamp} CRM is alive\n"

    try:
        with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
            log_file.write(log_line)

        # Optionally, query the hello field (you need to define one in your schema)
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ __typename }"},
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        if response.status_code != 200:
            with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
                log_file.write(f"{timestamp} WARNING: GraphQL endpoint unresponsive\n")

    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} ERROR: {str(e)}\n")
