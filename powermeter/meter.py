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
from threading import Thread


class Meter(object):
    def __init__(self, interval=20):
        self.interval = interval
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.powers = []
        self.thread = Thread(target=self._get_power_period,
                             name="powermeter_thread")
        self.thread.setDaemon(True)
        self.thread.start()
        self.sum = 0

    def _get_power_period(self):
        self._get_current_power(arrange_next=False)
        self.schedule.enter(self.interval, 1, self._get_current_power)
        self.schedule.run()

    def _get_current_power(self, arrange_next=True):
        # return in kilo watt
        if arrange_next:
            self.schedule.enter(self.interval, 1, self._get_current_power)
        else:
            pass
        self.powers.append(0.25)
        return 0.25

    def get_total_power(self):
        self.sum = sum(
            map(lambda x: float(x * self.interval/3600), self.powers))
        return self.sum

    def stop(self):
        self.get_total_power()
        print("Total Consumed: %0.2f Kwh" % self.sum)
        return self.sum

    def __del__(self):
        self.get_total_power()
        print("Total Consumed: %0.2f Kwh" % self.sum)
        return self.sum
