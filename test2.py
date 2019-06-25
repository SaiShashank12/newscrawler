from summizer import run as sm
from aljazeera import run as al
from downtoearth import run as de
import threading as th


t1 = th.Thread(target=sm)
t2 = th.Thread(target=al)
t3 = th.Thread(target=de)

try:
    t1.start()
except:
    print('t1')    
try:
    t2.start()
except:
    print('t2')
try:
    t3.start()
except:
    print('t3')   
t1.join()
t2.join()
t3.join()
