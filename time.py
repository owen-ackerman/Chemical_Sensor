from datetime import datetime
from time import sleep

x = datetime.now()
print(x.strftime("%b") + "_" + x.strftime("%d") + "_" + x.strftime("%Y"))

