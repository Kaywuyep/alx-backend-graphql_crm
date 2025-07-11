import datetime
import requests # type: ignore


def log_crm_heartbeat():
    """a cron job"""
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    log_message = f"{timestamp} CRM is alive\n"

    with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
        log_file.write(log_message)

    # Optional: Query the GraphQL hello field
    try:
        response = requests.post(
            'http://localhost:8000/graphql/',  # adjust if running on different port or domain
            json={'query': '{ hello }'},
            timeout=3
        )
        if response.ok:
            with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
                log_file.write(f"{timestamp} GraphQL hello response: {response.json()}\n")
        else:
            with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
                log_file.write(f"{timestamp} GraphQL hello failed: HTTP {response.status_code}\n")
    except Exception as e:
        with open('/tmp/crm_heartbeat_log.txt', 'a') as log_file:
            log_file.write(f"{timestamp} GraphQL hello exception: {str(e)}\n")
