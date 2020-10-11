import time
import datetime

class Schedule(object):
    MON=1
    TUE=2
    WED=3
    THU=4
    FRI=5
    SAT=6
    SUN=7

    def __init__(self, app_context, days, hour, minute, duration, enabled):
        self.app_context = app_context
        self.days = days
        self.hour = hour
        self.minute = minute
        self.duration = duration
        self.enabled = enabled

    def get_next_sprinkle_time(self, since):
        if not self.enabled:
            return None
        #time_now = self.app_context.time()
        #date_time = datetime.datetime.fromtimestamp(time_now)
        # find day to sprinkle next
        #f = open('/tmp/x.txt','w')
        time_now_i = since
        for i in range(7):
            datetime_i = datetime.datetime.fromtimestamp(time_now_i)
            #print('days {}'.format(self.days))
            if datetime_i.isoweekday() in self.days:

                sprinkle_time_i = datetime.datetime(
                    datetime_i.year,
                    datetime_i.month,
                    datetime_i.day,
                    self.hour,
                    self.minute,
                )
                #f.write("check {}\n".format(sprinkle_time_i))
                resulting_time = time.mktime(sprinkle_time_i.timetuple())

                # if today is the day - is it in future
                if resulting_time > since:
                    #f.write('found\n')
                    return resulting_time

            # iterating to next day
            next_day = datetime.datetime(
                datetime_i.year,
                datetime_i.month,
                datetime_i.day,
                0,
                0
            ) + datetime.timedelta(days=1)
            #f.write("next day {}\n".format(next_day))
            time_now_i = time.mktime(
                                next_day.timetuple()
                        )
        exit(1)
    #def is_time_now(self):
    #    time_now = self.app_context.time()
    #    date_time = datetime.datetime.fromtimestamp(time_now)
