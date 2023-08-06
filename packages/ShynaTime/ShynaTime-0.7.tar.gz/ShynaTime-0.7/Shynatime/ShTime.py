from datetime import datetime, date, timedelta


class ClassTime:
    """Class to maintain the default and standard date and time application wide"""
    now_time = datetime.now().time().__format__('%H:%M:%S')
    now_date = date.today()
    how_many = 0
    string_value = '12-12-2020'

    def subtract_hour(self, from_time, how_many):
        self.how_many = how_many
        """Need from time and number of hours needs to be subtracted. returns datetime.datetime value"""
        from_time = str(from_time).split('.')[0]
        new_time = (datetime.strptime(str(from_time), '%H:%M:%S') - timedelta(hours=int(self.how_many))).time()
        return new_time

    def add_hour(self, from_time, how_many):
        """Need from time and number of hours needs to be Added. returns datetime.datetime value"""
        self.how_many = how_many
        from_time = str(from_time).split('.')[0]
        new_time = (datetime.strptime(str(from_time), '%H:%M:%S') + timedelta(hours=int(self.how_many))).time()
        return new_time

    def subtract_date(self, from_date, how_many):
        """Need from date and number of days needs to be subtracted. returns datetime.datetime value"""
        self.how_many = how_many
        new_date = datetime.strptime(str(from_date - timedelta(days=int(self.how_many))), '%Y-%m-%d')
        return new_date

    def add_date(self, from_date, how_many):
        """Need from date and number of days needs to be added. returns datetime.datetime value"""
        self.how_many = how_many
        new_date = datetime.strptime(str(from_date + timedelta(days=int(self.how_many))), '%Y-%m-%d')
        return new_date

    def string_to_date(self, date_string):
        """Need date which need to be converted into datetime.datetime format."""
        self.string_value = date_string
        convert_date = datetime.strptime(str(self.string_value), '%Y-%m-%d')
        return convert_date

    def string_to_time(self, time_string):
        """Need time which need to be converted into datetime.datetime format."""
        self.string_value = time_string
        convert_time = datetime.strptime(str(self.string_value), '%H:%M:%S')
        return convert_time

    def get_day_of_week(self):
        """Return the day number in string format being 0 as Monday and 6 as Sunday"""
        self.string_value = datetime.today().weekday()
        return str(self.string_value)
