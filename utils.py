from datetime import datetime, timedelta
def calculate_future_date(initial_date_str, timedelta_days):
    # Convert the initial date string to a datetime object
    initial_date = datetime.strptime(initial_date_str, '%Y-%m-%d')

    # Calculate the future date
    future_date = initial_date + timedelta(days=timedelta_days)

    # Format the future date as a string in the same format
    future_date_str = future_date.strftime('%Y-%m-%d')

    return future_date_str