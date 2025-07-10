#!/usr/bin/env python3
"""
Order Reminders Script
Queries GraphQL endpoint for pending orders from
the last week and logs reminders.
"""

import os
import sys
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def get_pending_orders():
    """
    Query GraphQL endpoint for orders with order_date within the last 7 days.
    Returns a list of orders with ID and customer email.
    """
    # Calculate date 7 days ago
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    # Set up GraphQL client
    transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define GraphQL query
    query = gql("""
        query GetPendingOrders($startDate: String!) {
            orders(where: { order_date: { _gte: $startDate } }) {
                id
                order_date
                customer {
                    email
                }
            }
        }
    """)

    # Execute query
    variables = {"startDate": seven_days_ago}
    result = client.execute(query, variable_values=variables)

    return result.get('orders', [])


def log_order_reminder(order_id, customer_email, log_file_path):
    """
    Log order reminder with timestamp to the specified file.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] Order ID: {order_id}, Customer Email: {customer_email}\n"

    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)


def main():
    """
    Main function to process order reminders.
    """
    log_file_path = '/tmp/order_reminders_log.txt'

    try:
        # Get pending orders from GraphQL
        pending_orders = get_pending_orders()

        # Process each order
        for order in pending_orders:
            order_id = order.get('id')
            customer_email = order.get('customer', {}).get('email')

            if order_id and customer_email:
                log_order_reminder(order_id, customer_email, log_file_path)

        # Print completion message
        print("Order reminders processed!")

    except Exception as e:
        # Log error with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_msg = f"[{timestamp}] ERROR: {str(e)}\n"

        with open(log_file_path, 'a') as log_file:
            log_file.write(error_msg)

        print(f"Error processing order reminders: {e}")
        sys.exit(1)
