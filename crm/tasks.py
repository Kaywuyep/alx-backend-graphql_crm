import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


@shared_task
def generate_crm_report():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "./tmp/crm_report_log.txt"

    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql/',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """)

        result = client.execute(query)
        customers = result['totalCustomers']
        orders = result['totalOrders']
        revenue = result['totalRevenue']

        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")

    except Exception as e:
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - ERROR: {str(e)}\n")
