from datetime import datetime

time_period_config = {
    "1": {"start": datetime(2021, 2, 16), "end": datetime(2022, 2, 16)},
    "2": {"start": datetime(2020, 2, 16), "end": datetime(2022, 2, 16)},
    "3": {"start": datetime(2019, 2, 16), "end": datetime(2022, 2, 16)},
    "4": {"start": datetime(2018, 2, 16), "end": datetime(2022, 2, 16)},
    "5": {"start": datetime(2017, 2, 16), "end": datetime(2022, 2, 16)},
    "6": {"start": datetime(2016, 2, 16), "end": datetime(2022, 2, 16)},
    "7": {"start": datetime(2015, 2, 16), "end": datetime(2022, 2, 16)},
    "8": {"start": datetime(2014, 2, 16), "end": datetime(2022, 2, 16)},
    "9": {"start": datetime(2013, 2, 16), "end": datetime(2022, 2, 16)},
    "10": {"start": datetime(2012, 2, 16), "end": datetime(2022, 2, 16)},
}

three_year_period_config = {
    "1": {"start": datetime(2021, 2, 16), "end": datetime(2022, 2, 16)},
    "3": {"start": datetime(2018, 2, 16), "end": datetime(2021, 2, 16)},
    "4": {"start": datetime(2019, 2, 16), "end": datetime(2022, 2, 16)},
}

class bttimer:
    start_date: datetime
    end_date: datetime

    def __init__(self, period: int) -> None:
        self.start_date = three_year_period_config[str(period)]["start"]
        self.end_date = three_year_period_config[str(period)]["end"]