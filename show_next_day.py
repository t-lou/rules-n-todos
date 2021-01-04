import utils
import datetime

time = datetime.datetime.now() + datetime.timedelta(days=1)
while time.isocalendar()[2] > 5:
    time += datetime.timedelta(days=1)
utils.show(time)

input()
