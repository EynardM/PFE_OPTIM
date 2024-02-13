from util.imports import *
from util.locations import *
from util.helpers import *
from util.objects import *
from util.datamodule import get_data

from algorithms.helpers import *
from algorithms.run import *

tab = []

for i in range(10):
    tab.append(i)

print(tab[:0])
print(tab[:2]) # -1 -> 0, 0 -> 1 etc on met position+1 donc ici 5 ça veut dire qu'on avait 4 -> 5