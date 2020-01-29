class Timestamp(object):
    def __init__(self, hours: int = 0, mins: int = 0, secs: float = 0.0):
        self.hours = hours
        self.minutes = mins
        self.seconds = secs

    @classmethod
    def from_string(cls, s):
        """
        Parse a string into a Timestamp
        :param s: a string formatted as [[hh:]mm:]ss[.zzz]
        :return: a Timestamp
        """
        time_comp = s.strip().split(':')

        hours = 0
        mins = 0
        secs = 0.0
        if len(time_comp) > 0:
            secs = float(time_comp[-1])
            if len(time_comp) > 1:
                mins = int(time_comp[-2])
                if len(time_comp) > 2:
                    hours = int(time_comp[-3])

        # Safety checks if ths string is not well formatted
        if secs >= 60.0:
            add_mins = int(secs) // 60
            secs -= add_mins * 60.0
            mins += add_mins

        if mins >= 60:
            add_hours = mins // 60
            mins -= add_hours * 60
            hours += add_hours
        # Safety checks end

        return cls(hours=hours, mins=mins, secs=secs)

    @classmethod
    def from_milliseconds(cls, millisecs: int):
        secs = millisecs / 1000.0

        hours = int(secs) // 3600
        secs -= hours * 3600.0

        mins = int(secs) // 60
        secs -= mins * 60.0

        return Timestamp(hours=hours, mins=mins, secs=secs)

    def __str__(self):
        return "{hh:02d}:{mm:02d}:{ss:06.3f}".format(hh=self.hours, mm=self.minutes, ss=self.seconds)

    @property
    def hours(self) -> int:
        return self._hours

    @hours.setter
    def hours(self, hours: int):
        if hours < 0:
            raise ValueError("Hours cannot be negative")
        self._hours = hours

    @property
    def minutes(self):
        return self._mins

    @minutes.setter
    def minutes(self, mins):
        if mins < 0:
            raise ValueError("Minutes cannot be negative")
        elif mins >= 60:
            raise ValueError("Minutes cannot be more than 59")
        self._mins = mins

    @property
    def seconds(self):
        return self._secs

    @seconds.setter
    def seconds(self, secs):
        if secs < 0.0:
            raise ValueError("Seconds cannot be negative")
        elif secs >= 60.0:
            raise ValueError("Seconds cannot be more than 60.0")
        self._secs = secs

    @property
    def total_milliseconds(self) -> int:
        """
        Converts hh:mm:ss.zzz into integer milliseconds
        :return: number of milliseconds
        """
        seconds = (self.hours * 3600) + (self.minutes * 60) + self.seconds
        return int(seconds * 1000)
