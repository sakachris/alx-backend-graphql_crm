# crm/cron.py

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_line = f"{timestamp} CRM is alive\n"

    # Append heartbeat to log file
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(log_line)

    # Optional GraphQL query to test endpoint responsiveness
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("{ hello }")
        result = client.execute(query)

        # Append GraphQL response for visibility (optional)
        with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} GraphQL response: {result.get('hello')}\n")

    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} ERROR querying GraphQL: {str(e)}\n")


def update_low_stock():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_path = "/tmp/low_stock_updates_log.txt"

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql("""
    mutation {
      updateLowStockProducts {
        updatedProducts {
          name
          stock
        }
        message
      }
    }
    """)

    try:
        result = client.execute(mutation)
        updated = result.get("updateLowStockProducts", {}).get("updatedProducts", [])
        message = result.get("updateLowStockProducts", {}).get("message", "")

        with open(log_path, "a") as log:
            log.write(f"{timestamp} - {message}\n")
            for p in updated:
                log.write(f"  • {p['name']} → stock: {p['stock']}\n")

    except Exception as e:
        with open(log_path, "a") as log:
            log.write(f"{timestamp} - ERROR: {str(e)}\n")