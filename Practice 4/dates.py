from datetime import datetime, timedelta

# 1
old_date = datetime.now()
new_date = old_date - timedelta(days=5)
print(new_date.strftime("%d/%m/%Y"))


# 2
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print('Today: ', today)
print('Yesterday: ', yesterday)
print('Tomorrow: ', tomorrow)


# 3
date = datetime.now()
print(date.replace(microsecond=0))


# 4
date1 = datetime.now()
date2 = datetime.now() - timedelta(days=2)
n = date1 - date2
print(n.total_seconds())