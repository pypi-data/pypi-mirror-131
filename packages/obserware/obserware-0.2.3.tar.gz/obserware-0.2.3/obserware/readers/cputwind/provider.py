"""
Obserware
Copyright (C) 2021 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import psutil


def return_mainscreen_threaded_statistics():
    timedict, cputsecs, cputperc, cputusej, cputqant = (
        {},
        psutil.cpu_times(percpu=True),
        psutil.cpu_times_percent(percpu=True),
        psutil.cpu_percent(percpu=True),
        psutil.cpu_count(),
    )
    for indx in range(cputqant):
        timedict[indx] = {
            "usage": cputusej[indx],
            "seconds": {
                "user": cputsecs[indx].user,
                "nice": cputsecs[indx].nice,
                "system": cputsecs[indx].system,
                "idle": cputsecs[indx].idle,
                "iowait": cputsecs[indx].iowait,
                "irq": cputsecs[indx].irq,
                "softirq": cputsecs[indx].softirq,
                "steal": cputsecs[indx].steal,
                "guest": cputsecs[indx].guest,
                "guest_nice": cputsecs[indx].guest_nice,
            },
            "percent": {
                "user": cputperc[indx].user,
                "nice": cputperc[indx].nice,
                "system": cputperc[indx].system,
                "idle": cputperc[indx].idle,
                "iowait": cputperc[indx].iowait,
                "irq": cputperc[indx].irq,
                "softirq": cputperc[indx].softirq,
                "steal": cputperc[indx].steal,
                "guest": cputperc[indx].guest,
                "guest_nice": cputperc[indx].guest_nice,
            },
        }
    retndata = {"timedict": timedict}
    return retndata


def return_mainscreen_onetimed_statistics():
    retndata = psutil.cpu_count()
    return retndata
