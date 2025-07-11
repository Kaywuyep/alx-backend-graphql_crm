import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client


def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    log_file_path = '/tmp/crm_heartbeat_log.txt'

    # Log basic heartbeat
    with open(log_file_path, 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")

    # Set up GraphQL client
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql/',
            verify=True,
            retries=3,
        )

        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
            query {
                hello
            }
        """)

        result = client.execute(query)
        hello_response = result.get("hello", "No response")

        with open(log_file_path, 'a') as f:
            f.write(f"{timestamp} GraphQL hello response: {hello_response}\n")

    except Exception as e:
        with open(log_file_path, 'a') as f:
            f.write(f"{timestamp} GraphQL hello error: {str(e)}\n")
