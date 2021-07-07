"""
MIT License

Copyright (c) 2019 Xiaozhe Yao

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
import sched
import time
from threading import Thread

from py3nvml.py3nvml import nvmlDeviceGetPowerUsage,  \
    nvmlDeviceGetCount,  \
    nvmlDeviceGetHandleByIndex, \
    nvmlInit, \
    nvmlShutdown


def try_get_info(f, h, default='N/A'):
    try:
        v = f(h)
    except:
        v = default
    return v


class Meter(object):
    def __init__(self, interval=20):
        try:
            nvmlInit()
            self.gpu = True
        except:
            self.gpu = False
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
        if self.gpu:
            num_gpus = nvmlDeviceGetCount()
            current_power = 0
            for i in range(num_gpus):
                h = nvmlDeviceGetHandleByIndex(i)
                power = try_get_info(nvmlDeviceGetPowerUsage, h, "-1")
                current_power += power/1000
            if arrange_next:
                self.schedule.enter(self.interval, 1, self._get_current_power)
            else:
                pass
        else:
            current_power = 0
        self.powers.append(current_power)
        return current_power

    def get_total_power(self):
        self.sum = sum(
            map(lambda x: float(x * self.interval/3600), self.powers))
        return self.sum

    def stop(self):
        if self.gpu:
            nvmlShutdown()
        else:
            pass
        self.get_total_power()
        print("Total Consumed: %0.2f Wh" % self.sum)
        print("Your Badge is Ready! See https://img.shields.io/badge/Power%20Consumption-{:.2f}%20Wh-green".format(self.sum))
        return self.sum
