from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql('''
    query {
        totalCustomers: allCustomers {
            totalCount
        }
        totalOrders: allOrders {
            totalCount
        }
        allOrders {
            edges {
                node {
                    totalAmount
                }
            }
        }
    }
    ''')

    try:
        result = client.execute(query)
        customers = result['totalCustomers']['totalCount']
        orders = result['totalOrders']['totalCount']
        revenue = sum([float(edge['node']['totalAmount']) for edge in result['allOrders']['edges']])

        log_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report: {customers} customers, {orders} orders, {revenue:.2f} revenue\n"

        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(log_msg)

    except Exception as e:
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {str(e)}\n")
