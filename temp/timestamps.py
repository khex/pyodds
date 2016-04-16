from datetime import date, datetime

nowt = datetime.utcnow()
posx = int(datetime.timestamp(nowt))
odds = date.fromtimestamp(posx)
# в сутках 86400 секунд

print(posx, odds)
