# core/time_calc.py
from datetime import datetime, timedelta

def round_time(dt):
    """Round time to nearest 15-minute interval."""
    minute = dt.minute
    if minute < 8:
        minute = 0
    elif minute < 23:
        minute = 15
    elif minute < 38:
        minute = 30
    elif minute < 53:
        minute = 45
    else:
        dt += timedelta(hours=1)
        minute = 0
    return dt.replace(minute=minute, second=0, microsecond=0)

def calculate_work_hours(entry_time, exit_time, is_weekday, data_cache):
    """Calculate net working hours with meal breaks."""
    entry_dt = round_time(datetime.strptime(entry_time, "%H:%M"))
    exit_dt = round_time(datetime.strptime(exit_time, "%H:%M"))
    work_duration = exit_dt - entry_dt

    lunch_duration = timedelta()
    if is_weekday:
        lunch_1 = datetime(entry_dt.year, entry_dt.month, entry_dt.day, 13, 0)
        dinner = datetime(entry_dt.year, entry_dt.month, entry_dt.day, 19, 0)
        if entry_dt <= lunch_1 < exit_dt:
            lunch_duration += timedelta(minutes=45)
        if entry_dt <= dinner < exit_dt:
            lunch_duration += timedelta(minutes=30)
    else:
        lunch_1 = datetime(entry_dt.year, entry_dt.month, entry_dt.day, 13, 0)
        dinner = datetime(entry_dt.year, entry_dt.month, entry_dt.day, 19, 0)
        if entry_dt <= lunch_1 < exit_dt:
            lunch_duration += timedelta(minutes=30)
        if entry_dt <= dinner < exit_dt:
            lunch_duration += timedelta(minutes=30)

    net_duration = work_duration - lunch_duration

    # Update the data cache
    data_cache["entry"] = entry_dt
    data_cache["exit"] = exit_dt
    data_cache["net_duration"] = net_duration
    
    return round(net_duration.total_seconds() / 3600, 2)