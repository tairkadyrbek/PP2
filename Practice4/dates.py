from datetime import datetime, date, timedelta

# 1) Subtract five days from current date
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print("Current date:", current_date)
print("Date 5 days ago:", five_days_ago)


# 2) Print yesterday, today, tomorrow
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


# 3) Drop microseconds from datetime
now = datetime.now()
no_microseconds = now.replace(microsecond=0)
print("Now:", now)
print("Without microseconds:", no_microseconds)


# 4) Date difference in seconds
dt1 = datetime(2024, 1, 1, 12, 0, 0)
dt2 = datetime(2024, 1, 2, 14, 30, 0)

diff = dt2 - dt1
seconds_diff = diff.total_seconds()

print("Difference in seconds:", seconds_diff)