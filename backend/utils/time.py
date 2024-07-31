from datetime import datetime, UTC


def get_current_utc_time():
    return datetime.now(UTC).replace(tzinfo=None)
