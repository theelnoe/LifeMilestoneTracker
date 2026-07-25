
DEFAULT_MILESTONES = [
    25,
    50,
    100,
    200,
    350,
    500,
    750,
    1000,
    1250,
    1500,
    2000,
    3000,
    5000
]

def generate_milestones(goal):

    milestones = []

    for m in DEFAULT_MILESTONES:

        if m < goal:
            milestones.append(m)

    milestones.append(goal)

    return milestones

def format_hours(value):

    total_minutes = round(value * 60)

    hours = total_minutes // 60

    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} m"

    if minutes == 0:
        return f"{hours} h"

    return f"{hours} h {minutes} m"