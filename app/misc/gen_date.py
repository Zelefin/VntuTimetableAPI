import datetime


def gen_weeks_dates() -> list[dict[int, str]]:
    """
    Generate weeks dates. Returns a list where 0 element is 1-st week and 1 element is 2-nd week.
    Each week is a dict with keys {day_num: date} like so: {0: "22.04", 1: "23.04" ...}
    :return: [1 week with dates, 2 week with dates]
    """
    today = datetime.date.today()

    this_week_start = today - datetime.timedelta(days=today.weekday())

    weeks = [
        {
            i: (this_week_start + datetime.timedelta(days=7 * week + i)).strftime(
                "%d.%m"
            )
            for i in range(7)
        }
        for week in range(2)
    ]

    return weeks if today.isocalendar()[1] % 2 == 0 else weeks[::-1]
