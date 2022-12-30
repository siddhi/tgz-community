from datetime import timedelta, datetime

def pluralise(amount, word):
    if amount == 1:
        return f'{amount} {word} ago'
    return f'{amount} {word}s ago'

def humanise_timedelta(delta: timedelta):
    if delta < timedelta(hours=1):
        return "within an hour"
    elif delta < timedelta(days=1):
        return pluralise(delta.seconds//3600, "hour")
    else:
        return pluralise(delta.days, "day")

def humanise(timestamp):
    return humanise_timedelta(datetime.utcnow() - timestamp)
