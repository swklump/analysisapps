def excel_date(date1):
    from datetime import datetime
    temp = datetime(1899, 12, 30)
    date1 = datetime.strptime(str(date1), '%Y-%m-%d %H:%M:%S')
    delta = date1 - temp
    return round(float(delta.days) + (float(delta.seconds) / 86400), 5)