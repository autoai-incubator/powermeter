"""
MIT License

Copyright (c) 2019 AutoAI.org

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import sys
import atexit
import sched
import time


class Meter(object):
    def __init__(self, interval=20):
        self.interval = interval
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.powers = []
        self.schedule.enter(self.interval, 1, self.get_current_power)
        self.schedule.run()
        self.sum = 0

    def get_current_power(self):
        # return in kilo watt
        self.powers.append(0.25)
        # arrange next run
        self.schedule.enter(self.interval, 1, self.get_current_power)

    def get_total_power(self):
        print(self.powers)
        self.sum = sum(map(lambda x: float(x * self.interval/3600), self.powers))
        print(self.sum)

    def __del__(self):
        self.get_total_power()
        print("Total Consumed:" + str(self.sum))
