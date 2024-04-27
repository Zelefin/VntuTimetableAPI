import datetime


def gen_weeks_dates() -> list[dict[int, str]]:
    """
    Generate weeks dates. Returns a list where 0 element is 1-st week and 1 element is 2-nd week.
    Each week is a dict with keys {day_num: date} like so: {0: "22.04", 1: "23.04" ...}
    :return: [1 week with dates, 2 week with dates]
    """

    today: datetime.date = datetime.date.today()
    this_week_start: datetime.date = today - datetime.timedelta(
        days=(today.weekday()) % 7
    )
    next_week_start: datetime.date = this_week_start + datetime.timedelta(days=7)

    this_week_dates: dict[int, str] = {
        i: (this_week_start + datetime.timedelta(days=i)).strftime("%d.%m")
        for i in range(7)
    }
    next_week_dates: dict[int, str] = {
        i: (next_week_start + datetime.timedelta(days=i)).strftime("%d.%m")
        for i in range(7)
    }

    return (
        [this_week_dates, next_week_dates]
        if datetime.date.isocalendar(datetime.date.today())[1] % 2 == 0
        else [next_week_dates, this_week_dates]
    )
