#Write a Python program to subtract five days from current date.
from datetime import date, timedelta
today = date.today()
result = today - timedelta(days=5)
print(result)


#Write a Python program to print yesterday, today, tomorrow.
from datetime import date, timedelta
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


#Write a Python program to drop microseconds from datetime.from datetime import datetime
now = datetime.now()
no_microseconds = now.replace(microsecond=0)
print(no_microseconds)


#Write a Python program to calculate two date difference in seconds.
from datetime import datetime
date1 = datetime(2025, 1, 1, 12, 0, 0)
date2 = datetime(2025, 1, 2, 14, 30, 0)
difference = date2 - date1
print(difference.total_seconds())






