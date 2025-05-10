# core/time_calc.py
from datetime import datetime, timedelta
from gui.preferences import preferences

def round_time(dt):
    """Round time based on the selected algorithm in preferences."""
    algorithm = preferences.get("rounding_algorithm", "standard")
    
    if algorithm == "nearest_5":
        # Round to nearest 5 minutes
        minutes = dt.minute
        remainder = minutes % 5
        if remainder < 2.5:
            minutes -= remainder
        else:
            minutes += (5 - remainder)
        
        if minutes == 60:
            dt += timedelta(hours=1)
            minutes = 0
            
        return dt.replace(minute=minutes, second=0, microsecond=0)
    
    elif algorithm == "nearest_10":
        # Round to nearest 10 minutes
        minutes = dt.minute
        remainder = minutes % 10
        if remainder < 5:
            minutes -= remainder
        else:
            minutes += (10 - remainder)
            
        if minutes == 60:
            dt += timedelta(hours=1)
            minutes = 0
            
        return dt.replace(minute=minutes, second=0, microsecond=0)
    
    elif algorithm == "nearest_30":
        # Round to nearest 30 minutes
        minutes = dt.minute
        if minutes < 15:
            minutes = 0
        elif minutes < 45:
            minutes = 30
        else:
            dt += timedelta(hours=1)
            minutes = 0
            
        return dt.replace(minute=minutes, second=0, microsecond=0)
    
    elif algorithm == "ceiling":
        # Round up to next 15 minutes
        minute = dt.minute
        remainder = minute % 15
        if remainder > 0:
            minute += (15 - remainder)
            
        if minute == 60:
            dt += timedelta(hours=1)
            minute = 0
            
        return dt.replace(minute=minute, second=0, microsecond=0)
    
    elif algorithm == "floor":
        # Round down to previous 15 minutes
        minute = dt.minute
        remainder = minute % 15
        minute -= remainder
        return dt.replace(minute=minute, second=0, microsecond=0)
    
    else:
        # Standard rounding (15-minute intervals)
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
    
    # Get break settings from preferences for the appropriate day type
    lunch_info = preferences.get_break_info("lunch", is_weekday=is_weekday)
    dinner_info = preferences.get_break_info("dinner", is_weekday=is_weekday)
    
    # Parse lunch break time
    if lunch_info.get("enabled", True):
        lunch_time_str = lunch_info.get("start_time", "13:00")
        lunch_hour, lunch_minute = map(int, lunch_time_str.split(":"))
        lunch_break = datetime(entry_dt.year, entry_dt.month, entry_dt.day, lunch_hour, lunch_minute)
        
        # Check if lunch break falls within the work period
        if entry_dt <= lunch_break < exit_dt:
            try:
                end_time_str = lunch_info.get("end_time", "13:45" if is_weekday else "13:30")
                end_h, end_m = map(int, end_time_str.split(":"))
                end_time = datetime(lunch_break.year, lunch_break.month, lunch_break.day, end_h, end_m)
                duration = (end_time - lunch_break).total_seconds() / 60
                lunch_duration += timedelta(minutes=duration)
            except:
                # Fallback to default if there's an error
                default_duration = 45 if is_weekday else 30
                lunch_duration += timedelta(minutes=default_duration)

    # Parse dinner break time
    if dinner_info.get("enabled", True):
        dinner_time_str = dinner_info.get("start_time", "19:00")
        dinner_hour, dinner_minute = map(int, dinner_time_str.split(":"))
        dinner_break = datetime(entry_dt.year, entry_dt.month, entry_dt.day, dinner_hour, dinner_minute)
        
        # Check if dinner break falls within the work period
        if entry_dt <= dinner_break < exit_dt:
            try:
                end_time_str = dinner_info.get("end_time", "19:30")
                end_h, end_m = map(int, end_time_str.split(":"))
                end_time = datetime(dinner_break.year, dinner_break.month, dinner_break.day, end_h, end_m)
                duration = (end_time - dinner_break).total_seconds() / 60
                lunch_duration += timedelta(minutes=duration)
            except:
                # Fallback to default
                lunch_duration += timedelta(minutes=30)

    net_duration = work_duration - lunch_duration

    # Update the data cache
    data_cache["entry"] = entry_dt
    data_cache["exit"] = exit_dt
    data_cache["net_duration"] = net_duration
    
    return round(net_duration.total_seconds() / 3600, 2)