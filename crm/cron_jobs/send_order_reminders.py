#!/usr/bin/env python3

import requests
import datetime
import json

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

# Define the date range for the last 7 days
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

# Convert dates to ISO 8601 strings
date_from = seven_days_ago.isoformat()

# GraphQL query string
query = """
query GetRecentOrders($from: Date!) {
  allOrders(orderDateGte: $from) {
    edges {
      node {
        id
        orderDate
        customer {
          email
        }
      }
    }
  }
}
"""

# Variables for the query
variables = {
    "from": date_from
}

try:
    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"}
    )

    data = response.json()
    orders = data["data"]["allOrders"]["edges"]

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        for order in orders:
            order_id = order["node"]["id"]
            email = order["node"]["customer"]["email"]
            log.write(f"[{timestamp}] Reminder for Order ID: {order_id}, Email: {email}\n")

    print("Order reminders processed!")

except Exception as e:
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] ERROR: {e}\n")
    print("Failed to process order reminders.")
