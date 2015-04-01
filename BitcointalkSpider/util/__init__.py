def timeFormat(time):
    try:
        if time.find('at'):
            today = datetime.today()
            time = datetime.strptime(time.strip(), 'at %I:%M:%S %p')
            time = time.replace(today.year, today.month, today.day)
        else:
            time = datetime.strptime(time.strip(), "%B %d, %Y, %I:%M:%S %p")
        return time
    except:
        return None