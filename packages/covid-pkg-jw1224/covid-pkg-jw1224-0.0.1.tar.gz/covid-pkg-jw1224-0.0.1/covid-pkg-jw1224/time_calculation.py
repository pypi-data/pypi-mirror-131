
'''
This module deals with calculations involving time using the 
datetime module.

'''

from datetime import datetime
from datetime import timedelta



def time_difference(update_time: str) -> int:
    '''Calculates time difference between now and the given update time'''
    now = str(datetime.now().time())
    now = now[0:8]
    t_diff = datetime.strptime(update_time, '%H:%M') - datetime.strptime(now, '%H:%M:%S')
    if t_diff.days < 0:
        t_diff += timedelta(1)
    t_diff = str(t_diff)
    h, m, s = t_diff.split(':')
    total = int(h)*3600 + int(m)*60 + int(s)
    return total

def time_passed(update_time):
    '''Calculate which schedule has been updated by comparing the time'''
    now = str(datetime.now().time())
    now = now[0:5]
    if now == update_time:
        equal = True
    else:
        equal = False
    return equal
