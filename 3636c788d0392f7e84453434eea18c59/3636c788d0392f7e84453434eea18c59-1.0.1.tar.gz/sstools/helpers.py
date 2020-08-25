import datetime

def next_weekday(weekday=0, d=datetime.date.today()):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

# default - next monday

