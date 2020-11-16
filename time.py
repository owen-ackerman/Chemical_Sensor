from datetime import datetime
from time import sleep


for x in range (0,5):
    now = datetime.now()
    seconds = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds
    print(seconds)
    sleep(1)
