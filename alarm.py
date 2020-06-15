import datetime as dt
import os
import webbrowser
from datetime import datetime as dtt
from time import sleep

from config import links


def get_input_time():
    hour = input("시간을 입력하세요: ")
    minute = (input('분을 입력하세요: '))
    assert int(hour) in range(0, 25)
    assert int(minute) in range(0, 61)
    return ':'.join([hour.zfill(2), minute.zfill(2)])


def get_alarm_time(input_time: str):
    tz_kst = dt.timezone(dt.timedelta(hours=9))
    now = dtt.now(tz_kst)
    time = dtt.strptime(input_time, '%H:%M').time()
    alarm_time = dtt.combine(now, time, tzinfo=tz_kst)
    if alarm_time < now:
        alarm_time += dt.timedelta(days=1)
    return alarm_time


def get_check_duration(target, timezone):
    now = dtt.now(timezone)
    delta = target - now
    delta = delta.seconds
    if delta > 3600:
        return 'hour'
    elif delta > 600:
        return '5-minute'
    elif delta > 300:
        return 'minute'
    elif 300 > delta > 30:
        return 'second'
    else:
        return 'now'


def open(url):
    webbrowser.open_new(url)


class YoutubeAlarmClock:
    durations = {
        'hour': 3600,
        '5-minute': 300,
        'minute': 60,
        'second': 1
    }

    def __init__(self):
        input_time = get_input_time()
        self.browser = 'Google Chrome'
        self.tz = dt.timezone(dt.timedelta(hours=9))
        self.alarm_time = get_alarm_time(input_time)
        if dtt.now(self.tz).date() < self.alarm_time.date():
            start = 0
        else:
            delta = dtt.now(self.tz) - dtt.combine(dtt.now(self.tz), dt.time(), tzinfo=self.tz)
            start = delta.seconds
        self.lullaby = f'https://youtu.be/9IbQi4qZzh4?t={start}'
        self.alarm = links['alarm']
        self.set_check_duration()
        print(f"alarm time: {self.alarm_time}")
        print(f"check dura: {self.check_duration}")
        self.play_lullaby()
        self.alarm_main()

    def alarm_main(self):
        while True:
            if self.check_duration == 'now':
                self.stop_lullaby()
                self.play_alarm()
                break

            duration = self.durations[self.check_duration]
            sleep(duration)
            now = dtt.now(self.tz)
            print(now.time().strftime("%H:%M"))
            self.set_check_duration()
            print(self.check_duration)

    def kill_browser(self):
        os.system(f"killall -9 '{self.browser}'")

    def set_check_duration(self):
        self.check_duration = get_check_duration(self.alarm_time, self.tz)

    def play_lullaby(self):
        self.kill_browser()
        open(self.lullaby)

    def stop_lullaby(self):
        self.kill_browser()

    def play_alarm(self):
        open(self.alarm)
