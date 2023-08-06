"""
common_errors.py

Created by Ashish Patel on 14-12-2021
Copyright Ashish Patel, 2021

"""

import datetime
import os

name = ''

# Error messages
please_try_again = 'Please try again'

# Log messages
get_context_info = 'get_context'


def get_info() -> dict:
    return {'name': name}


class PerformanceTimer:
    def __init__(self):
        self.time_starts = {}
        self.timer_durations = {}
        self.infos = {}

    def start(self, name: str):
        time_now = datetime.datetime.utcnow()
        self.time_starts[name] = time_now

    def stop(self, name: str):
        time_now = datetime.datetime.utcnow()
        self.timer_durations[name] = round((time_now - self.time_starts[name]).total_seconds(), 3)

    def add(self, name: str):
        time_now = datetime.datetime.utcnow()
        if name in self.time_starts.keys():
            duration = time_now - self.time_starts[name]
            if name in self.duration.keys():
                self.timer_durations[name] = round(self.timer_durations[name] + duration.total_seconds(), 3)
            else:
                self.timer_durations[name] = round(duration.total_seconds(), 3)

    def clear(self, name: str):
        self.time_starts.pop(name, None)

    def reset(self):
        self.__init__()

    def add_info(self, name: str, increment: int = 1):
        if name in self.infos.keys():
            self.infos[name] = self.infos[name] + increment
        else:
            self.infos[name] = increment

    def get_result(self) -> dict:
        return {**self.timer_durations, **self.infos}


performance_timer = PerformanceTimer()