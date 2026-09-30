def format_wait_time(seconds):
    seconds = int(seconds)

    if seconds < 60:
        return f"{seconds} second{'s' if seconds != 1 else ''}"

    minutes = seconds // 60

    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''}"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if remaining_minutes == 0:
        return f"{hours} hour{'s' if hours != 1 else ''}"

    return (
        f"{hours} hour{'s' if hours != 1 else ''} "
        f"{remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"
    )
