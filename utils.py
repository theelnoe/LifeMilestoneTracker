
def format_duration(value):

    total_minutes = round(value * 60)

    hours = total_minutes // 60

    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} m"

    if minutes == 0:
        return f"{hours} h"

    return f"{hours} h {minutes} m"

def calculate_elapsed_minutes(start_time, end_time):

    elapsed = end_time - start_time

    return round(elapsed.total_seconds() / 60)

