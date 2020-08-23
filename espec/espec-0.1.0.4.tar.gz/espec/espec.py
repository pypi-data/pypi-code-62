from datetime import datetime, timedelta
import pendulum
from guang.Utils.date import LunarDate as Lunar
from guang.Utils.toolsFunc import dict_dotable
import dill
import os


class Mycrony:
    def __init__(self, data_file="data"):
        self.__crony = {}

        # self.name = ''
        self.load(data_file)
        self.__crony = dict_dotable(self.__crony)


    def set_name(self, name):
        self.name = name

    def set_birthday(self, date, lunarORsolar="lunar"):
        """
        --data: a  [year, month, day] list
        --lunarORsolar: "lunar" or "solar"
        """
        self.__crony.setdefault(self.name, {})
        self.__crony[self.name].setdefault("birthday", {})

        if lunarORsolar == "lunar":
            lunar_date = Lunar(*date)

            self.__crony[self.name]["birthday"]["lunar"] = lunar_date
            solar_date = lunar_date.to_datetime()
            self.__crony[self.name]["birthday"]["_solar"] = solar_date

        elif lunarORsolar == "solar":
            solar_date = datetime(*date)
            self.__crony[self.name]["birthday"]["solar"] = solar_date
            self.__crony[self.name]["birthday"][
                "_lunar"] = Lunar.from_datetime(solar_date)
        else:
            raise ValueError("lunarORsolar: lunar or solar")

    def get_current_birthday(self, name, lunarORsolar="lunar", tz="Asia/Shanghai"):
        """
        tz : "Asia/Shanghai", or otherwise
        Birth = {"lunar":self.__crony[name]["birthday"]["lunar"],
                 "solar":self.__crony[name]["birthday"]["solar"]}
        return Birth.get(lunarORsolar, None)
        """
        solar_now = pendulum.now(tz)  # beijing.now if tz=="beijing" else datetime.now()
        lunar_now = Lunar.from_datetime(solar_now)
        if lunarORsolar == "lunar":
            lunar_birthday = self.__crony[name]["birthday"]["lunar"]
            year = lunar_now.lunar_year
            return Lunar(year, lunar_birthday.lunar_month,
                         lunar_birthday.lunar_day)
        elif lunarORsolar == "solar":
            solar_birthday = self.__crony[name]["birthday"]["solar"]
            year = solar_now.year
            return datetime(year, solar_birthday.month, solar_birthday.day)
        else:
            raise ValueError("lunarORsolar: lunar/solar")

    def get_all_msg(self):
        return self.__crony

    def get_all_names(self):
        names = []
        for i in self.__crony.keys():
            names.append(i)
        return names

    def get_all_lunar_birthday(self):
        """
        return [name list, birthday list]
        """
        birthdays = []
        names = self.get_all_names()
        NAME = []
        for i in names:
            try:
                birthdays.append(self.__crony[i]["birthday"]["lunar"])
                NAME.append(i)
            except:
                continue
        return [NAME, birthdays]

    @classmethod
    def get_all_solar_birthday(cls):
        """
        return [name list, birthday list]
        """
        birthdays = []
        NAME = []
        names = cls.get_all_names()
        for i in names:
            try:
                birthdays.append(cls.__crony[i]["birthday"]["solar"])
                NAME.append(i)
            except:
                continue
        return [NAME, birthdays]

    @classmethod
    def get_valid_birthday(cls, name):
        """return all valid birthdays of current name"""
        birthdays = []
        try:
            birthdays.append(cls.__crony[name]["birthday"]["lunar"])
            try:
                birthdays.append(cls.__crony[name]["birthday"]["solar"])
            except:
                pass
        except:
            birthdays.append(cls.__crony[name]["birthday"]["solar"])
        return birthdays

    def get_all_valid_birthday(self):
        """
        return [name list, birthday list]
        """
        birthdays = []
        Names = []
        names = self.get_all_names()
        for i in names:
            try:
                birthdays.append(self.__crony[i]["birthday"]["lunar"])
                Names.append(i)
                try:
                    birthdays.append(self.__crony[i]["birthday"]["solar"])
                    Names.append(i)
                except:
                    pass
            except:
                birthdays.append(self.__crony[i]["birthday"]["solar"])
                Names.append(i)
        return [Names, birthdays]

    def find_name_from_birthday(self, date):
        """
        -- date can be Lunar type or Solar type

        """

        target_names = []
        if type(date).__name__ == "LunarDate":
            for i in self.get_all_names():
                try:
                    if self.__crony[i]["birthday"]["lunar"] == date:
                        target_names.append(i)
                except:
                    continue
            return target_names

        elif type(date).__name__ == "datetime":
            for i in self.get_all_names():
                try:
                    if self.__crony[i]["birthday"]["solar"] == date:
                        target_names.append(i)
                except:
                    continue
            return target_names

        else:
            raise ValueError(
                "The type of '--date' should be LunarDate or datetime")

    def del_brithday(self, name, date):
        """
        :arg date can be lunar or solar
        """
        if type(date).__name__ == "LunarDate":
            del self.__crony[name]["birthday"]["lunar"]
        elif type(date).__name__ == "datetime":
            del self.__crony[name]["birthday"]["solar"]
        else:
            print("'name' or 'date' invalid, nothing changes ")

    def load(self, data_file):
        try:
            with open(os.path.join(os.path.dirname(__file__), data_file), 'rb') as fi:
                self.__crony = dill.load(fi)
        except:
            print('The data file does not exist. A new one has been created')
            self.name = ''

    def save(self):
        with open(os.path.join(os.path.dirname(__file__), "data"), "wb") as fo:
            dill.dump(self.__crony, fo)

    @staticmethod
    def parseDeltaDays(delta_days):
        """
        return list[days, hours, minutes, seconds] of a daltatime type data.
        """
        days = delta_days.days
        total_seconds = delta_days.seconds
        hours, res_hour = divmod(total_seconds, 3600)
        minutes, seconds = divmod(res_hour * 3600, 60)
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }

    @property
    def crony(self):
        return self.__crony


def parseDate(date):
    """
    Parse the date into year, month, and day
    :param date: Lunar date or Solar date
    :return: year, month, day
    """
    if type(date).__name__ == "LunarDate":
        year = date.lunar_year
        month = date.lunar_month
        day = date.lunar_day
    elif type(date).__name__ == "datetime":
        year = date.year
        month = date.month
        day = date.day
    else:
        raise ValueError("'date' invalid!")
    return year, month, day

def get_current_lunar_year():
    solor_now = datetime.now()
    lunar_now = Lunar.from_datetime(solor_now)

    return lunar_now.lunar_year

def parseDate2solar(date, current_year=True):
    """parse date to solar date (datetime)
    :return: year, month, day
    """
    if type(date).__name__ == "LunarDate":
        if current_year:
            year = get_current_lunar_year()
            date = Lunar(year, date.lunar_month, date.lunar_day)
        date = date.to_datetime()

    return date.year, date.month, date.day


def delta_days(date1, date2):
    """
    return days of (date2 - date1)
    """
    if type(date1).__name__ == "LunarDate":
        date1 = date1.to_datetime()
    if type(date2).__name__ == "LunarDate":
        date2 = date2.to_datetime()
    d_dates = date2 - date1
    print(d_dates)
    # print(date1, date2)
    print(date1.timestamp())
    print(date2.timestamp())
    d_dates = pendulum.from_timestamp(date2.timestamp()) - pendulum.from_timestamp(date1.timestamp())
    return d_dates


def awayFromToday(specDate):
    """ return how much times is left before that special day
        :param specDate: `Lunar` or `datetime` type date.
    """
    _, specialMonth, specialDay = parseDate2solar(specDate)

    solarNow = datetime.now()
    now_year, now_month, now_day = parseDate(solarNow)

    specialDate_this_year = datetime(now_year, specialMonth, specialDay)
    delta_times = specialDate_this_year - solarNow

    if delta_times.days < -1:
        one_solor_year = (datetime(now_year + 1, specialMonth, specialDay) -
                          specialDate_this_year)
        specialDate_next_year = specialDate_this_year + one_solor_year
        delta_times = specialDate_next_year - solarNow

    return timedelta(
        days=delta_times.days,
        seconds=delta_times.seconds)  # In order not to show milliseconds


def all_in_period(all_date, period=7):
    """get {name:[days, date]} map dictionary for all_date
    """
    def is_in_period(date, period=7):
        """return (True, delta_time) or (False, None)"""
        delta_time = awayFromToday(date)
        if delta_time.days <= period:  # delta_time constant greater than zero
            # print(delta_time, date)
            return True, delta_time
        else:
            return False, None

    name_days = {}
    for name, date in zip(*all_date):
        is_true, days = is_in_period(date, period=period)
        if is_true:
            name_days[name] = [days, date]
    return name_days


if __name__ == "__main__":
    # pass
    # print(delta_days(datetime.now(), Lunar(2020, 3, 17)))
    print(awayFromToday(Lunar(1962, 7, 25)))
    print(awayFromToday(datetime(2020, 8, 26)))

    # from pprint import pprint;
    # person = Mycrony()
    # person.set_name('yao')
    # person.set_birthday([2020, 12, 18], "lunar")
    # person.set_birthday([2020, 1, 15], "solar")
    # person.save()
    #
    # # pprint(person.get_all_valid_birthday())
    # pprint(person.get_all_msg())
    # pprint(person.get_all_valid_birthday())

    # pprint(person.find_name_from_birthday(Lunar(2020,12,18)))
    # pprint(person.find_name_from_birthday(datetime(2020,1,10)))
    # remind_me = Remind()
    #
    # print(remind_me.who_will_be_remind())

    # person.save()
